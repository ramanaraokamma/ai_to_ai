# Week 28 — Tools and the Loop

[⬅ Week 27](week-27.md) · [Course Home](../README.md) · [Week 29 ➡](week-29.md) · [Workbook](../workbook/week-28.md)

---

> ### This week in one sentence
> **A tool is a function plus a contract, and the model only asks: your code checks, limits and acts, so every fence (a check in your code that holds whatever the prompt says) that keeps an agent safe is a line of Python you can test with no model at all.**
>
> **By the end of this chapter you will be able to:**
> - **Say what a tool is** (a function plus a contract) and who does what in the loop: *perceive, decide, act, observe, stop*
> - **Turn text into a tree with `ast.parse`** and build a calculator that refuses everything except arithmetic
> - **Test a path by resolving it first** and comparing second, with `Path.resolve()` and `is_relative_to`
> - **Check arguments against the tool's contract** with `isinstance` before the tool runs
> - **Enforce a timeout** with `ThreadPoolExecutor`, and say what a timeout does *not* do
> - **Fire all six fences from plain Python** and name each one from its stop reason or error text
> - **Read a real trace**: five turns, the stop reason, the money spent and why the input grows every turn
>
> **New maths:** **none.** The only arithmetic is pricing a turn (`tokens in × price + tokens out × price`) and noticing that a long task re-sends its history.
>
> **New syntax:** `ast.parse` with an `operator` whitelist · `Path.resolve()` + `is_relative_to` · `isinstance` checks on arguments · `ThreadPoolExecutor`
>
> **Reading time:** about 25 minutes. **In class:** 70 minutes. **Homework:** about 55 minutes (workbook pages 28.1 to 28.3).

> **📌 About the code blocks.** Put the blocks in **one file**, `tools_and_loop.py`, in the order they appear, or paste them into one Python session. Later blocks use names made by earlier ones. Run it from the folder that contains `l4lib/` and `notes/` (the notes from Week 26). Every output shown was printed by a real run on a CPU. **There is no randomness anywhere today**, so your numbers should match, except the "waited … s" timings, which vary a little. Nothing needs the internet.

> **⚠️ There is no model in this chapter. Every "model" is a scripted plan, a stand-in, not a model.** `toyagent.ScriptedModel` replays a list of steps a person typed. It cannot be fooled, cannot forget and cannot invent a tool. The loop, the fences, the trace and the *shape* of the cost growth are real code. The choices the "model" makes are typed text, so **nothing measured today says anything about how a real model behaves**. Tokens are counted by the kit's local counter and dollars use an **illustrative** price table (`fake-small`: 1.00 in, 5.00 out, per million tokens). It is not any company's price list.

---

## 🪝 Start Here

For four terms your programs have done one thing: text in, text out. From today the assistant gets **hands**. It can look things up, do sums and save files. That is useful, and it is the reason this week is about **what stops it**.

Before any code, write three guesses on a card.

1. You type `eval("2 + 3 * 4")` and get `14`. That is a calculator in one line. What else could the text inside `eval(...)` do?
2. A model is asked a question, and it answers "please run `write_file`". Who runs it: the model, or your program?
3. The model is told, in its instructions, "be careful, never write outside the sandbox" (the one folder it may write in). A request to write `../notes.md` arrives anyway. What stops it: the instruction, or something else?

Keep the card. We come back to it at the end.

---

## 🧠 The Big Idea

A **tool** is a function plus a **contract**. The contract (also called a *spec* or *schema*) is what the model is shown: a name, a sentence saying when to use it, and the named, typed arguments it takes. The model never sees the function. Its whole job is to pick a name and fill in the arguments. **Everything else is your code.**

The **agent loop** has five steps, over and over.

```text
perceive -> decide -> act -> observe -> stop
```

- **Perceive.** The model is sent the question and *everything so far*.
- **Decide.** It answers in words (we are done) or with a **tool call**: a name and arguments.
- **Act.** Your code looks the name up, checks it, runs it, and gets a **tool result**.
- **Observe.** The result goes back to the model as text. Each pass round the loop is one **iteration**.
- **Stop.** When the model answers in words, or when a fence says so. The reason is recorded as a **stop reason**: `end_turn`, `max_iterations` or `budget_exhausted`.

A **guardrail** (we say **fence**) is a line of code that holds whether or not anything obeys the prompt. There are six.

| # | Fence | What it does | What you will see |
|:--:|---|---|---|
| 1 | **Turns cap** | the loop ends after so many iterations | `max_iterations` |
| 2 | **Money cap** | the loop ends when spend passes a budget | `budget_exhausted` |
| 3 | **Sandbox** | files only inside one folder; suffix and size limits | `PermissionError` |
| 4 | **Timeout** | one tool call may not be waited on forever | `timed out` |
| 5 | **Allowlist** | only tools you registered can be called | `no tool named` |
| 6 | **A human** | a write needs a person to say yes | `declined` |

None of the six reads the prompt. None needs a model. **That is how you test them.**

A tool that fails is not a crash. It is a message the model gets to read, and today's worked run has exactly that at turn 3.

---

## 1. The four new pieces of syntax

Each on a toy small enough to read. Type this first.

**`isinstance(value, type)`** asks "is this value of this type?". `isinstance(3, int)` is `True` and `isinstance("3", int)` is `False`. **One trap:** in Python a `bool` *is* a kind of `int`, so `isinstance(True, int)` is `True` too. You will meet this again in the argument check.

**`ast.parse(text, mode="eval")`** is Python's own parser as a library. It turns the *text* of an expression into a **tree** of objects **without running anything**. `.body` is the top of the tree. A sum has the type `BinOp` (two things joined by an operator), and its `.op` says which operator.

**`Path.resolve()` and `.is_relative_to(root)`.** A path such as `root / "../a.md"` is a path *made of text*. `.resolve()` asks the file system where it really points: it cancels every `..`, makes the path absolute and follows shortcuts. `.is_relative_to(root)` asks "is this path at or below `root`?".

**`ThreadPoolExecutor`.** A *thread* is a second line of execution inside your program. `pool.submit(fn, ...)` starts `fn` in a thread and at once hands back a `future`, a promise of a result. `future.result(timeout=1.0)` waits at most a second for it.

```python
# toys.py - the four new pieces on toys small enough to read
import ast
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
print(isinstance(3, int), isinstance("3", int), isinstance(True, int))
tree = ast.parse("1 + 2", mode="eval")
print(type(tree.body).__name__, type(tree.body.op).__name__)
root = Path("sandbox").resolve()
print((root / "a.md").resolve().is_relative_to(root), (root / "../a.md").resolve().is_relative_to(root))
pool = ThreadPoolExecutor(max_workers=1)
future = pool.submit(pow, 2, 10)
print(future.result(timeout=1.0))
```

```text
True False True
BinOp Add
True False
1024
```

Read it line by line. Line 1: the trap, `True` counts as an `int`. Line 2: the text `1 + 2` became a `BinOp` whose operator is `Add`. Line 3: `sandbox/a.md` is inside `sandbox`, and `sandbox/../a.md` resolves to a file *next to* `sandbox`, so it is not. Line 4: `pow(2, 10)` ran in another thread and gave `1024`.

---

## 2. Load the notes and the tool contracts

Your first lines are Week 26's load (three lines), then the contracts the kit ships. `toyagent.tool_specs()` returns the list the model would be shown.

```python
# tools_and_loop.py - Week 28. Part 1: the load, then the tool contracts the kit ships.
import ast
import operator
import time
from pathlib import Path
from l4lib import rag, toyagent

files = sorted(Path("notes").glob("note-*.md"))
chunks = [open(p).read().strip() for p in files]
titles = rag.notebook_titles(chunks)
index = rag.VectorIndex(chunks, rag.TfidfEmbedder())
specs = toyagent.tool_specs()
print(len(files), "notes;", len(index), "chunks in the index")
print("tools in the spec:", [s["name"] for s in specs])
print("calculate takes:", specs[0]["input_schema"]["required"], " search_notes requires:", specs[1]["input_schema"]["required"])
```

```text
15 notes; 15 chunks in the index
tools in the spec: ['calculate', 'search_notes', 'write_file']
calculate takes: ['expression']  search_notes requires: ['query']
```

If `ModuleNotFoundError: No module named 'l4lib'` appears, you are in the wrong folder: go to the one that *contains* `l4lib/`. If there is no `notes/` folder, run Week 26's `setup_notes.py` once.

---

## 3. See the tree

Before writing a calculator, look at what `ast.parse` makes of three pieces of text. **Predict the third before you run it.** It is an attack, so what kind of thing must it contain?

```python
# tree.py - what ast.parse makes of text. Nothing is run; the text is only turned into a tree.
print(ast.dump(ast.parse("2 + 3 * 4", mode="eval").body))
print(ast.dump(ast.parse("-5", mode="eval").body))
print(ast.dump(ast.parse("__import__('os').getcwd()", mode="eval").body))
```

```text
BinOp(left=Constant(value=2), op=Add(), right=BinOp(left=Constant(value=3), op=Mult(), right=Constant(value=4)))
UnaryOp(op=USub(), operand=Constant(value=5))
Call(func=Attribute(value=Call(func=Name(id='__import__', ctx=Load()), args=[Constant(value='os')], keywords=[]), attr='getcwd', ctx=Load()), args=[], keywords=[])
```

Read the first as "a sum of 2 and (a product of 3 and 4)". The multiplication sits *inside* the addition, so it is done first. The second is a minus sign in front of a 5. The third contains a `Call`: it asks Python to run something. **Nothing ran.** `ast.parse` only reads. So the plan is: read the text, and run it only if **every piece of the tree is on a list we wrote**.

---

## 4. A calculator that cannot run anything but arithmetic

A **whitelist** is a list of what *is* allowed, with everything else refused. Ours allows numbers and six operators. `OPS` maps each operator's *class* (`ast.Add`) to an ordinary function from the `operator` module (`operator.add` is `+` as a function).

The function `walk` is **given to you: copy it, do not try to invent it**. It calls itself: to work out `2 + 3 * 4` it first works out `3 * 4`, which is the same job on a smaller tree. It stops because a plain number has no smaller tree inside it. Read its four `if` branches aloud: a number; a minus in front; two things joined by an operator; anything else is refused. You write `OPS`, `calc` and the test loop.

Two details in `walk`. It checks `type(node.value) in (int, float)` and not `isinstance`, because of the trap above: `True` is an `int`, and we want `True + True` refused. And it refuses a huge power (`**` on big numbers can swallow gigabytes of memory).

```python
# calc.py - a calculator that cannot run anything except arithmetic.
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}

def walk(node):
    """GIVEN (copy it): the function hands each child of the tree to itself, so a sum of sums works."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](walk(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left, right = walk(node.left), walk(node.right)
        if type(node.op) is ast.Pow and (abs(right) > 64 or abs(left) > 1e6):
            raise ValueError("exponent too large; keep ** small")
        return OPS[type(node.op)](left, right)
    raise ValueError(f"not allowed here: {type(node).__name__}")

def calc(expression):
    tree = ast.parse(expression, mode="eval")
    value = walk(tree.body)
    return round(value, 10) if isinstance(value, float) else value

for text in ["0.00144 * 250", "138 / 1117 * 100", "2 ** 10", "-(3 + 4) * 2",
             "__import__('os').getcwd()", "'a' * 3", "True + True", "2 ** 10 ** 10", "1 +"]:
    try:
        print(f"{text:28s} -> {calc(text)}")
    except Exception as e:
        print(f"{text:28s} -> {type(e).__name__}: {e}")
print("agrees with the kit's calculate:", [str(calc(t)) == toyagent.calculate(t) for t in ["0.00144 * 250", "138 / 1117 * 100", "2 ** 10"]])
```

```text
0.00144 * 250                -> 0.36
138 / 1117 * 100             -> 12.3545210385
2 ** 10                      -> 1024
-(3 + 4) * 2                 -> -14
__import__('os').getcwd()    -> ValueError: not allowed here: Call
'a' * 3                      -> ValueError: not allowed here: Constant
True + True                  -> ValueError: not allowed here: Constant
2 ** 10 ** 10                -> ValueError: exponent too large; keep ** small
1 +                          -> SyntaxError: invalid syntax (<unknown>, line 1)
agrees with the kit's calculate: [True, True, True]
```

Four work, four are a `ValueError`, and one is a `SyntaxError` (the text is not even an expression). So the `except` must catch **more than `ValueError`**. The loop in the kit does exactly this around every tool. The float `0.00144 * 250` is really `0.36000000000000004` inside Python, so `calc` rounds floats to 10 places, as the kit does.

The idea to keep: the set of things the text can make happen is exactly the set you wrote in `OPS`. With `eval`, the text decides.

---

## 5. The sandbox test: resolve first, compare second

`write_file` is the dangerous tool, so it may only touch one folder, `sandbox/`. **Predict the `inside:` column before you run it**: six names, each `True` or `False`. The folder `sandbox` is made for you if it is missing (`mkdir`, as in Week 26's set-up; you do not need to understand it).

The root is resolved once, at the top. `resolved(root, filename)` says where a name *really* points; `inside` asks if that is at or below the root.

```python
# sandbox_check.py - resolve first, compare second.
ROOT = Path("sandbox").resolve()
ROOT.mkdir(exist_ok=True)

def resolved(root, filename):
    return (root / filename).resolve()

def inside(root, filename):
    return resolved(root, filename).is_relative_to(root)

for name in ["report.md", "sub/a.md", "notes/../report.md", "../escape.md", "a/../../escape.md", "/etc/passwd"]:
    where = str(resolved(ROOT, name)).replace(str(ROOT), "<ROOT>") if inside(ROOT, name) else "(outside the sandbox)"
    print(f"{name:20s} -> {where:24s} inside: {inside(ROOT, name)}")
```

```text
report.md            -> <ROOT>/report.md         inside: True
sub/a.md             -> <ROOT>/sub/a.md          inside: True
notes/../report.md   -> <ROOT>/report.md         inside: True
../escape.md         -> (outside the sandbox)    inside: False
a/../../escape.md    -> (outside the sandbox)    inside: False
/etc/passwd          -> (outside the sandbox)    inside: False
```

`..` means "up one folder". In `notes/../report.md` the `notes` is cancelled by the `..` straight after it, so the file lands in the root: `notes` does not even have to exist. `/etc/passwd` is an absolute path, so joining it to the root throws the root away. Note that `sub/a.md` is *inside*, but the folder `sub` does not exist: that is a different problem, and the worked run in section 8 meets it.

Say the rule out loud: **resolve first, compare second.**

---

## 6. Check the arguments before the tool runs

The contract lists each argument and its type. `validate_args` reads the contract and returns a **list of problems** (an empty list means fine), so the model is told *every* problem at once, in words. `TYPES` turns the contract's words into Python types. You fill in the `isinstance` line; the `or isinstance(value, bool)` part is there for the trap from section 1.

```python
# validate.py - check the arguments BEFORE the tool runs.
TYPES = {"string": str, "integer": int}
SPEC = {s["name"]: s for s in specs}

def validate_args(name, args):
    if name not in SPEC:
        return [f"no tool named '{name}'"]
    schema = SPEC[name]["input_schema"]
    problems = []
    for key in schema["required"]:
        if key not in args:
            problems.append(f"missing '{key}'")
    for key, value in args.items():
        if key not in schema["properties"]:
            problems.append(f"unknown argument '{key}'")
            continue
        want = schema["properties"][key]["type"]
        if not isinstance(value, TYPES[want]) or isinstance(value, bool):
            problems.append(f"'{key}' must be {want}, got {type(value).__name__}")
    return problems

print(validate_args("calculate", {"expression": "2 + 2"}))
print(validate_args("calculate", {}))
print(validate_args("calculate", {"expression": 4}))
print(validate_args("search_notes", {"query": "dropout", "k": "3"}))
print(validate_args("search_notes", {"query": "dropout", "k": True}))
print(validate_args("write_file", {"filename": "a.md", "content": "hi", "mode": "w"}))
print(validate_args("delete_everything", {}))
```

```text
[]
["missing 'expression'"]
["'expression' must be string, got int"]
["'k' must be integer, got str"]
["'k' must be integer, got bool"]
["unknown argument 'mode'"]
["no tool named 'delete_everything'"]
```

Look at the fifth line. Python says a `bool` is an `int`. Our contract says "integer" and means a count. Both are right in their own world, so the check has to say which one it means.

---

## 7. The timeout: stop waiting, not stop working

A tool that never returns would freeze the whole loop. So the tool runs in another thread, and the loop waits for it for a limited time. On Python 3.10 the exception for "too slow" is `concurrent.futures.TimeoutError` and *not* the built-in `TimeoutError`, so the block imports it with a new name, `TooSlow`.

The slow tool is `toyagent.FlakyBackend(fn, latency=1.0)`: a wrapper that **sleeps** one second before calling `fn`. **That is a simulated delay**, not a real slow service.

```python
# timeout.py - run the tool in another thread, and stop WAITING for it after a few seconds.
from concurrent.futures import ThreadPoolExecutor, TimeoutError as TooSlow
pool = ThreadPoolExecutor(max_workers=2)

def call_with_timeout(fn, seconds, **kwargs):
    future = pool.submit(fn, **kwargs)
    try:
        return future.result(timeout=seconds)
    except TooSlow:
        return f"Error: timed out after {seconds} s"

slow_calc = toyagent.FlakyBackend(toyagent.calculate, latency=1.0)    # SIMULATED delay: it sleeps 1 second, then works
for seconds in [3.0, 0.2]:
    t0 = time.time()
    out = call_with_timeout(slow_calc, seconds, expression="6 * 7")
    print(f"timeout {seconds}: {out!r}  (waited {time.time() - t0:.1f} s)")
```

```text
timeout 3.0: '42'  (waited 1.0 s)
timeout 0.2: 'Error: timed out after 0.2 s'  (waited 0.2 s)
```

With patience the answer arrives after a second. Without it the call gives up after `0.2 s`. **But has the slow tool stopped?** No. It is still asleep in its thread for another 0.8 seconds. A thread cannot be killed from outside. **A timeout stops the waiting; it does not stop the work.** For a tool that writes a file, that means the write may still land after you gave up. (Real systems run tools in a separate *process* they can end. That is beyond this course.)

---

## 8. The six fences, with no model

This is the centre of the week. You build a **registry** (the table of tools your code will run) with three entries, then send **eight scripted requests** through the kit's loop, `toyagent.run_agent`. Each request meets one fence. The "model" is a script that never reads a word, so a fence that stops a request is a fence that works **with the model unplugged**.

- `once(name, args)` is a two-step plan: make that one call, then say `ok`.
- `forever` is a plan that calls the calculator 50 times.
- `requires_confirmation=True` marks `write_file` as needing a human. In `runs`, `confirm=lambda name, args: False` is "the human says no", and `auto_approve=True` is "skip the human" (fine here, where we want the *sandbox* to be the thing that answers).
- The slow tool sleeps 0.5 s but has a limit of 0.1 s.

**Before you run it, predict the `stop=` column for row 3.** Is it `PermissionError`?

```python
# fences.py - all six fences, fired from plain Python. The "model" is a scripted plan: a STAND-IN, NOT A MODEL.
box = toyagent.Sandbox(root=ROOT)
reg = toyagent.ToolRegistry()
reg.register("calculate", toyagent.calculate, timeout=2.0)
reg.register("slow", toyagent.FlakyBackend(toyagent.calculate, latency=0.5), timeout=0.1)
reg.register("write_file", box.write_file, timeout=5.0, requires_confirmation=True)

def once(name, args):
    return toyagent.ScriptedModel([("", [(name, args)]), ("ok", [])])

forever = toyagent.ScriptedModel([("", [("calculate", {"expression": "1 + 1"})])] * 50)
runs = [
    ("1 max_iterations", dict(model=forever, max_iterations=3)),
    ("2 budget_usd", dict(model=forever, max_iterations=50, budget_usd=0.0004)),
    ("3 sandbox", dict(model=once("write_file", {"filename": "../escape.md", "content": "x"}), auto_approve=True)),
    ("4 timeout", dict(model=once("slow", {"expression": "1 + 1"}))),
    ("5 allowlist", dict(model=once("delete_everything", {}))),
    ("6 confirmation", dict(model=once("write_file", {"filename": "h.md", "content": "x"}), confirm=lambda name, args: False)),
    ("  bad arguments", dict(model=once("calculate", {}))),
    ("  hostile calculate", dict(model=once("calculate", {"expression": "__import__('os').getcwd()"}))),
]
for label, kw in runs:
    r = toyagent.run_agent("q", reg, specs, **kw)
    calls = [e for e in r["trace"] if e["event"] == "tool_call"]
    note = calls[0]["result_preview"][:59] if calls else ""
    print(f"{label:18s} stop={r['stop']:17s} iterations={r['iterations']:2d}  {note}")
print("files the sandbox holds:", sorted(p.name for p in ROOT.iterdir()), "| write attempts logged:", len(box.attempts))
print("escape.md exists outside the sandbox:", (ROOT.parent / "escape.md").exists())
```

```text
1 max_iterations   stop=max_iterations    iterations= 3  2
2 budget_usd       stop=budget_exhausted  iterations= 2  2
3 sandbox          stop=end_turn          iterations= 2  Error: PermissionError: refused: '../escape.md' resolves to
4 timeout          stop=end_turn          iterations= 2  Error: 'slow' timed out.
5 allowlist        stop=end_turn          iterations= 2  Error: no tool named 'delete_everything'.
6 confirmation     stop=end_turn          iterations= 2  Error: the human declined this action.
  bad arguments    stop=end_turn          iterations= 2  Error: bad arguments for 'calculate': calculate() missing 1
  hostile calculate stop=end_turn          iterations= 2  Error: ValueError: unsupported expression element: Call
files the sandbox holds: [] | write attempts logged: 1
escape.md exists outside the sandbox: False
```

How to read it:

- **Only the first two fences change the stop reason.** The other four show `end_turn`, because the model was handed an error, "read" it (the script says `ok`) and finished. **The stop reason is not the fence's name; the `Error:` text is.** A stop reason of `end_turn` does not mean the task worked.
- Row 2 stops after 2 turns, not 1: the loop checks spend *before* each turn, so the turn that crosses the budget still happens. A budget is not a hard cap. It stops one call late.
- The last two rows are not numbered fences. The missing argument comes from Python itself (the loop turns the `TypeError` into text), and the hostile text is refused by the calculator's own whitelist. The kit's message says `unsupported expression element: Call`; yours said `not allowed here: Call`. Same idea.
- The last two lines are the point: we asked for `../escape.md`, and **nothing happened**. The sandbox holds no files, and nothing was written outside it. That is what a fence looks like.

---

## 9. The worked run: five turns and a bill

Now one real task through the same loop: *look up what one extraction call costs in the notes, work out 250 calls, and save a one-line summary.* The scripted plan is `toyagent.worked_plan()`: **search, calculate, write (to a folder that does not exist), write (flat), answer.** The failed write at turn 3 is in the plan **on purpose**, so that the trace shows an error being read and recovered from. **The recovery is the plan's, not a model's.** A real model might fix the path, or might repeat the mistake until a fence stops it. We cannot measure that here, and that is exactly why the fences exist.

`toyagent.build_registry(box2, index, titles)` is the kit's three-tool registry (with `write_file` flagged for confirmation). `approve` is a function that prints the request and says yes, so the run needs no typing. In your own experiments you can leave `confirm` out: the kit's default asks you to type `y` or `n`, and end-of-input counts as "no".

```python
# run_worked.py - the worked five-turn task, through the kit's loop. The plan is scripted: STAND-IN, NOT A MODEL.
box2 = toyagent.Sandbox(root=ROOT)
reg2 = toyagent.build_registry(box2, index, titles)

def approve(name, args):
    print(f"   CONFIRM {name}: filename={args['filename']!r}  (a person types y; this stand-in says yes)")
    return True

r = toyagent.run_agent("What does one extraction call cost per my notebook? Work out 250 calls and save a one-line summary to extraction-250.md.",
                       reg2, specs, toyagent.ScriptedModel(toyagent.worked_plan()), confirm=approve)
for e in r["trace"]:
    if e["event"] == "model_turn":
        print(f"turn {e['iteration']}  in={e['in_tok']:4d} out={e['out_tok']:3d}  ${e['cost']:.6f}  calls={e['calls']}")
    elif e["event"] == "tool_call":
        print(f"   {e['tool']:13s} {'ERR' if e['is_error'] else 'ok '} {e['result_preview'][:70]!r}")
print("stop:", r["stop"], "| iterations:", r["iterations"], f"| spend: ${r['spend']:.6f}", "| label:", r["label"])
print("answer:", r["answer"])
print("file on disk:", (ROOT / "extraction-250.md").read_text())
```

```text
   CONFIRM write_file: filename='reports/extraction-250.md'  (a person types y; this stand-in says yes)
   CONFIRM write_file: filename='extraction-250.md'  (a person types y; this stand-in says yes)
turn 1  in= 247 out= 28  $0.000387  calls=['search_notes']
   search_notes  ok  '[note 14] (similarity 0.322) 2026-08-14 - Cost accounting\nOne extracti'
turn 2  in= 415 out= 10  $0.000465  calls=['calculate']
   calculate     ok  '0.36'
turn 3  in= 448 out= 25  $0.000573  calls=['write_file']
   write_file    ERR "Error: ValueError: directory 'reports' does not exist in the sandbox. "
turn 4  in= 519 out= 19  $0.000614  calls=['write_file']
   write_file    ok  'wrote 47 bytes to extraction-250.md'
turn 5  in= 566 out= 20  $0.000666  calls=[]
stop: end_turn | iterations: 5 | spend: $0.002705 | label: stand-in, not a model
answer: One extraction call costs about $0.00144 [note 14]. 250 calls cost $0.36. Saved to extraction-250.md.
file on disk: 250 extraction calls = $0.36 (source: note 14).
```

(The two `CONFIRM` lines print first because `approve` runs *during* the loop, while the trace is printed only afterwards. Read the trace below them.)

Walk down it. Turn 1 asks the notes and gets note 14. Turn 2 calculates `0.36`. Turn 3 tries `reports/extraction-250.md`; the folder is missing, so the tool returns a plain-English error (`ERR`), which is just a result. Turn 4 writes `extraction-250.md` flat and it works. Turn 5 answers in words, and the loop stops.

**Two warnings.** The citation `[note 14]` and the number `$0.36` look right, and Week 26 taught you what a valid citation does and does not prove: the answer still needs *your* check against note 14. And this is one task with one path. It says nothing about how often an agent succeeds.

### Why a long task costs more than it looks

Each turn the model is sent **everything so far**: the instructions, the contracts, the question, every earlier message and every tool result. So the input of each turn is the previous turn's input plus whatever happened in between.

```python
# growth.py - why a long task gets expensive: every turn re-sends the whole conversation.
ins = r["in_tokens"]
diffs = [b - a for a, b in zip(ins, ins[1:])]
print("input tokens per turn:", ins)
print("growth each turn     :", diffs)
print("total input tokens   :", sum(ins), "| if the first turn's size had been re-used every time:", ins[0] * len(ins))
print("output tokens per turn:", r["out_tokens"], "total", sum(r["out_tokens"]))
print("tool calls made:", [(c["tool"], "ERR" if c["is_error"] else "ok") for c in r["tool_calls"]])
```

```text
input tokens per turn: [247, 415, 448, 519, 566]
growth each turn     : [168, 33, 71, 47]
total input tokens   : 2195 | if the first turn's size had been re-used every time: 1235
output tokens per turn: [28, 10, 25, 19, 20] total 102
tool calls made: [('search_notes', 'ok'), ('calculate', 'ok'), ('write_file', 'ERR'), ('write_file', 'ok')]
```

The big first step, `168`, is turn 1's search result arriving: two notes of text. Turn 5 costs more than turn 2 even though the "model" says about the same number of words, because turn 5 is sent the whole conversation again.

**The bill, by hand.** The price is 1.00 per million tokens in and 5.00 per million out. Turn 1: `247 × 1.00 + 28 × 5.00 = 247 + 140 = 387` millionths of a dollar, which is `$0.000387`, the number in the trace. For the whole run, add the five "in" numbers and the five "out" numbers and price them; you should land on the printed `spend`. You do that sum yourself on workbook page 28.3.

If every step added about the same number of tokens `g`, the inputs would be `b, b + g, b + 2g, …`, and the growth part of the total would be `g × (1 + 2 + … + (n − 1))`. That grows like `n²/2`: **doubling the number of steps a little more than triples the bill for the history.** Real steps are not all the same size (`168, 33, 71, 47` here), so this is a *shape*, not a prediction. Tokens here are the kit's own count and the dollars are illustrative; the shape survives a real tokenizer, the values do not.

---

## 🎲 Your Turn

### Which Fence?

Do this on paper, **before** anything else in your workbook. Six fences stand between "the model asked" and "something happened":

`1` turns cap · `2` money cap · `3` sandbox (folder, suffix, size) · `4` timeout · `5` allowlist · `6` a human says yes

A request may also be stopped by **the tool's own check (0)**, or it may be fine (**none**). Name one for each. The model has been told to be careful.

| | Request |
|:--:|---|
| A | `calculate("2 + 2")` |
| B | `calculate("__import__('os').getcwd()")` |
| C | `write_file("../notes.md", "hi")` (the human said yes) |
| D | `write_file("run.sh", "hi")` (the human said yes) |
| E | `delete_everything()` (no such tool exists) |
| F | a plan that calls `calculate("1 + 1")` over and over, forever |
| G | `write_file("plan.md", "hi")` (the human said no) |
| H | a tool that sleeps 30 seconds; the limit is 10 |
| I | `write_file("sub/a.md", "hi")` (there is no folder `sub`) |
| J | `write_file("big.md", <25,000 letters>)` (the human said yes) |

Then answer three questions.

1. Which **one** of A to J should not be stopped at all?
2. Which **one** is stopped by a check that is not a security fence, and what does the model get back?
3. The model was told "be careful". Which of the six fences read that sentence?

---

## 🔬 Break It On Purpose

**DELIBERATE, and in a scratch session only.** This is the calculator *without* the whitelist. The text is harmless on purpose: it only asks which folder we are in. Predict what it prints, then run it.

```python
# bad_eval.py - DELIBERATE: a "calculator" built on eval(). Run this alone, in a scratch session.
print(eval("2 + 3 * 4"))
print(eval("__import__('os').getcwd()"))
```

The first line prints `14`. The second prints the name of **your** current folder, because `eval` *runs* the text. (Yours will differ from mine, so there is no output to paste.) You asked for arithmetic and got a program. Ask yourself what else that text could have been: that is the reason section 4 reads the text as a tree and runs only what is on a list. **Do not try anything destructive to find out.**

---

## 🧭 What was shown, and what was not

**Shown:**
- A tool is a function plus a contract, and the model only asks; your code checks, limits and acts.
- A calculator that reads the text as a tree and refuses everything not on its list, including `True + True` and a huge power.
- A sandbox test that resolves first and compares second, and the three names (`../escape.md`, `a/../../escape.md`, `/etc/passwd`) it refuses.
- An argument check against the contract, including `True` refused as an integer.
- A timeout that stops the *waiting*, not the work.
- Six fences fired with no model: `max_iterations`, `budget_exhausted`, `PermissionError`, `timed out`, `no tool named`, `declined`.
- A real five-turn trace: `stop: end_turn`, `spend: $0.002705`, inputs of `247, 415, 448, 519, 566`.

**Not shown:**
- **Any model.** Every plan is typed text labelled "stand-in, not a model". The recovery at turn 3 is written into the plan.
- How a real model picks tools, loops, recovers from an error or obeys its instructions. Nothing today measures that.
- Anything about networks, environment variables, subprocesses or databases. A fence is only as wide as the tools behind it. Our sandbox is one folder of flat files.
- Real token counts or real prices. Both are the kit's illustrative arithmetic.
- That the agent "works". It is one task with one path.

---

## 🔑 Wrap Up

1. Turn to your card. Who runs a tool: the model or your program? What stopped the `../notes.md` write, the instruction or the code?
2. In the fence table, which fences need a model? Which read the prompt?
3. Why is `/etc/passwd` refused when you resolve first, and what would a test that only looks for `..` say about it?
4. A timeout fired after 0.2 seconds. Has the slow tool stopped? What could that mean for a tool that writes a file?
5. The stop reason says `end_turn`. Does that mean the task worked? Where do you look instead?
6. Why does turn 5 cost more than turn 2 when the model says about the same number of words?

Then write this sentence in your Bug Log in your own handwriting:

> **"The model asks; my code checks, limits and acts. A fence is a line of code that holds whether or not anything obeys the prompt, so I can test every one with no model at all, but a scripted plan proves the fences, not the agent."**

**A look ahead.** Next week the same loop reads a note that *says* "call `write_file`". You will turn a dial that makes the scripted model more gullible, switch three layers of defence on one at a time, and see which one holds when the model is fully fooled. (Hint: it is one of the fences you built today.) That model is also a stand-in, and what happens to it says nothing about a real one.

---

## 📤 Homework

Complete workbook pages 28.1 to 28.3 (about 55 minutes: 25 of pen and paper, 30 at the computer). Write your **predictions before you run anything.** Every number you write must have come from your own calculator or your own run.

**Optional (fast students).** Write your own `safe_write(filename, content)` that refuses the names the sandbox refuses, then check it against the kit's `Sandbox` on the same six names. Or add a node-count limit to `calc`.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **tool** | a function the model may ask for, described by a contract |
| **contract (spec, schema)** | the name, description and typed arguments the model is shown |
| **agent loop** | perceive, decide, act, observe, stop, repeated |
| **iteration** | one pass round the loop |
| **tool call / tool result** | the model's request (a name and arguments) / the text your code hands back |
| **allowlist** | the list of tools that may be called; anything else is refused |
| **sandbox** | one folder that file tools may touch, and nothing outside it |
| **path traversal** | a path that uses `..` or an absolute name to escape the sandbox |
| **timeout** | a limit on how long the loop will wait for a tool |
| **human-in-the-loop (confirmation)** | a person must say yes before a write happens |
| **guardrail / fence** | a line of code that limits what a request can do, whatever the prompt says |
| **trace** | the recorded list of turns and tool calls, with tokens and cost |
| **stop reason** | why the loop ended: `end_turn`, `max_iterations` or `budget_exhausted` |
| **whitelist** | a list of what is allowed, with everything else refused |
| **stand-in** | a script imitating a model; measures nothing about a real one |

---

[⬅ Week 27](week-27.md) · [Course Home](../README.md) · [Week 29 ➡](week-29.md) · [Workbook](../workbook/week-28.md)
