"""Block 12 (weeks 34, 35, 36) concept figures. Every number is copied from the week's printed output
(student-guide/week-34.md .. week-36.md); the source is named beside each figure. Written fresh for Level 4.

    build() -> {filename: svg_text}     (called by _gen_build.py, which writes them next to the maps)
"""
from _gen_core import *

VB = "0 0 800 400"


def title(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=376):
    return t(400, y, s, 14, MUT, "middle")


def box(x, y, w, h, fill, stroke, lab, sub, dash=None, sw=3):
    cx = x + w / 2.0
    return "\n  ".join([rect(x, y, w, h, 10, fill, stroke, sw, dash),
                        t(cx, y + h / 2.0 - 8, lab, 18, INK, "middle", central=True),
                        t(cx, y + h / 2.0 + 16, sub, 14, MUT, "middle", central=True)])


def w34_flow():
    xs = [40, 230, 420, 610]
    p = []
    for i in range(3):
        p.append(arrow(xs[i] + 144, 165, xs[i + 1] - 4, 165, INK, 3))
    p.append(box(xs[0], 100, 140, 130, HUMAN_F, HUMAN_S, "1 Design", "7 headings, 1 page"))
    p.append(box(xs[1], 100, 140, 130, HUMAN_F, HUMAN_S, "2 Test", "25 cases, 6 categories"))
    p.append(box(xs[2], 100, 140, 130, ACC_F, ACC_S, "3 Freeze", "hash, src/ empty"))
    p.append(box(xs[3], 100, 140, 130, PANEL, GRID, "4 System", "Week 35: not built", dash="6 4", sw=2))
    p.append(t(130, 262, "the demo freeze of the 8 example cases", 12, MUT, "start"))
    p.append(terminal(130, 270, 540, ["a80e5bfd45ee&#8230; cases=8 frozen=2026-10-05 src_files=0",
                                      "python files in src/: 0"], 12, 18, hi=0))
    p.append(cap("The test is written and frozen before the thing it tests exists.", 366))
    return svg_doc(VB, "Write and freeze the test before the system exists",
                   "Four boxes left to right joined by arrows: 1 Design, 2 Test (25 cases in 6 categories), "
                   "3 Freeze (a hash is written while src/ is empty), 4 System (dashed, not built until Week 35). "
                   "Below, the demo freeze line for the 8 example cases reads cases=8, src_files=0, and "
                   "python files in src/ is 0.",
                   J(title("Design, test, freeze, then the system"), *p))


def w34_scorer():
    cats = ["fact", "fact", "fact", "hop", "arith", "scope", "adv", "amb"]
    rows = [("refuse_all", [0, 0, 0, 0, 0, 1, 1, 0], "2/8 = 0.25"),
            ("oracle", [1] * 8, "8/8 = 1.00"),
            ("echo", [0] * 8, "0/8 = 0.00")]
    x0, cw = 200, 54
    p = [stand_in_frame(24, 100, 752, 215)]
    for k, c in enumerate(cats):
        p.append(t(x0 + cw * k + cw / 2.0, 124, c, 12, MUT, "middle"))
    for r, (name, v, sc) in enumerate(rows):
        y = 136 + r * 58
        p.append(t(40, y + 24, name, 14, INK, "start", mono=True, central=True))
        for k, ok in enumerate(v):
            cx = x0 + cw * k
            p.append(sq(cx, y, cw, 48, OK_F if ok else BAD_F, OK_S if ok else BAD_S, 2))
            p.append(tick(cx + cw / 2.0, y + 24, 9) if ok else cross(cx + cw / 2.0, y + 24, 7))
        p.append(t(x0 + cw * 8 + 14, y + 24, sc, 14, INK, "start", central=True))
    p.append(cap("Floor 2/8 (not 0), ceiling 8/8, junk 0/8: the scorer does what it says.", 350))
    return svg_doc(VB, "A scorer is tested on answers typed by hand: floor, ceiling and junk",
                   "Three scripted stand-ins, each marked on the same 8 example cases (3 factual, multi_hop, "
                   "arithmetic, out_of_scope, adversarial, ambiguous). refuse_all passes only the out_of_scope and "
                   "adversarial cases: 2/8 = 0.25. oracle passes all 8: 1.00. echo passes none: 0.00. "
                   "Ticks mark a pass and crosses a fail.",
                   J(title("Test the scorer, not just use it"), *p))


def w35_bars():
    cats = [("factual", 9, 8, 8), ("multi_hop", 4, 0, 0), ("arithmetic", 4, 0, 3),
            ("out_of_scope", 3, 2, 2), ("adversarial", 3, 0, 3), ("ambiguous", 2, 1, 1)]
    x0, W = 250, 300
    p = [stand_in_frame(580, 96, 196, 236, 678, 96)]
    p.append(line(x0, 98, x0, 338, GRID, 1.5))
    p.append(line(x0 + W, 98, x0 + W, 338, GRID, 1.5, "6 4"))
    p.append(t(x0, 356, "0", 12, MUT, "middle"))
    p.append(t(x0 + W, 356, "all cases", 12, MUT, "middle"))
    for i, (c, n, b, v) in enumerate(cats):
        y = 104 + i * 38
        p.append(t(x0 - 14, y + 15, "%s  n=%d" % (c.replace("_", " "), n), 14, INK, "end", central=True))
        for j, (val, fill, stroke, kind, lab) in enumerate([(b, DATA_F, DATA_S, "circle", "baseline"),
                                                            (v, MODEL_F, MODEL_S, "square", "v1")]):
            yy = y + j * 17
            w = W * val / n
            if w > 0:
                p.append(rect(x0, yy, w, 14, 3, fill, stroke, 2))
            p.append(mark(kind, x0 + w, yy + 7, 5, stroke, fill, 2))
            p.append(t(x0 + w + 12, yy + 7, "%s %d/%d" % (lab, val, n), 12, INK, "start", central=True))
    p.append(t(678, 128, "all 25 cases", 14, INK, "middle"))
    for k, s in enumerate(["floor  6", "baseline  11", "v1 spine  17", "wobble  2.3"]):
        p.append(t(678, 168 + k * 36, s, 14, INK, "middle"))
    p.append(t(678, 300, "(counts out of 25)", 12, MUT, "middle"))
    p.append(cap("The baseline is the number the spine has to beat: 11 of 25, then 17 of 25.", 374))
    return svg_doc(VB, "Floor, baseline and spine measured on the same 25 frozen cases",
                   "For each of six categories two bars show passes out of n: baseline (circle end) and v1 spine "
                   "(square end). factual 8/9 and 8/9; multi_hop 0/4 and 0/4; arithmetic 0/4 and 3/4; out_of_scope "
                   "2/3 and 2/3; adversarial 0/3 and 3/3; ambiguous 1/2 and 1/2. Totals: floor 6 of 25, baseline "
                   "11 of 25, v1 17 of 25, wobble 2.3. Everything is measured on scripted stand-ins.",
                   J(title("Floor, baseline, spine: the same 25 cases"), *p))


def w35_regression():
    ax, sc = 60, 1750.0

    def X(v):
        return ax + v * sc
    p = [line(ax, 200, ax + 0.4 * sc, 200, INK, 2)]
    for v in (0, 0.1, 0.2, 0.3, 0.4):
        p.append(line(X(v), 196, X(v), 204, INK, 2))
        p.append(t(X(v), 222, "%.1f" % v if v else "0", 12, MUT, "middle"))
    p.append(line(X(0.10), 112, X(0.10), 290, HUMAN_S, 3, "6 4"))
    p.append(line(X(0.36), 112, X(0.36), 290, ACC_S, 3))
    p.append(t(X(0.10), 100, "v1 cut: tau 0.10", 14, HUMAN_S, "middle"))
    p.append(t(X(0.36), 100, "v2 cut: tau 0.36", 14, ACC_S, "middle"))
    pts = [("c09", 0.133, False, "below"), ("c01", 0.151, False, "above"),
           ("c03", 0.236, False, "above"), ("c19", 0.357, True, "below")]
    for name, v, good, side in pts:
        cx = X(v)
        if side == "above":
            p.append(line(cx, 190, cx, 164, GRID, 1.5))
            p.append(t(cx, 156, "%s  %.3f" % (name, v), 12, INK, "middle"))
            p.append(t(cx, 140, "fail &#8594; pass" if good else "pass &#8594; FAIL", 12, MUT, "middle"))
        else:
            p.append(line(cx, 210, cx, 250, GRID, 1.5))
            p.append(t(cx, 264, "%s  %.3f" % (name, v), 12, INK, "middle"))
            p.append(t(cx, 280, "fail &#8594; pass" if good else "pass &#8594; FAIL", 12, MUT, "middle"))
    for name, v, good, side in pts:
        cx = X(v)
        p.append(circ(cx, 200, 11, OK_F if good else BAD_F, OK_S if good else BAD_S, 2))
        p.append(tick(cx, 200, 5) if good else cross(cx, 200, 4))
    p.append(t(410, 304, "best-note score of the question (0 to 0.40)", 12, MUT, "middle"))
    p.append(t(400, 328, "overall 17 &#8594; 15 of 25 (wobble 2.3)  &#183;  factual 8 &#8594; 5 of 9  &#183;  "
                         "out of scope 2 &#8594; 3 of 3", 14, INK, "middle"))
    p.append(cap("Cut at 0.36: wins c19, loses c01, c03 and c09. A named mechanism, not noise.", 360))
    return svg_doc(VB, "One change to the threshold flipped four named cases: that is a regression, caught",
                   "A number line of best-note scores from 0 to 0.40 with a dashed cut at tau 0.10 (v1) and a solid "
                   "cut at tau 0.36 (v2). Four cases sit between: c09 at 0.133, c01 at 0.151, c03 at 0.236 and c19 at "
                   "0.357. Under v2 all four are refused: c01, c03 and c09 go from pass to FAIL and c19 goes from fail "
                   "to pass. Overall 17 to 15 of 25, factual 8 to 5 of 9, out_of_scope 2 to 3 of 3.",
                   J(title("One threshold change, four flipped cases"), *p))


def w36_ledger():
    xs = [40, 230, 420, 610]
    p = [arrow(xs[i] + 154, 110, xs[i + 1] - 4, 110, INK, 3) for i in range(3)]
    p.append(box(xs[0], 70, 150, 80, DATA_F, DATA_S, "Logs", "run_eval, redteam"))
    p.append(box(xs[1], 70, 150, 80, DATA_F, DATA_S, "F", "one dict, read once"))
    p.append(box(xs[2], 70, 150, 80, HUMAN_F, HUMAN_S, "Card", "numbers are slots"))
    p.append(box(xs[3], 70, 150, 80, OK_F, OK_S, "Checks", "check_card + you"))
    p.append(rect(30, 172, 740, 170, 12, PANEL, GRID, 2))
    for x, s in [(50, "claim"), (330, "number"), (450, "n"), (500, "command")]:
        p.append(t(x, 198, s, 12, MUT, "start", weight="600"))
    p.append(line(44, 208, 756, 208, GRID, 1.5))
    rows = [("overall score of v1.1", "17 of 25", "25", "run_eval.py v1.1"),
            ("baseline (one search)", "11 of 25", "25", "run_eval.py baseline"),
            ("A1 landed before the fix", "15 of 50", "50", "block S3, seeds 0&#8211;49"),
            ("redactor caught typed cases", "6 of 8", "8", "block S3")]
    for k, (a, b, c, d) in enumerate(rows):
        y = 232 + k * 28
        p.append(t(50, y, a, 14, INK, "start", central=True))
        p.append(t(330, y, b, 14, INK, "start", central=True))
        p.append(t(450, y, c, 14, INK, "start", central=True))
        p.append(t(500, y, d, 12, INK, "start", mono=True, central=True))
    p.append(cap("A claim with no command does not go in the card: every number is a slot filled from a log.", 372))
    return svg_doc(VB, "A claim has a number, an n and a command, or it is a mood",
                   "A flow of four boxes: Logs (run_eval, redteam), F (one dict, read once), Card (numbers are slots), "
                   "Checks (check_card plus you reading every number). Below, four ledger rows each with a claim, "
                   "a number, an n and the command that printed it: overall score of v1.1 17 of 25; baseline 11 of 25; "
                   "A1 landed before the fix 15 of 50; redactor caught 6 of 8.",
                   J(title("The card is made from the logs"), *p))


def w36_runsheet():
    segs = [("SAY IT", 30, "for Asha, 15 notes", HUMAN_F, HUMAN_S),
            ("IT WORKS", 60, "c01 and c14 both pass", OK_F, OK_S),
            ("THE NUMBER", 60, "17 of 25; worst row multi_hop 0 of 4", DATA_F, DATA_S),
            ("IT FAILS", 60, "c19: best note scores 0.357", BAD_F, BAD_S),
            ("I ATTACKED IT", 60, "A1 landed 15/50 &#8594; 0/50", ACC_F, ACC_S),
            ("WHO SHOULD NOT RELY", 30, "the card's last section", MODEL_F, MODEL_S)]
    p = []
    x, sec = 40.0, 0
    marks = []
    for k, (name, s, det, f, st) in enumerate(segs):
        w = s * 2.4
        p.append(rect(x + 1, 112, w - 2, 56, 8, f, st, 2))
        p.append(t(x + w / 2.0, 140, "%d s" % s, 14, INK, "middle", central=True))
        p.append(ring_num(x + w / 2.0, 95, k + 1))
        marks.append((x, sec))
        x += w
        sec += s
    marks.append((x, sec))
    for mx, ms in marks:
        p.append(line(mx, 168, mx, 176, INK, 2))
        p.append(t(mx, 192, "%d:%02d" % (ms // 60, ms % 60), 12, MUT, "middle"))
    for k, (name, s, det, f, st) in enumerate(segs):
        col, row = k // 3, k % 3
        cx = 60 + col * 380
        y = 236 + row * 44
        p.append(ring_num(cx, y, k + 1))
        p.append(t(cx + 22, y, "%s (%d s)" % (name, s), 14, INK, "start", central=True))
        p.append(t(cx + 22, y + 18, det, 12, MUT, "start", central=True))
    p.append(cap("30 + 60 + 60 + 60 + 60 + 30 = 300 seconds; one failure is shown on purpose.", 374))
    return svg_doc(VB, "The five-minute demo is six timed segments, one of them a failure shown on purpose",
                   "A timeline bar from 0:00 to 5:00 in six numbered segments: 1 SAY IT 30 s, 2 IT WORKS 60 s, "
                   "3 THE NUMBER 60 s (17 of 25, worst row multi_hop 0 of 4), 4 IT FAILS 60 s (case c19, best note "
                   "scores 0.357), 5 I ATTACKED IT 60 s (A1 landed 15/50 then 0/50), 6 WHO SHOULD NOT RELY ON IT 30 s.",
                   J(title("The five-minute run-sheet"), *p))


def build():
    return {
        "fig-w34-1-test-before-system.svg": w34_flow(),
        "fig-w34-2-scorer-floor-ceiling.svg": w34_scorer(),
        "fig-w35-1-floor-baseline-spine.svg": w35_bars(),
        "fig-w35-2-threshold-regression.svg": w35_regression(),
        "fig-w36-1-claim-ledger-flow.svg": w36_ledger(),
        "fig-w36-2-five-minute-run-sheet.svg": w36_runsheet(),
    }
