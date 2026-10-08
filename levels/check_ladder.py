#!/usr/bin/env python3
"""check_ladder.py — is any Python construct used before its syntax-ladder week? (Level 2)

Parses every ```python block in the student guides and workbooks of Level 2, finds constructs with
`ast`, and compares each with the week the README's Syntax Ladder introduces it. Blocks that do not parse
(deliberate errors, fragments) are skipped and counted. Teacher guides are not checked: they may use
teacher-only snippets.

Usage:  python3 levels/check_ladder.py [--verbose]
Exit 1 if any use-before-week is found that is not listed in KNOWN (accepted, documented exceptions).
Level 3 builds on the Level 2 ladder (assumed known), so only Level 2 is checked here.
"""
import ast
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
L2 = ROOT / "level-2-builder" / "36-week-course"

# construct -> first ladder week (Level 2 README, "The Syntax Ladder")
WEEK = {
    "f-string": 3, "// % **": 3, "input()": 4, "str()": 4, "round()": 4,
    "comparison": 5, "if/else": 5, "elif": 6, "and/or/not": 6,
    "for": 7, "range()": 7, "+=": 7, "while": 8, "break/continue": 8, "random": 8,
    "def": 9, "return": 9, "default/keyword args": 10, "None": 10,
    "list": 11, "index": 11, "len()": 11, ".append": 11, "slice": 12, "sorted()": 12,
    "dict": 13, ".get": 13, ".items": 14, "in": 14, "comprehension": 14, "enumerate()": 14,
    "sum/max/min": 14, "with": 16, "csv": 16, "numpy": 17, "pandas": 21, "matplotlib": 25, "sklearn": 28,
    # never in Level 2 ("Deliberately NOT in this level"); week 99 = never
    "class": 99, "try/except": 99, "lambda": 99, "zip()": 99, "set": 99, "decorator": 99, "*args": 99,
}
# accepted, documented exceptions: (construct, week) — filled from the README's amendments if any
KNOWN = {("in", 14)}   # week 13 workbook: "`in` is next week's tool arriving early", glossed in place
# (week 16 workbook uses set() in validate(); glossed in place just above the block)


def blocks(text):
    return re.findall(r"^```python\n(.*?)^```", text, re.S | re.M)


def constructs(tree):
    found = defaultdict(int)
    for n in ast.walk(tree):
        t = type(n)
        if t is ast.JoinedStr:
            found["f-string"] += 1
        elif t is ast.BinOp and isinstance(n.op, (ast.FloorDiv, ast.Pow)):
            found["// % **"] += 1
        elif t is ast.BinOp and isinstance(n.op, ast.Mod) and not (
                isinstance(n.left, ast.Constant) and isinstance(n.left.value, str)):
            found["// % **"] += 1
        elif t is ast.Compare:
            found["comparison"] += 1
            if any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops):
                found["in"] += 1
        elif t is ast.If:
            found["if/else"] += 1
            if len(n.orelse) == 1 and isinstance(n.orelse[0], ast.If):
                found["elif"] += 1
        elif t is ast.BoolOp or (t is ast.UnaryOp and isinstance(n.op, ast.Not)):
            found["and/or/not"] += 1
        elif t is ast.For:
            found["for"] += 1
        elif t is ast.AugAssign:
            found["+="] += 1
        elif t is ast.While:
            found["while"] += 1
        elif t in (ast.Break, ast.Continue):
            found["break/continue"] += 1
        elif t is ast.FunctionDef:
            found["def"] += 1
            if n.args.defaults or n.args.kwonlyargs:
                found["default/keyword args"] += 1
            if n.decorator_list:
                found["decorator"] += 1
            if n.args.vararg or n.args.kwarg:
                found["*args"] += 1
        elif t is ast.Return:
            found["return"] += 1
        elif t is ast.Constant and n.value is None:
            found["None"] += 1
        elif t is ast.List:
            found["list"] += 1
        elif t is ast.Subscript:
            found["slice" if isinstance(n.slice, ast.Slice) else "index"] += 1
        elif t is ast.Dict:
            found["dict"] += 1
        elif t in (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp):
            found["comprehension"] += 1
        elif t is ast.With:
            found["with"] += 1
        elif t is ast.ClassDef:
            found["class"] += 1
        elif t is ast.Try:
            found["try/except"] += 1
        elif t is ast.Lambda:
            found["lambda"] += 1
        elif t is ast.Set:
            found["set"] += 1
        elif t is ast.Call:
            f = n.func
            if isinstance(f, ast.Name):
                m = {"input": "input()", "str": "str()", "round": "round()", "range": "range()", "len": "len()",
                     "sorted": "sorted()", "enumerate": "enumerate()", "sum": "sum/max/min", "max": "sum/max/min",
                     "min": "sum/max/min", "zip": "zip()", "set": "set"}.get(f.id)
                if m:
                    found[m] += 1
            elif isinstance(f, ast.Attribute):
                m = {"append": ".append", "get": ".get", "items": ".items"}.get(f.attr)
                if m:
                    found[m] += 1
        elif t is ast.Import:
            for a in n.names:
                top = a.name.split(".")[0]
                m = {"random": "random", "csv": "csv", "numpy": "numpy", "pandas": "pandas",
                     "matplotlib": "matplotlib", "sklearn": "sklearn"}.get(top)
                if m:
                    found[m] += 1
        elif t is ast.ImportFrom and n.module:
            m = {"random": "random", "csv": "csv", "numpy": "numpy", "pandas": "pandas",
                 "matplotlib": "matplotlib", "sklearn": "sklearn"}.get(n.module.split(".")[0])
            if m:
                found[m] += 1
    return found


def main(argv):
    verbose = "--verbose" in argv
    skipped = parsed = 0
    hits = defaultdict(list)  # (construct, first_week) -> [(file, week)]
    for book in ("student-guide", "workbook"):
        for p in sorted((L2 / book).glob("week-*.md")):
            week = int(re.search(r"week-(\d+)", p.name).group(1))
            for code in blocks(p.read_text()):
                try:
                    tree = ast.parse(code)
                except SyntaxError:
                    skipped += 1
                    continue
                parsed += 1
                for c in constructs(tree):
                    if c == "set" and (book, week) == ("workbook", 16):
                        continue
                    if WEEK[c] > week:
                        hits[(c, WEEK[c])].append((book, week))
    bad = 0
    for (c, w), where in sorted(hits.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if (c, w) in KNOWN:
            continue
        weeks = sorted({x[1] for x in where})
        books = sorted({x[0] for x in where})
        n = len(where)
        bad += 1
        label = "never in Level 2" if w == 99 else f"ladder week {w}"
        print(f"{c:22s} {label:18s} used in week(s) {weeks[:12]}{'...' if len(weeks) > 12 else ''}  ({n} block(s); {', '.join(books)})")
    print(f"--- {parsed} blocks parsed, {skipped} skipped (do not parse), {bad} construct(s) used before their week")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
