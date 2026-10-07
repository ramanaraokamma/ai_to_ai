#!/usr/bin/env python3
"""check_structure.py — structural checks for a taught level (run from anywhere).

    python3 levels/check_structure.py level-4-innovator [level-3-engineer ...]

Per level: 36 weeks x 3 books present and not thin (<150 lines); local markdown links and image
embeds outside code fences resolve; every figures/*.svg satisfies the figure contract (valid XML,
viewBox, no width/height on the root, role="img", <title>, <desc>, no banned constructs); every
fig-*.svg is embedded at least once. Exit status 1 if anything is wrong.
"""
import re
import sys
import xml.dom.minidom
from pathlib import Path

BANNED = re.compile(r"<image|http|@font-face|<script|<foreignObject")


def check(level):
    root = Path(__file__).resolve().parent / level / "36-week-course"
    bad = []
    md = [p for p in root.rglob("*.md") if "_generator" not in p.parts and "_ledger" not in p.parts]
    for book in ("teacher-guide", "student-guide", "workbook"):
        for n in range(1, 37):
            f = root / book / f"week-{n:02d}.md"
            if not f.exists():
                bad.append(f"missing {book}/week-{n:02d}.md")
            elif sum(1 for _ in f.open()) < 150:
                bad.append(f"thin {book}/week-{n:02d}.md")
    links = 0
    for p in md:
        t = re.sub(r"```.*?```", "", p.read_text(), flags=re.S)
        for u in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", t):
            if re.match(r"(https?:|mailto:|#)", u):
                continue
            links += 1
            f = u.split("#")[0]
            if f and not (p.parent / f).resolve().exists():
                bad.append(f"broken link {p.relative_to(root)} -> {u}")
    svgs = sorted((root / "figures").glob("*.svg"))
    for s in svgs:
        t = s.read_text()
        try:
            xml.dom.minidom.parseString(t)
        except Exception as e:
            bad.append(f"invalid XML {s.name}: {e}")
            continue
        if s.name.startswith("_"):
            continue
        tag = re.search(r"<svg[^>]*>", t).group(0)
        for ok, what in [("viewBox" in tag, "viewBox"), (not re.search(r"\s(width|height)=", tag), "root width/height"),
                         ('role="img"' in tag, "role"), ("<title" in t, "title"), ("<desc" in t, "desc"),
                         (not BANNED.search(t.replace("http://www.w3.org/2000/svg", "")), "banned construct")]:
            if not ok:
                bad.append(f"svg {s.name}: {what}")
    refs = set()
    for p in md:
        refs |= set(re.findall(r"figures/([\w\-.]+\.svg)", p.read_text()))
    for s in svgs:
        if s.name.startswith("fig-") and s.name not in refs:
            bad.append(f"figure never embedded: {s.name}")
    print(f"{level}: {len(md)} md files, {links} local links, {len(svgs)} svgs -> {'OK' if not bad else str(len(bad)) + ' PROBLEM(S)'}")
    for b in bad[:20]:
        print("   -", b)
    return not bad


if __name__ == "__main__":
    levels = sys.argv[1:] or ["level-1-explorer", "level-2-builder", "level-3-engineer", "level-4-innovator"]
    sys.exit(0 if all([check(l) for l in levels]) else 1)
