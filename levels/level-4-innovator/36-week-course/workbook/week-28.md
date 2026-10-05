# Workbook — Week 28: Tools and the Loop

**Name:** ________________________________  **Date:** ______________

[⬅ Week 27](week-27.md) · [📖 Read the chapter first](../student-guide/week-28.md) · [Course Home](../README.md) · [Next ➡](week-29.md)

---

> **Rules for this workbook.** This week has no new maths. The pen-and-paper work is *reading requests, predicting what a check says, and pricing turns*. Then the computer confirms. **Write your answer by hand first, then run.** A guess written after the run is not a guess.
>
> **Real numbers.** Every number printed below came from a real run of the code shown. Nothing uses randomness, so your numbers should match (the kit counts tokens itself; the dollars use the kit's **illustrative** price of 1.00 per million tokens in and 5.00 per million out, which is not any company's price list). By-hand numbers are plain arithmetic.
>
> **There is no model here.** Every "model" in this workbook is a scripted plan, a **stand-in, not a model**. It replays what a person typed. A fence that stops a scripted plan is a fence that works; it says **nothing** about how a real model behaves.
>
> **Files you need.** Run every code block in the **same Python session** as your `tools_and_loop.py` from the chapter, straight after it, because the blocks use its names: `ast`, `walk`, `ROOT`, `resolved`, `inside`, `SPEC`, `specs`, `validate_args`, `reg`, `once`, `toyagent` and `r` (the worked run). Run it from the folder that contains `l4lib/`, `notes/` and `sandbox/`. Import `l4lib`; never copy it. Nothing needs the internet.
>
> **Calculator.** Plain arithmetic is enough.

---

## ✅ Warm-Up (5 min, before anything else, from memory)

1. Who runs a tool: the model or your program? ____________________
2. Name the six fences, in any order. ____________________________________________________________
3. Which of the six read the sentence "be careful" in the prompt? ______ Which need a model to be present? ______
4. A stop reason of `end_turn`. Does it mean the task worked? Where do you look instead? ____________________________________________________________

---

## 🎲 Page 28.0 — Which Fence? (in class · 12 min · pen only, no computer)

Six fences: `1` turns cap · `2` money cap · `3` sandbox (folder, suffix, size) · `4` timeout · `5` allowlist · `6` a human says yes. A request may also be stopped by the **tool's own check** (write `0`), or it may be fine (write `none`). Name **one** for each. The model has been told to be careful.

| | Request | Your answer |
|:--:|---|:--:|
| A | `calculate("2 + 2")` | |
| B | `calculate("__import__('os').getcwd()")` | |
| C | `write_file("../notes.md", "hi")` (the human said yes) | |
| D | `write_file("run.sh", "hi")` (the human said yes) | |
| E | `delete_everything()` (no such tool exists) | |
| F | a plan that calls `calculate("1 + 1")` over and over, forever | |
| G | `write_file("plan.md", "hi")` (the human said no) | |
| H | a tool that sleeps 30 seconds; the limit is 10 | |
| I | `write_file("sub/a.md", "hi")` (there is no folder `sub`) | |
| J | `write_file("big.md", <25,000 letters>)` (the human said yes) | |

(b) Which **one** of A to J should not be stopped at all? ______

(c) Which **one** is stopped by a check that is not a security fence? ______ What does the model get back? ____________________________________________________________

(d) The model was told "be careful". Which fences read that sentence? ______

---

## 🧰 Page 28.1 — A Fourth Tool (30 min · think first, then type)

Your kit has three tools: `calculate`, `search_notes`, `write_file`. You will add a fourth, `count_words(text)`, which returns the number of words in a piece of text, as a string.

**Predict first.** A tool needs some number of separate things before the loop will use it safely. The function itself is one. Write what you think the others are: ____________________________________________________________

**Step 1.** Only the function and the registry entry. Before you run it, predict what `validate_args("count_words", {"text": "one two three"})` returns, when the contract has **not** been written yet: ____________________

```python
# count_words_a.py - Page 28.1, step 1: ONLY the function and the registry entry. No contract yet.
def count_words(text):
    return str(len(text.split()))

reg.register("count_words", count_words, timeout=2.0)
print("in the registry:", reg.has("count_words"))
print("validate_args says:", validate_args("count_words", {"text": "one two three"}))
```

```text
in the registry: True
validate_args says: ["no tool named 'count_words'"]
```

**Read it.** The registry has it, and `validate_args` still says `no tool named 'count_words'`. Why? Write it: ____________________________________________________________

**Step 2.** Write the contract. It has the same shape as the others: a name, a sentence saying when to use it, and typed arguments. Fill in what you expect **before** you run the block:

| call | your prediction for `validate_args` |
|---|---|
| `{"text": "one two three"}` | |
| `{"text": 5}` | |
| `{}` | |
| `{"text": "a", "extra": 1}` | |

```python
# count_words_b.py - Page 28.1, step 2: add the contract, then check four calls.
SPEC["count_words"] = {"name": "count_words",
                       "description": "Count the words in one piece of text. Not for arithmetic.",
                       "input_schema": {"type": "object",
                                        "properties": {"text": {"type": "string"}},
                                        "required": ["text"],
                                        "additionalProperties": False}}
specs_plus = specs + [SPEC["count_words"]]
tests = [{"text": "one two three"}, {"text": 5}, {}, {"text": "a", "extra": 1}]
for args in tests:
    print(f"{str(args):28s} -> {validate_args('count_words', args)}")
```

```text
{'text': 'one two three'}    -> []
{'text': 5}                  -> ["'text' must be string, got int"]
{}                           -> ["missing 'text'"]
{'text': 'a', 'extra': 1}    -> ["unknown argument 'extra'"]
```

**Step 3.** A scripted plan (a stand-in, not a model) calls the new tool once. Predict the `is_error` flag and the result text: ____________________

```python
# count_words_c.py - Page 28.1, step 3: a scripted plan that calls the new tool. The plan is a STAND-IN, NOT A MODEL.
cw = toyagent.run_agent("q", reg, specs_plus, once("count_words", {"text": "one two three"}))
print([(c["tool"], c["is_error"]) for c in cw["tool_calls"]])
print([e["result_preview"] for e in cw["trace"] if e["event"] == "tool_call"])
print("stop:", cw["stop"], "| label:", cw["label"])
```

```text
[('count_words', False)]
['3']
stop: end_turn | label: stand-in, not a model
```

**Your sentence.** The function `count_words` works on its own. Why is it **not enough** on its own? (Hint: look at Step 1.) ____________________________________________________________

---

## 🧱 Page 28.2 — Predict the Sandbox (30 min · pen first, then run)

`inside(ROOT, name)` resolves the name first and then asks whether the result is at or below `ROOT`. For each of the eight names below, write `True` or `False` for `inside` **before you run anything**. Row 8 is a story and has no code: reason it out.

| # | name | your `inside` |
|:--:|---|:--:|
| 1 | `notes.md` | |
| 2 | `one/two/../../ok.md` (two `..`, and they cancel two real folders) | |
| 3 | `one/../../bad.md` (two `..`, and only one of them has a folder to cancel) | |
| 4 | `../sandbox/ok.md` (up one folder, then straight back down into `sandbox`) | |
| 5 | `/tmp/x.md` | |
| 6 | `../sandbox-evil/x.md` (a *sibling* folder whose name starts with `sandbox`) | |
| 7 | `.` (the folder itself) | |
| 8 | `link/x.md`, where `link` is a shortcut (a symbolic link) **inside** the sandbox that points to the folder above it | |

Now run the block. It also shows three **DELIBERATELY wrong** checks, one per column, so you can see which one would have given each of your answers. The three are the "dots" test (`".." not in name`), the "compare-first" test (compare the joined path *before* `resolve`) and the "text" test (`startswith` on the text of the paths).

```python
# sandbox_eight.py - Page 28.2: seven names, the right check, and three WRONG checks (DELIBERATELY wrong, for comparison).
def inside_dots(root, filename):        # WRONG 1: "no two dots"
    return ".." not in filename

def inside_lexical(root, filename):     # WRONG 2: compare first, resolve later
    return (root / filename).is_relative_to(root)

def inside_text(root, filename):        # WRONG 3: compare the TEXT with startswith
    return str(resolved(root, filename)).startswith(str(root))

names = ["notes.md", "one/two/../../ok.md", "one/../../bad.md", "../sandbox/ok.md",
         "/tmp/x.md", "../sandbox-evil/x.md", "."]
print(f"{'name':22s} {'inside':7s} {'dots':6s} {'lexical':8s} {'text':6s}")
for n in names:
    print(f"{n:22s} {str(inside(ROOT, n)):7s} {str(inside_dots(ROOT, n)):6s} {str(inside_lexical(ROOT, n)):8s} {str(inside_text(ROOT, n)):6s}")
```

```text
name                   inside  dots   lexical  text  
notes.md               True    True   True     True  
one/two/../../ok.md    True    False  True     True  
one/../../bad.md       False   False  True     False 
../sandbox/ok.md       True    False  True     True  
/tmp/x.md              False   True   False    False 
../sandbox-evil/x.md   False   False  True     True  
.                      True    True   True     True  
```

Mark every row where you were wrong with a cross: #____, #____, #____. For each one, name the wrong check (dots / lexical / text) that would have given **your** wrong answer: ____________________________________________________________

**Three questions.**

i. Row 4 is `True` for the right check. Which of the three wrong checks gets row 4 wrong, and which gets it right by luck? ____________________________________________________________

ii. Row 6 is a sibling folder. Which wrong check is fooled by it, and why does `is_relative_to` (which compares *parts* of a path, not letters) not fall for it? ____________________________________________________________

iii. Row 8 cannot be run without new syntax, so reason it out. What does `resolve()` do with a shortcut? What do the "dots" test and the "compare-first" test say about `link/x.md`, and what does the right check say? ____________________________________________________________

---

## 💰 Page 28.3 — Pay the Bill (30 min · pen first, then run)

The price is 1.00 per million tokens in and 5.00 per million out. Cost in **millionths of a dollar** = `tokens in × 1 + tokens out × 5`. The worked run from the chapter had five turns:

| turn | in | out |
|:--:|:--:|:--:|
| 1 | 247 | 28 |
| 2 | 415 | 10 |
| 3 | 448 | 25 |
| 4 | 519 | 19 |
| 5 | 566 | 20 |

**Part 1 — the trace by hand (10 min).**

(a) Turn 1 in millionths: `247 × 1 + 28 × 5 =` ______ → dollars: ______

(b) The five "in" numbers add to ______; the five "out" numbers add to ______. Cost in millionths = ______ × 1 + ______ × 5 = ______ → dollars: $______

(c) How much did the input grow from turn 1 to turn 2? ______ What arrived in between that explains most of it? ____________________________________________________________

```python
# bill_trace.py - Page 28.3, Part 1: the five turns of the worked run, priced two ways.
p_in, p_out = 1.0, 5.0           # the kit's ILLUSTRATIVE price, per million tokens
turns = [e for e in r["trace"] if e["event"] == "model_turn"]
total_in = sum(e["in_tok"] for e in turns)
total_out = sum(e["out_tok"] for e in turns)
print("inputs :", [e["in_tok"] for e in turns], "sum", total_in)
print("outputs:", [e["out_tok"] for e in turns], "sum", total_out)
millionths = total_in * p_in + total_out * p_out
print("millionths of a dollar:", millionths, "-> dollars:", millionths / 1e6)
print("the trace's own spend :", round(r["spend"], 6))
```

```text
inputs : [247, 415, 448, 519, 566] sum 2195
outputs: [28, 10, 25, 19, 20] sum 102
millionths of a dollar: 2705.0 -> dollars: 0.002705
the trace's own spend : 0.002705
```

Does your (b) match the printed `spend`? ______ If not, find the slip before you go on.

**Part 2 — a steady staircase (10 min).** Real steps are not all the same size (`168, 33, 71, 47`). To see the *shape*, pretend every step adds the same `g = 32` tokens, starting from `223` at turn 1. A task of *n steps* has `n + 1` turns: turn 1, then one more turn for each step.

(d) The input at turn 5 of such a task is `223 + 4 × 32 =` ______

(e) Ten steps (eleven turns). The inputs are `223, 255, 287, …`. Ten steps add `1 + 2 + … + 10 =` ______. So the growth adds ______ × 32 = ______ tokens on top of eleven copies of 223 (which is ______).

(f) Twenty steps: `1 + 2 + … + 20 =` ______. Is 20 steps **twice, three times or four times** as dear as 10 steps, *for the growth part*? Your guess: ______ (then divide: ______ / ______ = ______)

```python
# bill_growth.py - Page 28.3, Part 2: a steady 32 tokens of growth per step. A SHAPE, not a measurement of any real system.
first, g = 223, 32
for steps in (10, 20):
    inputs = [first + g * i for i in range(steps + 1)]      # turn 1, then one more turn per step
    growth = sum(inputs) - first * len(inputs)
    print(f"{steps:2d} steps: {len(inputs)} turns, last input {inputs[-1]}, growth part {growth}, "
          f"total input {sum(inputs)}, input-only cost ${sum(inputs) * 1.0 / 1e6:.6f}")
print("1+2+...+10 =", sum(range(1, 11)), "  1+2+...+20 =", sum(range(1, 21)))
print("growth ratio 20 steps / 10 steps:", round(sum(range(1, 21)) / sum(range(1, 11)), 1))
print("total ratio  20 steps / 10 steps:", round((21 * first + g * 210) / (11 * first + g * 55), 2))
```

```text
10 steps: 11 turns, last input 543, growth part 1760, total input 4213, input-only cost $0.004213
20 steps: 21 turns, last input 863, growth part 6720, total input 11403, input-only cost $0.011403
1+2+...+10 = 55   1+2+...+20 = 210
growth ratio 20 steps / 10 steps: 3.8
total ratio  20 steps / 10 steps: 2.71
```

(g) The *whole* input, growth and all, grows by a smaller factor than the growth part. Why? (Hint: eleven copies of 223 do not grow like a staircase.) ____________________________________________________________

**Part 3 — measured, not pretended (5 min).** The same shape, measured on the kit's own loop. The scripted plan calls `calculate` `k` times in a row and then answers. This is a stand-in, not a model, and the number of tokens per step belongs to this plan only.

```python
# bill_measured.py - Page 28.3, Part 3: the same shape, measured on the kit's loop with a scripted plan (STAND-IN, NOT A MODEL).
tiny = toyagent.ToolRegistry()
tiny.register("calculate", toyagent.calculate)
for k in (4, 8):
    plan = toyagent.ScriptedModel([("", [("calculate", {"expression": "1 + 1"})])] * k + [("done", [])])
    ins = toyagent.run_agent("q", tiny, specs, plan, max_iterations=k + 1)["in_tokens"]
    extra = sum(x - ins[0] for x in ins)
    print(f"k={k} tool turns: first {ins[0]}, last {ins[-1]}, growth part {extra}, k(k+1)/2 = {k * (k + 1) // 2}, per step {extra / (k * (k + 1) / 2):.1f}")
```

```text
k=4 tool turns: first 223, last 353, growth part 324, k(k+1)/2 = 10, per step 32.4
k=8 tool turns: first 223, last 483, growth part 1168, k(k+1)/2 = 36, per step 32.4
```

(h) The shape `k(k+1)/2` matches the measured growth to within a step size of about ______ tokens per step. The staircase in Part 2 used 32. Why is pretending with 32 reasonable, and what would you not conclude about a real model from it? ____________________________________________________________

(i) In one sentence: why is a long task dearer than it looks? ____________________________________________________________

**Finish with three sentences** (homework): what a fence **proves**, what it **does not** prove, and what a scripted plan says about a real model.

1. ____________________________________________________________
2. ____________________________________________________________
3. ____________________________________________________________

---

## 🐞 Page 28.4 — Break It on Purpose (three bugs · 25 min)

Each block below is **DELIBERATELY wrong**. Predict, run, then write what it meant and the fix.

### 28.4-A (SILENT) — a "kind of int" check

Two words sound the same and are not: "is it an integer?" and "is it a kind of integer?" In Python, `True` is a kind of integer.

```python
# break_a.py - DELIBERATE BUG 28.4-A (SILENT): a "kind of int" check.
def count_ok_bad(value):
    return isinstance(value, int)

print([count_ok_bad(v) for v in (3, True, "3", 2.5)])
print("True + True =", True + True)
```

(i) Predict the first line. Four values: `3`, `True`, `"3"`, `2.5`. Which does the check say yes to? ____________________

(ii) Run it. What printed? ____________________ Which of the chapter's two checks (the calculator's `walk`, or `validate_args`) could this bug have slipped into? ____________________

(iii) Fix it in one line, two ways: ____________________________________________________________

### 28.4-B (loud) — the tree of a program, not of an expression

```python
# break_b.py - DELIBERATE BUG 28.4-B (loud): ast.parse without mode="eval".
tree = ast.parse("2 + 3")
print(type(tree).__name__, type(tree.body).__name__)
print(walk(tree.body))
```

(i) Predict what `type(tree).__name__` and `type(tree.body).__name__` print. ____________________

(ii) Run it. Read the last line of the message. What type did `walk` refuse? ____________________

(iii) What one piece of the `ast.parse` call is missing? ____________________

### 28.4-C (SILENT) — the switch left on

```python
# break_c.py - DELIBERATE BUG 28.4-C (SILENT): auto_approve=True left on "just for testing".
r_bad = toyagent.run_agent("q", reg, specs, once("write_file", {"filename": "hello.md", "content": "hi"}),
                           auto_approve=True, confirm=lambda name, args: False)
print("stop:", r_bad["stop"])
print("the confirm function said no, but hello.md exists:", (ROOT / "hello.md").exists())
(ROOT / "hello.md").unlink()
```

(i) The `confirm` function says no to everything. Predict: does `hello.md` exist afterwards? ____________________

(ii) Run it. What printed? ____________________ What did `auto_approve=True` do to fence number ____?

(iii) Why is `auto_approve=True` right for some runs and wrong for others? ____________________________________________________________

(iv) A reminder: the block ends with `(ROOT / "hello.md").unlink()`, which removes the file it made. Nothing else is deleted.

---

## 📓 Page 28.5 — The Bug Log

Add **at least two** entries, one of them SILENT. Then copy this sentence in your own handwriting on the last line of the page:

> **"The model asks; my code checks, limits and acts. A fence is a line of code that holds whether or not anything obeys the prompt, so I can test every one with no model at all, but a scripted plan proves the fences, not the agent."**

| # | File / page | What I saw | What it meant | The fix | How I would catch it next time |
|:--:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

---

## 🧠 Self-Check (from memory, no notes)

1. What is the model's whole job in a tool call? ____________________________________________________________
2. Why does `ast.parse` make a safer calculator than `eval`? ____________________________________________________________
3. "Resolve first, compare second." What goes wrong if you compare first? ____________________________________________________________
4. A timeout fired. Has the slow tool stopped? ____________________________________________________________
5. Why does the budget fence stop one call late? ____________________________________________________________
6. A valid citation is in the answer. What does that prove, and what check does the answer still need? ____________________________________________________________
7. Why is turn 5 dearer than turn 2 when the "model" says about the same number of words? ____________________________________________________________
8. The scripted plan recovered from the error at turn 3. Who decided to drop the folder name? ____________________________________________________________

---

# ✂️ ANSWERS - keep this page folded until you have finished

### Warm-Up

1. **Your program.** The model only asks (a name and arguments). 2. Turns cap, money cap, sandbox, timeout, allowlist, a human. 3. **None** read the prompt; **none** needs a model. 4. **No.** `end_turn` only says the loop ended because the "model" answered in words. Look at the **tool results** (the `Error:` text) and at the answer itself, and check it against the source.

### Page 28.0

| | Answer | Why |
|:--:|:--:|---|
| A | **none** | A good request; it gives `4`. Not everything should be stopped. |
| B | **0** | The calculator's own whitelist refuses it (`unsupported expression element: Call`). It is the tool's contract, not one of the six. |
| C | **3** | The sandbox. The human said yes; the fence did not care. |
| D | **3** | The sandbox's suffix list (`.sh` is not allowed). |
| E | **5** | The allowlist: `no tool named 'delete_everything'`. |
| F | **1** | The turns cap (`max_iterations`). |
| G | **6** | A human declined; nothing is written. |
| H | **4** | The timeout. |
| I | **none of the six** (an ordinary tool error) | The message is a hint (`directory 'sub' does not exist in the sandbox`): the model can read it and retry flat. Accept "3" if you said *why* it is a hint and not a wall. |
| J | **3** | The sandbox's size limit (`content too large: 25000 bytes > 20000`). |

(b) **A.** (c) **I**: the model gets a plain-English `ValueError` saying the folder does not exist. (d) **None.** The prompt is a request to a model; the fences are code. (The money cap, fence 2, is not in A to J; the chapter's second row of the fence table shows it.)

### Page 28.1

Predict: **three** things: the function, the registry entry, and the contract (the spec that `validate_args` reads).

Step 1: `["no tool named 'count_words'"]`. `validate_args` reads the **contract** (`SPEC`), not the registry; the function is registered but the contract does not exist yet, so the model could never be *told* about the tool and its arguments cannot be checked.

Step 2:

| call | result |
|---|---|
| `{"text": "one two three"}` | `[]` (fine) |
| `{"text": 5}` | `["'text' must be string, got int"]` |
| `{}` | `["missing 'text'"]` |
| `{"text": "a", "extra": 1}` | `["unknown argument 'extra'"]` |

Step 3: `is_error` is `False` and the result text is `3`. Sentence: a function alone is not a tool. Without the contract the model is never shown it and nothing checks its arguments; without the registry entry the loop cannot run it. Accept any sentence that names the contract and says what it is for.

### Page 28.2

| # | `inside` | why |
|:--:|:--:|---|
| 1 | `True` | plain, below the root |
| 2 | `True` | both `..` cancel the two folders just entered, so the file lands in the root |
| 3 | `False` | one `..` cancels `one`; the second climbs **out** of the root |
| 4 | `True` | up one folder, then back down into `sandbox`: the real path is `<ROOT>/ok.md` |
| 5 | `False` | an absolute path throws the root away |
| 6 | `False` | `sandbox-evil` is a different folder, next to the sandbox |
| 7 | `True` | the folder itself is "at or below" itself |
| 8 | `False` | `resolve()` follows the shortcut to the folder above |

The check prints:

```text
name                   inside  dots   lexical  text  
notes.md               True    True   True     True  
one/two/../../ok.md    True    False  True     True  
one/../../bad.md       False   False  True     False 
../sandbox/ok.md       True    False  True     True  
/tmp/x.md              False   True   False    False 
../sandbox-evil/x.md   False   False  True     True  
.                      True    True   True     True  
```

Reading it. The **dots** test is wrong on rows **2, 4 and 5**: it refuses the safe names 2 and 4 (they contain `..`), and it says `True` to the absolute path in row 5 (`/tmp/x.md` has no dots at all). It gets rows 3 and 6 right only because those names happen to contain `..`. The **compare-first** (lexical) test is wrong on rows **3 and 6**: before `resolve` cancels the `..`, the joined text still starts with `ROOT`. The **text** test (`startswith` after resolving) is wrong on **row 6** only: the letters of `sandbox-evil` begin with the letters `sandbox`. Rows 1 and 7 are right for all four.

i. Row 4 is a safe name. The **dots** test gets it **wrong** (it sees `..` and refuses); the compare-first and text tests get it right, and so does the right check. A test that refuses safe names is wrong in the harmless direction; row 5 shows the same test wrong in the harmful direction. ii. The **text** test (and the compare-first test too, on this row). `startswith` compares letters; `sandbox-evil` begins with the letters `sandbox`. `is_relative_to` compares whole parts (`sandbox-evil` is not `sandbox`). iii. `resolve()` follows the shortcut and reports the real place, which is outside. The dots test has no `..` to see and says `True` (wrong); the compare-first test joins the text and sees it still starts with `ROOT`, so it says `True` (wrong); the right check says `False`. A text comparison cannot see a shortcut; only the file system can.

### Page 28.3

Part 1. (a) `247 × 1 + 28 × 5 = 247 + 140 =` **387** → **$0.000387**. (b) Inputs **2195**, outputs **102**; `2195 × 1 + 102 × 5 = 2195 + 510 =` **2705** millionths → **$0.002705** (the printed `spend`). (c) `415 − 247 =` **168**; the search result (the two notes' text) arrived as a tool result and is now part of the conversation that is re-sent.

Printed by the run:

```text
inputs : [247, 415, 448, 519, 566] sum 2195
outputs: [28, 10, 25, 19, 20] sum 102
millionths of a dollar: 2705.0 -> dollars: 0.002705
the trace's own spend : 0.002705
```

Part 2. (d) `223 + 128 =` **351**. (e) **55**; `55 × 32 =` **1760**; eleven copies of 223 = **2453**; total input `2453 + 1760 =` **4213**. (f) **210**; `210 / 55 =` **3.8**: **about four times** for twice the steps (the guess "four" is closest).

```text
10 steps: 11 turns, last input 543, growth part 1760, total input 4213, input-only cost $0.004213
20 steps: 21 turns, last input 863, growth part 6720, total input 11403, input-only cost $0.011403
1+2+...+10 = 55   1+2+...+20 = 210
growth ratio 20 steps / 10 steps: 3.8
total ratio  20 steps / 10 steps: 2.71
```

(g) The eleven or twenty-one copies of 223 grow only in step with the number of turns (twice the steps is about twice as many copies); only the staircase part grows like the square. The two added together are `2.71` times, which lies between 2 and 3.8. Longer tasks drift towards 4.

Part 3.

```text
k=4 tool turns: first 223, last 353, growth part 324, k(k+1)/2 = 10, per step 32.4
k=8 tool turns: first 223, last 483, growth part 1168, k(k+1)/2 = 36, per step 32.4
```

(h) About **32.4** tokens per step (your Part 2 figure of 32 was close enough). Pretending with a steady step is a *shape* only: the real steps in the trace were `168, 33, 71, 47`, and these numbers belong to a scripted plan and the kit's counter. You cannot conclude how large a real model's steps would be, how many it would take, or what a real price list would say. (i) Each turn re-sends the whole history, so the input grows every turn and the total grows roughly with the square of the number of steps.

Three sentences, for example: *A fence proves that, for the requests I tried, the code stops the request whatever the prompt says. It does not prove that every request is covered, nor that the tools behind the fence are safe. A scripted plan says nothing about a real model: it only exercises my code.*

### Page 28.4

**A.** (i) Expect `[True, False, False, False]`; the surprise is in the run. (ii) `[True, True, False, False]` and `True + True = 2`. The bug could slip into either `walk` (which would accept `True + True`) or `validate_args` (which would accept `k=True` as a count). (iii) `type(value) is int`, or `isinstance(value, int) and not isinstance(value, bool)`.

**B.** (i) `Module list`. (ii) `ValueError: not allowed here: list` (the last line names the type refused). (iii) `mode="eval"`: without it `ast.parse` returns a `Module`, whose `.body` is a **list** of statements. Fix: `ast.parse("2 + 3", mode="eval")` and `walk(tree.body)`.

**C.** (i) The honest expectation is `False` (a "no" should stop the write). (ii) `True`: the file exists. `auto_approve=True` switched off fence **6**: the person's "no" was never asked. (iii) It is right when nobody is at the keyboard and you want the *sandbox* to be what answers (the chapter's fence drill); it is wrong for anything else, because fence 6 is then a wall with no door. The kit's default asks on the keyboard and end-of-input counts as "no".

### Page 28.5 and Self-Check

Bug Log: any two true entries, one SILENT, each naming a check that would have caught it (a case that can fail; a `True` and a `False` tried on purpose; checking that a declined write leaves `sandbox/` empty).

1. Pick a tool name and fill in the arguments. 2. `ast.parse` only reads the text as a tree, and your code runs only what is on your list; `eval` lets the text decide. 3. The text can still start with the sandbox's name while `..` would carry it out (`../escape.md` passes). 4. **No**: it stopped the waiting, not the work; a write tool may still land its file. 5. Spend is checked **before** each turn, so the turn that crosses the budget has already happened. 6. Only that the writer named a note it was given; the answer still needs your check against the note itself. 7. Its input is bigger (566 vs 415) because the whole history is re-sent. 8. The **plan** (a person typed it). A real model might not.
