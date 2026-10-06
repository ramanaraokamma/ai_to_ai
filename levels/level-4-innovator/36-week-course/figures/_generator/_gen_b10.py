"""Block 10 figures: weeks 28, 29, 30 (two concept figures each). Deterministic; no randomness.

Every number printed on a canvas is copied from the week's executed output (student-guide/week-NN.md)
or is a hand sum whose working is printed beside it (STYLE.md 2.1). Stand-ins carry the dashed frame/chip (2.5).

    python3 _gen_b10.py        # (re)writes the six fig-w28/29/30-{1,2}-*.svg files
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_core import *   # noqa: E402,F401

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # figures/
WIDE = "0 0 800 400"


def title(s):
    return t(400, 44, s, 24, INK, "middle")


def caption(s, y=376):
    """One or two lines (a list): the last baseline is y, the first is 18 above."""
    lines = [s] if isinstance(s, str) else list(s)
    return "\n  ".join(t(400, y - 18 * (len(lines) - 1 - i), ln, 14, MUT, "middle") for i, ln in enumerate(lines))


def standin_chip(x, y):
    return chip(x, y, 172, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False, dash="6 4")


# ------------------------------------------------------------------ W28-1
def w28_1():
    rows = [("report.md", "&lt;ROOT&gt;/report.md", True),
            ("sub/a.md", "&lt;ROOT&gt;/sub/a.md", True),
            ("notes/../report.md", "&lt;ROOT&gt;/report.md", True),
            ("../escape.md", "(outside the sandbox)", False),
            ("a/../../escape.md", "(outside the sandbox)", False),
            ("/etc/passwd", "(outside the sandbox)", False)]
    o = [title("Resolve first, compare second")]
    o.append(t(40, 86, "name asked for", 14, MUT))
    o.append(t(300, 86, "where it really points", 14, MUT))
    o.append(t(560, 86, "at or below the root?", 14, MUT))
    o.append(line(40, 96, 760, 96, GRID, 1.5))
    for i, (name, where, ok) in enumerate(rows):
        y = 108 + i * 38
        c = y + 16
        o.append(rect(34, y, 150, 32, 8, DATA_F, DATA_S, 2))
        o.append(t(44, c, name, 14, INK, mono=True, central=True))
        o.append(arrow(190, c, 280, c, INK, 2))
        o.append(t(300, c, where, 14, INK, mono=ok, central=True))
        if ok:
            o.append(rect(556, y, 150, 32, 8, OK_F, OK_S, 3))
            o.append(tick(578, c, 9, OK_S))
            o.append(t(596, c, "inside: True", 14, INK, mono=True, central=True))
        else:
            o.append(rect(556, y, 150, 32, 8, BAD_F, BAD_S, 3))
            o.append(cross(578, c, 7, BAD_S))
            o.append(t(596, c, "inside: False", 14, INK, mono=True, central=True))
    o.append(caption(["The root is resolved once. Each name is followed (.. cancels the folder before it),", "and only then compared. 3 of 6 names stay inside."]))
    desc = ("Six file names a tool was asked to write, each with an arrow to where it really points and a verdict. "
            "report.md, sub/a.md and notes/../report.md land inside the sandbox root, so inside is True. "
            "../escape.md, a/../../escape.md and /etc/passwd resolve outside it, so inside is False. "
            "Numbers and names are the printed output of sandbox_check.py in Week 28.")
    return "fig-w28-1-resolve-first-compare-second.svg", svg_doc(
        WIDE, "A path is judged by where it really points, not by how it is written", desc, J(o))


# ------------------------------------------------------------------ W28-2
def w28_2():
    ins = [247, 415, 448, 519, 566]
    labs = ["search ok", "calculate ok", "write ERR", "write ok", "answer"]
    base, sc = 290, 180.0 / 566
    o = [title("Every turn re-sends the whole conversation")]
    o.append(standin_chip(560, 62))
    ytop1 = base - ins[0] * sc
    o.append(line(40, ytop1, 515, ytop1, MUT, 1.5, "6 4"))
    o.append(t(520, ytop1 + 4, "247", 12, MUT))
    o.append(line(40, base, 515, base, INK, 2))
    for i, v in enumerate(ins):
        x = 60 + i * 90
        h = v * sc
        o.append(rect(x, base - h, 70, h, 4, DATA_F, DATA_S, 2))
        o.append(t(x + 35, base - h - 8, str(v), 14, INK, "middle"))
        o.append(t(x + 35, base + 20, "turn %d" % (i + 1), 14, INK, "middle"))
        o.append(t(x + 35, base + 38, labs[i], 12, MUT, "middle"))
    o.append(cross(60 + 2 * 90 + 8, base + 56, 5, BAD_S))
    o.append(t(60 + 2 * 90 + 20, base + 60, "tool error, read and recovered", 12, MUT))
    o.append(trot(36, 190, "input tokens sent on that turn", 12))
    # right panel
    o.append(rect(560, 100, 220, 96, 10, PANEL, INK, 2))
    o.append(t(570, 124, "total input, measured", 14, MUT))
    o.append(t(570, 156, "2195 tokens", 24, INK))
    o.append(t(570, 182, "growth: 168, 33, 71, 47", 14, INK))
    o.append(rect(560, 214, 220, 70, 10, PAPER, GRID, 2, "6 4"))
    o.append(t(570, 238, "if turn 1 were re-used", 14, MUT))
    o.append(t(570, 270, "5 &#215; 247 = 1235", 18, INK))
    o.append(caption(["Same 5 turns: 2195 input tokens sent, against 1235 if nothing were re-sent.", "A scripted plan; the growth shape is real."]))
    desc = ("Five bars of input tokens per turn: turn 1 247, turn 2 415, turn 3 448, turn 4 519, turn 5 566. "
            "A dashed line marks 247, the size of turn 1. Turn 3 is a failed write that the plan then recovers from. "
            "A side panel states the measured total, 2195 input tokens, against 5 times 247 equals 1235 if turn 1 were re-used. "
            "The plan is a scripted stand-in, not a model. Numbers from run_worked.py and growth.py, Week 28.")
    return "fig-w28-2-input-grows-every-turn.svg", svg_doc(
        WIDE, "A long task costs more than it looks because the history is sent again each turn", desc, J(o))


# ------------------------------------------------------------------ W29-1
def w29_1():
    rows = [("no layers", 100, 100), ("layer 1: frame", 69, 60), ("layer 2: scan", 58, 50), ("layers 1 + 2", 32, 30)]
    x0, sc = 240, 3.0
    o = [title("Soft layers lower the rate; the fence stops it")]
    o.append(standin_chip(590, 56))
    o.append(line(x0, 96, x0, 372, INK, 2))
    for i, (lab, ob, exp) in enumerate(rows):
        y = 100 + i * 62
        o.append(t(x0 - 12, y + 12, lab, 14, INK, "end", central=True))
        o.append(rect(x0, y, ob * sc, 24, 4, DATA_F, DATA_S, 2))
        o.append(t(x0 + ob * sc + 8, y + 12, "%d obeyed (expected %d)" % (ob, exp), 14, INK, central=True))
        o.append(tick(x0 + 12, y + 41, 8, OK_S))
        o.append(t(x0 + 28, y + 41, "file landed: 0 of 100 runs, strict sandbox", 12, OK_S, central=True))
    o.append(caption(["Gullibility 1.0, 100 seeded runs each (seeds 0&#8211;99), on a stand-in.", "The rates are typed in: they show which defence moves a rate, not model behaviour."]))
    desc = ("Four horizontal bars of how many of 100 seeded runs obeyed the planted order, with gullibility 1.0 on a scripted stand-in. "
            "No layers: 100 obeyed, expected 100. Layer 1 framing: 69, expected 60. Layer 2 scan: 58, expected 50. Both layers: 32, expected 30. "
            "Under each bar a green tick states that the file landed in 0 of 100 runs with the strict sandbox. Numbers from layers.py, Week 29.")
    return "fig-w29-1-three-layers-rates-vs-fence.svg", svg_doc(
        WIDE, "Prompt-level defences lower the rate, the sandbox fence stops the damage", desc, J(o))


# ------------------------------------------------------------------ W29-2
def w29_2():
    meas = [(4, 0.001649), (8, 0.003585), (10, 0.004748), (12, 0.006041), (20, 0.012513), (30, 0.023528)]
    # straight line through k = 4, 8, 12 (least squares by hand-checkable normal equations)
    ks = [4, 8, 12]
    ds = [0.001649, 0.003585, 0.006041]
    mk, md = sum(ks) / 3.0, sum(ds) / 3.0
    slope = sum((k - mk) * (d - md) for k, d in zip(ks, ds)) / sum((k - mk) ** 2 for k in ks)
    icpt = md - slope * mk
    # printed value (budget2.py) is $0.015836 at k=30 from full-precision spends; ours must agree to 4 decimals
    assert abs(slope * 30 + icpt - 0.015836) < 0.0002, slope * 30 + icpt
    X0, Y0, KS, DS = 100, 300, 380 / 30.0, 210 / 0.025

    def px(k): return X0 + k * KS
    def py(d): return Y0 - d * DS
    o = [title("The bill bends upward; a straight line misses it")]
    for d, lab in [(0, "$0"), (0.01, "$0.01"), (0.02, "$0.02")]:
        o.append(line(X0, py(d), 485, py(d), GRID, 1.5))
        o.append(t(X0 - 8, py(d) + 4, lab, 12, MUT, "end"))
    for k in (0, 10, 20, 30):
        o.append(t(px(k), Y0 + 20, str(k), 12, MUT, "middle"))
    o.append(t(X0 + 200, Y0 + 40, "tool steps k", 12, MUT, "middle"))
    o.append(trot(40, 195, "spend, dollars", 12))
    o.append(line(X0, 86, X0, Y0, INK, 2))
    line_end = slope * 30 + icpt
    o.append(poly([(px(4), py(slope * 4 + icpt)), (px(30), py(line_end))], "none", BAD_S, 3, "6 4"))
    o.append(poly([(px(k), py(d)) for k, d in meas], "none", DATA_S, 3))
    for k, d in meas:
        o.append(mark("circle", px(k), py(d), 5, DATA_S, DATA_F))
    o.append(mark("triangle", px(30), py(line_end), 6, BAD_S, BAD_F))
    o.append(t(px(30) - 10, py(0.023528) - 8, "measured $0.023528 (k=30)", 12, INK, "end"))
    o.append(t(px(30) - 10, py(line_end) + 28, "straight line: $0.015836", 12, BAD_S, "end"))
    # right panel
    o.append(rect(520, 86, 260, 64, 10, PANEL, INK, 2))
    o.append(t(532, 108, "10 to 30 steps: 3 times", 14, MUT))
    o.append(t(532, 136, "4.96 times the cost", 18, INK))
    o.append(rect(520, 164, 260, 64, 10, PANEL, INK, 2))
    o.append(t(532, 186, "re-sent history, share of bill", 14, MUT))
    o.append(t(532, 214, "38% (k=10), 64% (k=30)", 18, INK))
    o.append(rect(520, 242, 260, 64, 10, PAPER, BAD_S, 2, "6 4"))
    o.append(t(532, 264, "line through k = 4, 8, 12", 14, MUT))
    o.append(t(532, 292, "about a third too low", 18, BAD_S))
    o.append(caption(["Spend of a scripted plan at k = 4, 8, 10, 12, 20, 30 (illustrative prices).", "A shape, not a forecast."]))
    desc = ("A chart of spend in dollars against tool steps k. The measured points at k 4, 8, 10, 12, 20 and 30 are $0.001649, $0.003585, "
            "$0.004748, $0.006041, $0.012513 and $0.023528 and form an upward bend. A dashed straight line fitted through k 4, 8 and 12 "
            "reaches only $0.015836 at k 30, about a third too low. Side panels: 3 times the steps costs 4.96 times; "
            "the re-sent history is 38 percent of the bill at k 10 and 64 percent at k 30. Numbers from budget.py and budget2.py, Week 29.")
    return "fig-w29-2-bill-bends-upward.svg", svg_doc(
        WIDE, "Doubling the steps more than doubles the bill, because the history is paid for again", desc, J(o))


# ------------------------------------------------------------------ W30-1
def w30_1():
    cats = [("greeting", 6, 1.000, 0.833, True), ("refund", 7, 0.714, 0.857, False),
            ("technical", 7, 0.571, 0.714, False), ("billing", 5, 1.000, 0.800, True),
            ("out_of_scope", 5, 1.000, 0.200, True), ("OVERALL", 30, 0.833, 0.700, True)]
    x0, sc = 210, 300.0
    o = [title("The average hides where it got worse")]
    o.append(rect(40, 62, 16, 14, 3, HUMAN_F, HUMAN_S, 2))
    o.append(t(62, 70, "keyword rules (free)", 12, INK, central=True))
    o.append(rect(240, 62, 16, 14, 3, MODEL_F, MODEL_S, 2))
    o.append(t(262, 70, "TF-IDF + logistic regression (trained)", 12, INK, central=True))
    o.append(line(x0, 84, x0, 328, INK, 2))
    for i, (c, n, b, a, reg) in enumerate(cats):
        y = 90 + i * 38 + (8 if i == 5 else 0)
        if i == 5:
            o.append(line(30, y - 6, 770, y - 6, GRID, 1.5))
        o.append(t(x0 - 12, y + 16, "%s (n=%d)" % (c, n), 14, INK, "end", central=True))
        o.append(rect(x0, y, b * sc, 15, 3, HUMAN_F, HUMAN_S, 2))
        o.append(t(x0 + b * sc + 8, y + 8, "rules %.3f" % b, 12, INK, central=True))
        o.append(rect(x0, y + 17, a * sc, 15, 3, MODEL_F, MODEL_S, 2))
        o.append(t(x0 + a * sc + 8, y + 25, "trained %.3f" % a, 12, INK, central=True))
        if reg:
            o.append(cross(630, y + 16, 7, BAD_S))
            o.append(t(646, y + 16, "REGRESSION", 12, BAD_S, central=True))
    o.append(caption(["30 frozen eval tickets, scored once each. Overall 0.833 &#8594; 0.700 (&#8722;0.133),", "but out_of_scope fell 1.000 &#8594; 0.200 (&#8722;0.800)."]))
    desc = ("Paired horizontal bars of accuracy on 30 frozen tickets, keyword rules versus a trained TF-IDF classifier. "
            "Greeting 1.000 to 0.833, refund 0.714 to 0.857, technical 0.571 to 0.714, billing 1.000 to 0.800, out_of_scope 1.000 to 0.200, "
            "overall 0.833 to 0.700. Greeting, billing, out_of_scope and overall are marked REGRESSION with a cross. Numbers from p10_compare.py, Week 30.")
    return "fig-w30-1-average-hides-regressions.svg", svg_doc(
        WIDE, "Read every category, not just the average", desc, J(o))


# ------------------------------------------------------------------ W30-2
def w30_2():
    o = [title("Agreement beyond luck: Cohen's kappa")]
    gx, gy, cw, ch = 150, 120, 110, 70
    o.append(t(gx + cw, 100, "H (strict) says", 12, MUT, "middle"))
    o.append(t(gx + cw / 2, 114, "pass", 14, INK, "middle"))
    o.append(t(gx + cw * 1.5, 114, "fail", 14, INK, "middle"))
    o.append(t(gx - 10, gy + ch / 2, "J pass", 14, INK, "end", central=True))
    o.append(t(gx - 10, gy + ch * 1.5, "J fail", 14, INK, "end", central=True))
    cells = [(0, 0, 7, True), (1, 0, 7, False), (0, 1, 0, False), (1, 1, 6, True)]
    for cx_, cy_, v, agree in cells:
        x, y = gx + cx_ * cw, gy + cy_ * ch
        if agree:
            o.append(sq(x, y, cw, ch, OK_F, OK_S, 3))
            o.append(tick(x + 18, y + 18, 8, OK_S))
        elif v == 0:
            o.append(sq(x, y, cw, ch, PANEL, GRID, 2))
            o.append(cross(x + 18, y + 18, 6, MUT))
        else:
            o.append(sq(x, y, cw, ch, BAD_F, BAD_S, 3))
            o.append(cross(x + 18, y + 18, 6, BAD_S))
        o.append(t(x + cw / 2, y + ch / 2, str(v), 18, INK, "middle", central=True))
    o.append(t(gx + cw, gy + 2 * ch + 24, "20 replies; green = they agree", 12, MUT, "middle"))
    o.append(t(gx + cw, gy + 2 * ch + 42, "the empty cell: J never fails what H passes", 12, MUT, "middle"))
    # steps
    sx = 420
    steps = [("1", "they agreed", "(7 + 6) &#247; 20 = 0.65"),
             ("2", "luck alone would agree", "0.70 &#215; 0.35 + 0.30 &#215; 0.65 = 0.44"),
             ("3", "kappa, the part above luck", "(0.65 &#8722; 0.44) &#247; (1 &#8722; 0.44) = 0.375")]
    for i, (n, lab, arith) in enumerate(steps):
        y = 82 + i * 60
        hot = i == 2
        o.append(rect(sx, y, 360, 54, 10, ACC_F if hot else PANEL, ACC_S if hot else INK, 3 if hot else 2))
        o.append(ring_num(sx + 22, y + 27, n))
        o.append(t(sx + 44, y + 20, lab, 14, MUT))
        o.append(t(sx + 44, y + 42, arith, 14, INK))
    o.append(rect(420, 268, 360, 62, 10, PAPER, GRID, 2, "6 4"))
    o.append(t(432, 292, "a judge that says pass to everything", 14, MUT))
    o.append(t(432, 316, "agrees 18 &#247; 20 = 0.90, kappa = 0.0", 14, INK))
    o.append(caption(["The same 20 replies: raw agreement 0.65, kappa 0.375.", "A judge that never looks scores 0.90 agreement and kappa 0."]))
    desc = ("A two by two grid of 20 replies marked pass or fail by a strict rater H and a lenient rater J. Both pass 7, J pass and H fail 7, "
            "J fail and H pass 0, both fail 6. Three numbered steps: agreement (7 plus 6) over 20 is 0.65; agreement by luck 0.70 times 0.35 plus 0.30 times 0.65 is 0.44; "
            "kappa is 0.65 minus 0.44 over 1 minus 0.44, which is 0.375. A box notes that a judge who always says pass agrees 0.90 with a person passing 18 of 20 but has kappa 0. "
            "Numbers from p6_kappa.py and p7_constant.py, Week 30.")
    return "fig-w30-2-kappa-beyond-luck.svg", svg_doc(
        WIDE, "Two raters can agree a lot and still agree no more than luck", desc, J(o))


FIGS = [w28_1, w28_2, w29_1, w29_2, w30_1, w30_2]


def emit_b10():
    names = []
    for f in FIGS:
        name, svg = f()
        open(os.path.join(HERE, name), "w").write(svg + "\n")
        names.append(name)
    return names


if __name__ == "__main__":
    print("\n".join(emit_b10()))
