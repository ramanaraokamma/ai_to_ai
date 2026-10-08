"""Block C12 (weeks 34, 35, 36) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W34  student-guide/week-34.md section 4 (score_case: the order of the checks), the maths section
     (s6_wobble.py: n=25, p=0.70, expected 17.5, wobble 2.29 = 0.092, one case 0.04, a six-case
     category 0.17); the blank is workbook page 34.1 Part A (five failure modes, no ranks written)
W35  student-guide/week-35.md section 4 (Spine.answer: guard, route, path; then the trace line),
     section 6 (s6_budget_check.py printout: headroom 2.21x, 2.02x, 0.97x, 1.00x); the blank is
     workbook page 35.2 Part A (four headroom rulers, nothing marked)
W36  student-guide/week-36.md section 1 (the files printed by s1_restore.py, and the week in which
     each was written), section 11 (the paper: 75 marks; A 20, B 16, C 12, D 15, E 12); the blank is
     workbook page 36.6 (the per-week grid, nothing written; the marks available per week are on the
     teacher's marking sheet and are NOT drawn)
"""
from _gen_core import *

FIGS = {}
VB = "0 0 800 400"


def fig(name, title, desc, parts, vb=VB):
    FIGS[name + ".svg"] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=376):
    return t(400, y, s, 14, MUT, "middle")


def node(x, y, w, h, lines, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, subs=None):
    """A box with a 14px head line and optional 12px muted sub lines, centred."""
    o = [rect(x, y, w, h, 8, fill, stroke, sw, dash)]
    n = 1 + len(subs or [])
    y0 = y + h / 2.0 - (n - 1) * 9
    o.append(t(x + w / 2.0, y0, lines, 14, INK, "middle", central=True))
    for i, s in enumerate(subs or []):
        o.append(t(x + w / 2.0, y0 + 18 * (i + 1), s, 12, MUT, "middle", central=True))
    return "\n  ".join(o)


# ---------------------------------------------------------------- W34-4  the order the scorer checks
def w34_4():
    o = [ctitle("The scorer checks in a fixed order")]
    names = [("must refuse?", "yes: stop here"), ("refused?", "when it should not"),
             ("needles?", "whole tokens"), ("citation?", "if the case wants one"),
             ("cited = fetched?", "notes it retrieved")]
    below = [("pass only if", "it refused"), ("FAIL: refused an", "answerable question"),
             ("FAIL: a needle", "is missing"), ("FAIL: no", "citation given"),
             ("FAIL: cited a note", "never retrieved")]
    x0, w, gap, y, h = 24, 116, 20, 96, 76
    for i, (a, b) in enumerate(names):
        x = x0 + i * (w + gap)
        if i < 4:
            o.append(arrow(x + w + 1, y + h / 2.0, x + w + gap - 2, y + h / 2.0, INK, 3))
    for i, (a, b) in enumerate(names):
        x = x0 + i * (w + gap)
        o.append(node(x, y, w, h, a, DATA_F, DATA_S, 2, None, [b]))
        o.append(ring_num(x + 14, y - 8, i + 1))
        bad = i > 0
        o.append(line(x + w / 2.0, y + h, x + w / 2.0, y + h + 34, BAD_S if bad else MUT, 2, None if bad else "6 4"))
        if bad:
            o.append(cross(x + w / 2.0, y + h + 46, 6))
        o.append(t(x + w / 2.0, y + h + 76, below[i][0], 12, INK, "middle"))
        o.append(t(x + w / 2.0, y + h + 92, below[i][1], 12, INK, "middle"))
    xe = x0 + 4 * (w + gap) + w
    o.append(arrow(xe + 1, y + h / 2.0, xe + 26, y + h / 2.0, OK_S, 3))
    o.append(rect(xe + 30, y + 16, 66, 44, 8, OK_F, OK_S, 3))
    o.append(t(xe + 63, y + 38, "PASS", 14, INK, "middle", central=True))
    o.append(rect(24, 300, 752, 46, 10, PANEL, GRID, 2))
    o.append(t(400, 318, "needles: all of them, or any one if the case says any_of; no partial credit", 12, INK, "middle", central=True))
    o.append(t(400, 336, "a case that must be refused ends at box 1: it passes only if the answer refused", 12, MUT, "middle", central=True))
    o.append(cap("Checks run left to right: the first failure ends the case.", 374))
    fig("fig-w34-4-scorer-check-order", "The scorer checks a refusal case first, then needles, then the citation, and gives no partial credit",
        "Five boxes in a row joined by arrows, numbered 1 to 5: must refuse, refused, needles, citation, cited equals fetched. "
        "Box 1 drops to a dashed note that a case which must be refused passes only if the answer refused. Boxes 2 to 5 each drop to a "
        "red cross: refused an answerable question; a needle is missing; no citation given; cited a note that was never retrieved. "
        "After box 5 an arrow leads to PASS. A strip below says needles are all of them, or any one when the case says any_of, with no partial credit.", o)


# ---------------------------------------------------------------- W34-5  25 cases, one case, wobble
def w34_5():
    o = [ctitle("What 25 cases can and cannot tell you")]
    o.append(rect(20, 62, 760, 164, 12, PANEL, GRID, 2))
    o.append(t(40, 84, "a true pass rate of 0.70 on 25 cases", 14, INK, "start", central=True))
    X0, CW = 60, 27.2
    for k in range(25):
        full = k < 17
        o.append(sq(X0 + k * CW, 100, CW, 34, DATA_F if full else PAPER, DATA_S if full else GRID, 2))
    o.append(sq(X0 + 17 * CW, 100, CW / 2.0, 34, DATA_F, DATA_S, 2))      # 17.5 expected passes: half of the 18th cell
    for v in (0, 5, 10, 15, 20, 25):
        o.append(line(X0 + v * CW, 134, X0 + v * CW, 142, INK, 1.5))
        o.append(t(X0 + v * CW, 156, str(v), 12, MUT, "middle"))
    lo, hi = 17.5 - 2.29, 17.5 + 2.29
    o.append(bracket(X0 + lo * CW, X0 + hi * CW, 166, 8, ACC_S, True))
    o.append(line(X0 + 17.5 * CW, 166, X0 + 17.5 * CW, 150, ACC_S, 2))
    o.append(t(X0 + 17.5 * CW, 196, "expected 17.5 passes, wobble 2.29 cases each way", 14, INK, "middle"))
    o.append(t(X0 + 17.5 * CW, 214, "so 17 of 25 could have been about 15 or 20", 12, MUT, "middle"))
    # hand sum
    o.append(rect(20, 240, 370, 96, 12, PAPER, HUMAN_S, 2))
    o.append(t(36, 262, "by hand", 14, HUMAN_S, "start", central=True))
    o.append(t(36, 286, "25 &#215; 0.70 &#215; 0.30 = 5.25", 14, INK, "start", mono=True, central=True))
    o.append(t(36, 308, "&#8730;5.25 = 2.29 cases", 14, INK, "start", mono=True, central=True))
    o.append(t(36, 328, "2.29 &#247; 25 = 0.092 of the score", 14, INK, "start", mono=True, central=True))
    # one case
    o.append(rect(410, 240, 370, 96, 12, PANEL, GRID, 2))
    o.append(t(425, 262, "one case is worth", 14, INK, "start", central=True))
    for k in range(25):
        o.append(sq(425 + k * 5, 274, 5, 14, ACC_F if k == 0 else PAPER, ACC_S if k == 0 else GRID, 1.5))
    o.append(t(560, 281, "1 of 25 = 0.04", 14, INK, "start", central=True))
    for k in range(6):
        o.append(sq(425 + k * 21, 304, 21, 22, ACC_F if k == 0 else PAPER, ACC_S if k == 0 else GRID, 2))
    o.append(t(560, 315, "1 of 6 = 0.17", 14, INK, "start", central=True))
    o.append(t(560, 332, "(a six-case category)", 12, MUT, "start", central=True))
    o.append(cap("One case is never a finding; a whole category moving, with the failing cases named, is.", 374))
    fig("fig-w34-5-twenty-five-cases-wobble", "On 25 cases a score wobbles by about 2.3 cases, and one case is worth 0.04 of the score",
        "A row of 25 cells with 17 filled and the 18th half filled, for 17.5 expected passes at a true pass rate of 0.70. A bracket spans "
        "15.2 to 19.8 passes, the expected 17.5 plus and minus a wobble of 2.29 cases. Below, a hand sum: 25 times 0.70 times 0.30 is 5.25, "
        "its square root is 2.29 cases, and 2.29 divided by 25 is 0.092 of the score. A second panel shows one cell of 25 highlighted, "
        "one case is 0.04 of the score, and one cell of a six-cell category, 0.17.", o)


# ---------------------------------------------------------------- W34-6  BLANK: severity against likelihood
def w34_6():
    o = [ctitle("Place the five failure modes")]
    modes = ["injected note writes outside its folder", "confident wrong answer, real-looking citation",
             "personal data in the notes ends up in logs", "a sum is copied from a note, not computed",
             "it refuses so often that Asha stops using it"]
    o.append(rect(20, 66, 330, 262, 12, PANEL, GRID, 2))
    o.append(t(36, 90, "Asha's design (Part A)", 14, INK, "start", central=True))
    for i, m in enumerate(modes):
        yy = 124 + i * 40
        o.append(ring_num(46, yy, i + 1))
        o.append(t(66, yy, m, 12, INK, "start", central=True))
    GX, GY, CW, CH = 430, 82, 62, 46
    for r in range(5):
        for c in range(5):
            o.append(sq(GX + c * CW, GY + r * CH, CW, CH, PAPER, GRID, 2))
    for c in range(5):
        o.append(t(GX + c * CW + CW / 2.0, GY + 5 * CH + 18, str(c + 1), 12, MUT, "middle"))
    for r in range(5):
        o.append(t(GX - 12, GY + r * CH + CH / 2.0, str(5 - r), 12, MUT, "end", central=True))
    o.append(t(GX + 5 * CW / 2.0, GY + 5 * CH + 40, "likelihood (1 rare ... 5 common)", 12, MUT, "middle"))
    o.append(trot(GX - 34, GY + 5 * CH / 2.0, "severity (1 mild ... 5 someone loses something)"))
    o.append(cap("Write each number in its cell, then ring the one you would read first.", 374))
    fig("fig-w34-6-blank-severity-likelihood", "Blank grid: put each failure mode where its likelihood and severity say",
        "A list of five failure modes for Asha's design, numbered 1 to 5, beside an empty five by five grid. The columns are likelihood from 1, "
        "rare, to 5, common; the rows are severity from 1, mild, to 5, someone loses something, with 5 at the top. Every cell is empty.", o)


# ---------------------------------------------------------------- W35-4  Spine.answer
def w35_4():
    o = [ctitle("answer(): guard, then route, then path")]
    o.append(rect(140, 88, 532, 250, 12, "none", GRID, 2, "6 4"))
    o.append(t(406, 80, "inside answer(): a catch-all that writes down and counts what it catches", 12, MUT, "middle"))
    # connectors first
    o.append(arrow(124, 200, 150, 200, INK, 3))
    o.append(arrow(284, 200, 314, 200, INK, 3))
    o.append(arrow(444, 190, 484, 140, INK, 3))
    o.append(arrow(444, 208, 484, 210, INK, 3))
    o.append(poly([(219, 230), (219, 284), (476, 284)], "none", BAD_S, 3))
    o.append(head(484, 284, 0, BAD_S, 3))
    o.append(arrow(654, 132, 696, 176, INK, 3))
    o.append(arrow(654, 210, 696, 196, INK, 3))
    o.append(arrow(654, 284, 696, 214, INK, 3))
    o.append(arrow(738, 232, 738, 266, INK, 3))
    o.append(t(300, 190, "else", 12, MUT, "middle"))
    o.append(t(226, 262, "guard hit", 12, BAD_S, "start"))
    o.append(node(24, 170, 100, 60, "question", DATA_F, DATA_S, 2))
    o.append(node(150, 170, 134, 60, "question_guard", HUMAN_F, HUMAN_S, 2, None, ["shapes, not meanings"]))
    o.append(node(314, 170, 130, 60, "route_of", HUMAN_F, HUMAN_S, 2, None, ["a number in it?"]))
    o.append(node(484, 100, 170, 64, "agent path", MODEL_F, MODEL_S, 2, "6 4", ["search, calculate, finish", STAND_IN]))
    o.append(node(484, 178, 170, 64, "retrieve path", MODEL_F, MODEL_S, 2, "6 4", ["below tau: refuse", STAND_IN]))
    o.append(node(484, 256, 170, 56, "refuse path", BAD_F, BAD_S, 2, None, ["a reason goes in the trace"]))
    o.append(node(696, 160, 84, 72, "Answer", DATA_F, DATA_S, 2, None, ["12 fields"]))
    o.append(node(696, 268, 84, 52, "trace line", PANEL, MUT, 2, None, ["written last"]))
    o.append(cap("Every path returns an Answer with all twelve fields, and a trace line is written for each.", 374))
    fig("fig-w35-4-spine-guard-route-path", "The spine runs the guard first, then the route, then one of three paths, and always returns an Answer",
        "A question enters question_guard, which matches shapes of attack and not meanings. If the guard hits, the question goes straight to the refuse path. "
        "Otherwise route_of decides whether a number appears in the question: yes sends it to the agent path (search, calculate, finish), no sends it to the retrieve "
        "path, which refuses when the top note scores below tau. The agent and retrieve paths are labelled stand-in, not a model. All three paths lead to an Answer with 12 fields "
        "and then a trace line written last. A dashed frame around the guard, route and paths marks a catch-all that writes down and counts what it catches.", o)


# ---------------------------------------------------------------- W35-5  promises against measurements
def w35_5():
    o = [ctitle("Four promises, read back as headroom")]
    X0, U = 300, 160.0
    rows = [("mean cost per task", "promised under $0.001", "measured $0.00045", 2.21, True),
            ("worst single task", "promised under $0.003", "measured $0.00148", 2.02, True),
            ("score", "promised at least 0.70", "measured 17 of 25 = 0.68", 0.97, False),
            ("refusals right", "promised at least 5", "measured 5", 1.00, True)]
    o.append(chip(604, 56, 172, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))
    o.append(line(X0, 100, X0, 316, GRID, 1.5))
    o.append(line(X0 + U, 96, X0 + U, 316, INK, 2, "6 4"))
    o.append(t(X0 + U, 90, "promise = 1.0", 12, INK, "middle"))
    for i, (nm, pr, ms, h, ok) in enumerate(rows):
        y = 112 + i * 54
        o.append(t(24, y + 8, nm, 14, INK, "start", central=True))
        o.append(t(24, y + 26, pr + "; " + ms, 12, MUT, "start", central=True))
    for i, (nm, pr, ms, h, ok) in enumerate(rows):
        y = 112 + i * 54
        o.append(rect(X0, y, U * h, 20, 3, OK_F if ok else BAD_F, OK_S if ok else BAD_S, 2))
        xe = X0 + U * h
        o.append(circ(xe, y + 10, 11, OK_F if ok else BAD_F, OK_S if ok else BAD_S, 2))
        o.append(tick(xe, y + 10, 5) if ok else cross(xe, y + 10, 4))
        o.append(t(xe + 18, y + 10, "%.2fx %s" % (h, "kept" if ok else "MISSED"), 14, INK, "start", central=True))
    for v in (0, 1, 2):
        o.append(line(X0 + v * U, 316, X0 + v * U, 324, INK, 1.5))
        o.append(t(X0 + v * U, 340, "%d" % v if v != 1 else "1.0", 12, MUT, "middle"))
    o.append(t(X0 + 1.0 * U, 354, "headroom (right of the dashed line = kept)", 12, MUT, "middle"))
    o.append(t(24, 340, "18 of 25 would have been 0.72", 12, MUT, "start"))
    o.append(cap("Cost: 0.001 &#247; 0.00045 = 2.21. Score: 0.68 &#247; 0.70 = 0.97, one case short, so MISSED.", 374))
    fig("fig-w35-5-promise-headroom", "A promise written before the build is read back as headroom; the score promise was missed by one case",
        "Four horizontal bars measured against a dashed line at headroom 1.0, the promise. Mean cost per task, promised under 0.001, measured 0.00045 stand-in dollars: "
        "headroom 2.21, kept. Worst single task, promised under 0.003, measured 0.00148: headroom 2.02, kept. Score, promised at least 0.70, measured 17 of 25 which is 0.68: "
        "headroom 0.97, just short of the line, MISSED; 18 of 25 would have been 0.72. Refusals right, promised at least 5, measured 5: headroom 1.00, kept with no room to spare. "
        "Dollars are stand-in dollars, from scripted stand-ins, not a model.", o)


# ---------------------------------------------------------------- W35-6  BLANK: headroom rulers
def w35_6():
    o = [ctitle("Mark your headroom on each ruler")]
    X0, U = 300, 160.0
    rows = ["mean cost, under $0.001", "worst task, under $0.003", "score, at least 0.70", "refusals right, at least 5 of 6"]
    o.append(line(X0 + U, 92, X0 + U, 312, INK, 2, "6 4"))
    o.append(t(X0 + U, 86, "promise = 1.0", 12, INK, "middle"))
    for i, nm in enumerate(rows):
        y = 112 + i * 54
        o.append(t(24, y + 10, nm, 14, INK, "start", central=True))
        o.append(line(X0, y + 10, X0 + 2.5 * U, y + 10, INK, 2))
        for v in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
            o.append(line(X0 + v * U, y + 4, X0 + v * U, y + 16, INK, 1.5))
        o.append(rect(692, y - 4, 84, 28, 8, PAPER, HUMAN_S, 2, "6 4"))
        o.append(t(734, y + 10, "kept / MISSED", 12, MUT, "middle", central=True))
    for v in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
        o.append(t(X0 + v * U, 336, "%g" % v if v != 1.0 else "1.0", 12, MUT, "middle"))
    o.append(t(X0 + 1.25 * U, 356, "headroom", 12, MUT, "middle"))
    o.append(cap("Mark each headroom from Part A with a cross; write kept or MISSED in the box.", 372))
    fig("fig-w35-6-blank-headroom-rulers", "Blank rulers: mark each promise's headroom and say whether it was kept",
        "Four horizontal rulers from 0 to 2.5, one each for mean cost under $0.001, worst task under $0.003, score at least 0.70 and refusals right at least 5 of 6. "
        "A dashed vertical line at 1.0 marks the promise. At the right of each ruler is an empty box for the words kept or MISSED. No ruler is marked.", o)


# ---------------------------------------------------------------- W36-4  what the capstone folder holds
def w36_4():
    o = [ctitle("What the capstone folder holds")]
    cols = [("Week 34", "the test, before the system", HUMAN_F, HUMAN_S,
             ["DESIGN.md", "eval/cases.py", "eval/freeze.py", "eval/FROZEN.txt"]),
            ("Week 35", "the system and its numbers", MODEL_F, MODEL_S,
             ["src/contract.py", "eval/score.py", "src/baseline.py", "src/guards.py", "src/spine.py",
              "eval/run_eval.py", "eval/COMMITTED.json", "eval/redteam.py", "RED_TEAM.md"]),
            ("Week 36", "say it twice", ACC_F, ACC_S, ["SYSTEM_CARD.md", "ask.py", "demo.py"])]
    for i, (wk, sub, f, s, files) in enumerate(cols):
        x = 20 + i * 256
        if i < 2:
            o.append(arrow(x + 234, 190, x + 254, 190, INK, 3))
        o.append(rect(x, 64, 232, 250, 12, PANEL, s, 3))
        o.append(rect(x + 12, 76, 208, 28, 8, f, s, 2))
        o.append(t(x + 116, 90, wk, 14, INK, "middle", central=True))
        o.append(t(x + 116, 122, sub, 12, MUT, "middle", central=True))
        for k, fn in enumerate(files):
            o.append(t(x + 22, 148 + k * 18, fn, 12, INK, "start", mono=True, central=True))
    o.append(rect(532 + 12, 214, 208, 84, 8, PAPER, MUT, 2, "6 4"))
    o.append(t(648, 240, "Sitting 2: the paper", 14, INK, "middle", central=True))
    o.append(t(648, 262, "75 marks, no computer,", 12, MUT, "middle", central=True))
    o.append(t(648, 280, "no notes", 12, MUT, "middle", central=True))
    o.append(t(400, 330, "pieces from earlier weeks: W26 retrieve and cite &#183; W28 tool loop &#183; W29 trace and cost", 12, MUT, "middle"))
    o.append(t(400, 346, "W30 frozen suite &#183; W33 attacks and redaction", 12, MUT, "middle"))
    o.append(cap("The test was frozen in Week 34; the logs from Week 35 feed the card, so no number is typed.", 372))
    fig("fig-w36-4-capstone-folder-map", "The capstone folder grows in three steps: the test, the system, then the card and the demo",
        "Three panels joined by arrows. Week 34, the test before the system: DESIGN.md, eval/cases.py, eval/freeze.py and eval/FROZEN.txt. Week 35, the system and its numbers: "
        "src/contract.py, eval/score.py, src/baseline.py, src/guards.py, src/spine.py, eval/run_eval.py, eval/COMMITTED.json, eval/redteam.py and RED_TEAM.md. Week 36, say it twice: "
        "SYSTEM_CARD.md, ask.py and demo.py, with a dashed box for Sitting 2, the paper: 75 marks, no computer, no notes. A line below names the pieces from earlier weeks: "
        "Week 26 retrieve and cite, Week 28 tool loop, Week 29 trace and cost, Week 30 frozen suite, Week 33 attacks and redaction.", o)


# ---------------------------------------------------------------- W36-5  the paper's 75 marks
def w36_5():
    o = [ctitle("The paper: 75 marks in five sections")]
    secs = [("A", 20, "one-mark", "multiple choice"), ("B", 16, "short", "programs"), ("C", 12, "bugs", ""),
            ("D", 15, "arithmetic", "by hand"), ("E", 12, "reading two", "tables")]
    X0, PM = 40, 9.6
    x = X0
    for k, (L, m, a, b) in enumerate(secs):
        w = m * PM
        o.append(rect(x + 1, 96, w - 2, 70, 8, DATA_F, DATA_S, 2))
        o.append(t(x + w / 2.0, 120, "Section " + L if w > 130 else L, 14, INK, "middle", central=True))
        o.append(t(x + w / 2.0, 146, "%d marks" % m, 14, INK, "middle", central=True))
        o.append(line(x + w / 2.0, 168, x + w / 2.0, 186, GRID, 1.5))
        o.append(t(x + w / 2.0, 204, a, 12, INK, "middle"))
        if b:
            o.append(t(x + w / 2.0, 220, b, 12, INK, "middle"))
        x += w
    for v in (0, 20, 36, 48, 63, 75):
        o.append(line(X0 + v * PM, 166, X0 + v * PM, 176, INK, 1.5))
        o.append(t(X0 + v * PM, 82, str(v), 12, MUT, "middle"))
    o.append(rect(20, 250, 760, 82, 12, PANEL, HUMAN_S, 2))
    o.append(t(400, 276, "20 + 16 + 12 + 15 + 12 = 75 marks", 18, INK, "middle", central=True))
    o.append(t(400, 304, "75 marks in 75 minutes: one mark a minute", 14, INK, "middle", central=True))
    o.append(t(400, 322, "partial working earns marks; if you do not know, write did not get it", 12, MUT, "middle", central=True))
    o.append(cap("The ticks 20, 36, 48, 63, 75 are running totals: the sections add up to the paper.", 374))
    fig("fig-w36-5-paper-marks-bar", "The final paper is 75 marks in five sections, and the sections add up to 75",
        "One bar 75 marks long split into five sections: A 20 marks one-mark multiple choice; B 16 marks short programs; C 12 marks bugs; D 15 marks arithmetic by hand; "
        "E 12 marks reading two tables. Ticks on the bar mark the running totals 0, 20, 36, 48, 63 and 75. Below, the sum 20 + 16 + 12 + 15 + 12 = 75 and the time: "
        "75 marks in 75 minutes, one mark a minute. Partial working earns marks.", o)


# ---------------------------------------------------------------- W36-6  BLANK: per-week grid
def w36_6():
    o = [ctitle("The per-week grid, blank")]
    weeks = [("W26", "RAG: retrieve, cite, refuse"), ("W28", "Tools and the loop"), ("W29", "Agents: attack and budget"),
             ("W30", "Frozen suite and the judge"), ("W31", "Fine-tuning and LoRA"), ("W32", "Calibration and abstention"),
             ("W33", "Attack your own system"), ("W34", "Capstone 1: the frozen eval"), ("W35", "Capstone 2: build, measure"),
             ("W36", "Capstone 3: demo and card")]
    cx = [24, 74, 318, 456, 536, 616, 696]          # week, title, felt, scored, available, ratio, ring
    heads = [(cx[0], "week"), (cx[1], "topic"), (cx[2], "how sure (ring one)"), (cx[3] + 28, "scored"),
             (cx[4] + 28, "available"), (cx[5] + 28, "ratio"), (cx[6] + 40, "ring two")]
    for x, s in heads:
        o.append(t(x if s in ("week", "topic", "how sure (ring one)") else x, 76, s, 12, MUT,
                   "start" if s in ("week", "topic", "how sure (ring one)") else "middle"))
    o.append(line(20, 84, 780, 84, GRID, 1.5))
    for i, (w, ti) in enumerate(weeks):
        y = 104 + i * 25
        o.append(t(cx[0], y, w, 14, INK, "start", central=True))
        o.append(t(cx[1], y, ti, 14, INK, "start", central=True))
        for j, L in enumerate("SUG"):
            xx = cx[2] + 18 + j * 42
            o.append(circ(xx, y, 10, PAPER, MUT, 2))
            o.append(t(xx, y, L, 12, MUT, "middle", central=True))
        for c in (3, 4, 5):
            o.append(rect(cx[c], y - 10, 56, 20, 4, PAPER, MUT, 2, "6 4"))
        o.append(circ(cx[6] + 40, y, 10, PAPER, ACC_S, 2))
    o.append(line(20, 104 + 9 * 25 + 14, 780, 104 + 9 * 25 + 14, GRID, 1.5))
    o.append(t(24, 352, "S = sure, U = unsure, G = guessed.  Marks available are on your marking sheet.", 12, MUT, "start"))
    o.append(cap("Fill in your own marks and ring at most two weeks. Nothing on the grid is a grade.", 376))
    fig("fig-w36-6-blank-per-week-grid", "Blank per-week grid: your marks per week of Term 4, and the two weeks to revisit",
        "An empty table with ten rows, weeks 26, 28, 29, 30, 31, 32, 33, 34, 35 and 36, each with a short topic. Each row has three small rings marked S, U and G for sure, unsure and "
        "guessed, three empty dashed boxes for scored, available and ratio, and one empty ring to circle the week. Nothing is filled in.", o)


def build():
    for f in (w34_4, w34_5, w34_6, w35_4, w35_5, w35_6, w36_4, w36_5, w36_6):
        f()
    return FIGS
