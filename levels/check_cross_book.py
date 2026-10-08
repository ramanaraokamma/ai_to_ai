#!/usr/bin/env python3
"""check_cross_book.py — does each week's teacher guide agree with its workbook's answers?

The worst defect class in this repo was two files that disagree (teacher keys written against a workbook
layout that never shipped). Per-file audits cannot see it. This tool takes the numbers printed in each
workbook's Answers section (decimals and integers of 2+ digits, skipping years and list numbering) and
reports the share that also appear anywhere in the same week's teacher guide.

Usage:  python3 levels/check_cross_book.py [--min 0.80] [--verbose] [level-N-name ...]
Exit 1 if any week's coverage is below --min (default 0.80) or a week has no Answers section.
Coverage ~0.96 is typical; a low value means the key and the workbook probably describe different exercises.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANS = re.compile(r"^## (?:✅|✂️)?\s*(?:Answers|ANSWERS)", re.M)


def numbers(text):
    text = re.sub(r"```.*?```", lambda m: m.group(0), text, flags=re.S)   # numbers inside blocks count too
    text = re.sub(r"\]\([^)]*\)", "]", text)                               # link targets
    text = re.sub(r"[\w./-]*\d[\w./-]*\.(?:py|md|txt|csv|svg|json|png|joblib|npy|pt)\b", " ", text)
    out = set()
    for m in re.finditer(r"(?<![\w.])-?\d+(?:[.,]\d+)?(?![\w])", text):
        tok = m.group(0).replace(",", "")
        if "." in tok or len(tok.lstrip("-")) >= 2:
            if not re.fullmatch(r"(19|20)\d\d", tok):
                out.add(tok.lstrip("-"))
    return out


def main(argv):
    lo, verbose, levels = 0.80, False, []
    while argv:
        a = argv.pop(0)
        if a == "--min":
            lo = float(argv.pop(0))
        elif a == "--verbose":
            verbose = True
        else:
            levels.append(a)
    levels = levels or sorted(p.name for p in ROOT.glob("level-*"))
    bad = 0
    for lv in levels:
        base = ROOT / lv / "36-week-course"
        cov = []
        for n in range(1, 37):
            wb = (base / "workbook" / f"week-{n:02d}.md").read_text()
            tg = (base / "teacher-guide" / f"week-{n:02d}.md").read_text()
            m = ANS.search(wb)
            if not m:
                print(f"FAIL {lv} week {n}: no Answers section in workbook")
                bad += 1
                continue
            a, t = numbers(wb[m.end():]), numbers(tg)
            if not a:
                continue
            miss = sorted(a - t, key=lambda x: (len(x), x))
            c = 1 - len(miss) / len(a)
            cov.append(c)
            if c < lo:
                bad += 1
                print(f"FAIL {lv} week {n}: coverage {c:.2f} ({len(a) - len(miss)}/{len(a)}); missing e.g. {miss[:8]}")
            elif verbose:
                print(f"ok   {lv} week {n}: {c:.2f}")
        print(f"--- {lv}: mean coverage {sum(cov) / max(1, len(cov)):.3f} over {len(cov)} weeks")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
