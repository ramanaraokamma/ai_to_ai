#!/usr/bin/env python3
"""polish_check.py — the content-safety gate for the presentation polish pass.

Compares each given markdown file (working copy) with its committed version and enforces the
invariants in levels/PRESENTATION-SPEC.md:

  1. every fenced code block is byte-identical and in the same order (code, outputs, tracebacks);
  2. the multiset of link / image targets outside fences is unchanged;
  3. the multiset of numbers in the prose outside fences is unchanged (leading list numbers ignored);
  4. the H2 headings keep the same count (reworded is fine) — a different count is a WARNING;
  5. hygiene: one H1, no skipped heading level, balanced + language-tagged fences, no tabs,
     no trailing spaces, no 3+ blank lines.

Usage:   python3 levels/polish_check.py FILE [FILE ...]        (baseline: git HEAD)
         python3 levels/polish_check.py --base REF FILE ...    (baseline: any git ref)
Prints 'OK' per clean file; exit status 1 if any file has a FAIL.
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})([^\n]*)$")


def split(text):
    """Return (prose_lines, blocks, fence_problems). blocks = [(info, body)]."""
    prose, blocks, problems = [], [], []
    inblock, mark, info, body, start = False, "", "", [], 0
    for n, line in enumerate(text.split("\n"), 1):
        m = FENCE.match(line)
        if not inblock:
            if m:
                inblock, mark, info, body, start = True, m.group(2), m.group(3).strip(), [], n
                if not info:
                    problems.append(f"line {n}: fenced block has no language tag")
            else:
                prose.append((n, line))
        else:
            if m and m.group(2)[0] == mark[0] and len(m.group(2)) >= len(mark) and not m.group(3).strip():
                blocks.append((info, "\n".join(body)))
                inblock = False
            else:
                body.append(line)
    if inblock:
        problems.append(f"line {start}: fenced block never closed")
    return prose, blocks, problems


def numbers(prose):
    c = Counter()
    for _, line in prose:
        line = re.sub(r"^\s*\d+[.)]\s", "", line)  # ordered-list markers do not count
        line = re.sub(r"\]\([^)]*\)", "]", line)   # link targets are checked separately
        line = re.sub(r"[\w./-]*\d[\w./-]*\.(?:py|md|txt|csv|svg|json|jsonl|joblib|npy|pt)\b", "FILE", line)  # digits in file names
        c.update(re.findall(r"\d+(?:[.,]\d+)?", line))
    return c


def links(prose):
    c = Counter()
    for _, line in prose:
        c.update(re.findall(r"\]\(([^)\s]+)", line))
    return c


def base_text(path, ref):
    try:
        return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True,
                              check=True, cwd=Path(path).resolve().parent).stdout
    except Exception:
        return None


def rel_to_repo(path):
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         cwd=Path(path).resolve().parent).stdout.strip()
    return str(Path(path).resolve().relative_to(top))


def check(path, ref):
    fails, warns = [], []
    new = Path(path).read_text()
    prose, blocks, fp = split(new)
    fails += fp
    # ---- hygiene
    h1 = [l for _, l in prose if re.match(r"^# ", l)]
    if len(h1) != 1:
        fails.append(f"{len(h1)} H1 headings (need exactly 1)")
    last = 0
    for n, l in prose:
        m = re.match(r"^(#{1,6}) ", l)
        if m:
            lv = len(m.group(1))
            if last and lv > last + 1:
                fails.append(f"line {n}: heading jumps from H{last} to H{lv}")
            last = lv
    for n, l in prose:
        if "\t" in l:
            fails.append(f"line {n}: tab character in prose")
            break
    for n, l in prose:
        if l != l.rstrip():
            fails.append(f"line {n}: trailing whitespace")
            break
    blank, prev = 0, 0
    for n, l in prose:                       # only prose lines count; blank runs inside fences are code
        blank = blank + 1 if (not l.strip() and n == prev + 1) or (not l.strip() and blank == 0) else (1 if not l.strip() else 0)
        prev = n
        if blank >= 3:
            fails.append(f"line {n}: three or more consecutive blank lines")
            break
    # ---- against baseline
    old = base_text(rel_to_repo(path), ref)
    if old is None:
        warns.append("no committed baseline; invariants not compared")
        return fails, warns
    oprose, oblocks, _ = split(old)
    if len(blocks) != len(oblocks):
        fails.append(f"code blocks: {len(oblocks)} before, {len(blocks)} after")
    for i, (a, b) in enumerate(zip(oblocks, blocks)):
        if a[1] != b[1]:
            fails.append(f"code block #{i + 1} ({a[0] or 'untagged'}) body changed")
            break
        if a[0] and a[0] != b[0]:          # an untagged block may gain a tag; a tag may not change
            fails.append(f"code block #{i + 1} language tag changed {a[0]!r} -> {b[0]!r}")
            break
    ln, lo = links(prose), links(oprose)
    if ln != lo:
        fails.append("link/image targets changed: +%s -%s" % (dict(ln - lo), dict(lo - ln)))
    nn, no = numbers(prose), numbers(oprose)
    if nn != no:
        fails.append("numbers in prose changed: added %s, removed %s"
                     % (dict(nn - no), dict(no - nn)))
    h2n = sum(1 for _, l in prose if l.startswith("## "))
    h2o = sum(1 for _, l in oprose if l.startswith("## "))
    if h2n != h2o:
        warns.append(f"H2 sections: {h2o} before, {h2n} after")
    if "student-guide" in path or "workbook" in path:
        tn = sum(1 for _, l in prose if "teacher-guide/" in l)
        to = sum(1 for _, l in oprose if "teacher-guide/" in l)
        if tn > to:
            fails.append("student-facing file gained a reference to teacher-guide/")
    return fails, warns


def main(argv):
    ref = "HEAD"
    if argv and argv[0] == "--base":
        ref, argv = argv[1], argv[2:]
    if not argv:
        print(__doc__)
        return 2
    bad = 0
    for p in argv:
        fails, warns = check(p, ref)
        if fails:
            bad += 1
            print(f"FAIL {p}")
            for f in fails:
                print("   -", f)
        else:
            print(f"OK   {p}")
        for w in warns:
            print("   ~", w)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
