"""The seven Level 3 composition patterns, plus the two hard-rule worked examples."""
import math
from _gen_core import *
import _gen_term  # noqa: F401  (registers every motif)

BY_ID = {m["id"]: m for m in MOTIFS}
PATTERNS = []


def place(mid, x, y, s=1):
    tr = "translate(%s,%s)" % (x, y) + ("" if s == 1 else " scale(%s)" % s)
    return '<g transform="%s">\n%s\n  </g>' % (tr, BY_ID[mid]["body"])


def P(pid, title, desc, vb, note, body):
    PATTERNS.append(dict(id=pid, title=title, desc=desc, vb=vb, note=note, body=body.strip("\n")))


def polyg(pts, fill="none", stroke=GRID, sw=1.5):
    s = " ".join("%.1f,%.1f" % p for p in pts)
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"/>' % (s, fill, stroke, sw))


def ellipse_pts(cx, cy, rx, ry, n=36):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n))
            for i in range(n)]


# ============================================================ 1. pipeline
# scale() scales type too, so every stage glyph here is TEXT-FREE; the words live
# in the 18px stage label underneath.
GLYPH_SPLIT3 = "\n    ".join([
    sq(6, 40, 72, 34, DATA_F, INK, 2),
    sq(78, 40, 24, 34, HUMAN_F, INK, 2),
    sq(102, 40, 24, 34, ACC_F, INK, 2),
    rect(6, 40, 120, 34, 6, "none", INK, 3),
    line(78, 28, 78, 86, ACC_S, 2, dash="5 4", cap=False),
    line(102, 28, 102, 86, ACC_S, 2, dash="5 4", cap=False)])

GLYPH_ENGINEER = "\n    ".join([
    sq(4, 30, 44, 60, PAPER, INK, 2),
    line(4, 50, 48, 50, GRID, 1.5, cap=False),
    line(4, 70, 48, 70, GRID, 1.5, cap=False),
    arrow(54, 60, 74, 60, INK, 2.5),
    sq(80, 30, 48, 60, DATA_F, DATA_S, 3),
    sq(112, 30, 16, 60, ACC_F, ACC_S, 2),
    line(80, 50, 128, 50, GRID, 1.5, cap=False),
    line(80, 70, 128, 70, GRID, 1.5, cap=False)])

_fall = [(20, 24), (34, 50), (48, 66), (62, 76), (78, 83), (94, 87), (110, 89)]
GLYPH_LOSSFALL = "\n    ".join(
    [line(14, 14, 14, 96, INK, 2, cap=False), line(14, 96, 124, 96, INK, 2, cap=False),
     poly(" ".join("%s,%s" % p for p in _fall), "none", MODEL_S, 3)]
    + [dot(x, y, 4, MODEL_S) for x, y in _fall])

GLYPH_MATRIX = "\n    ".join([
    sq(16, 20, 50, 40, OK_F, INK, 2), sq(66, 20, 50, 40, BAD_F, INK, 2),
    sq(16, 60, 50, 40, BAD_F, INK, 2), sq(66, 60, 50, 40, OK_F, INK, 2),
    poly("28,38 34,44 50,28", "none", OK_S, 4),
    poly("78,30 96,48", "none", BAD_S, 4), poly("96,30 78,48", "none", BAD_S, 4),
    poly("28,70 46,88", "none", BAD_S, 4), poly("46,70 28,88", "none", BAD_S, 4),
    poly("78,78 84,84 100,68", "none", OK_S, 4),
    rect(16, 20, 100, 80, 0, "none", INK, 3)])

_STAGES = ((30, DATA_S, GLYPH_SPLIT3, 106, "1. Split", "three ways, first of all"),
           (222, ACC_S, GLYPH_ENGINEER, 298, "2. Engineer", "fit on train rows only"),
           (414, MODEL_S, GLYPH_LOSSFALL, 490, "3. Fit", "watch the loss fall"),
           (606, OK_S, GLYPH_MATRIX, 682, "4. Measure", "four numbers, not one"))
_pl = ["  " + t(400, 46, "The Level 3 pipeline: split, engineer, fit, measure", 24, INK, "middle")]
for _x, _st, _gl, _cx, _a, _b in _STAGES:
    _pl.append("  " + rect(_x, 96, 152, 190, 12, PAPER, _st, 3))
for _x in (183, 375, 567):
    _pl.append('  <g transform="translate(%s,182) scale(0.4)">\n%s\n  </g>' % (_x, BY_ID["motif-arrow"]["body"]))
for _x, _st, _gl, _cx, _a, _b in _STAGES:
    _pl.append('  <g transform="translate(%s,130)">\n    %s\n  </g>' % (_x + 10, _gl))
for _x, _st, _gl, _cx, _a, _b in _STAGES:
    _pl.append("  " + t(_cx, 312, _a, 18, INK, "middle"))
    _pl.append("  " + t(_cx, 332, _b, 12, MUT, "middle"))
_pl.append("  " + t(400, 372, "Stage 2 is where leakage happens. Stage 4 is where you find out.",
                    14, MUT, "middle"))

P("pattern-pipeline", "The Level 3 pipeline: split, engineer, fit, measure",
  "Four numbered stages left to right: cut the data three ways into train, validation and test; build "
  "features fitting only on the train rows; train while the loss curve falls; and measure with a two by "
  "two matrix of ticks and crosses.",
  "0 0 800 400",
  "Four equal boxes, arrows in the gaps, a NUMBER on every stage so the order survives greyscale. "
  "Stage colours run data &rarr; accent &rarr; model &rarr; correct: the data, the danger, the learned "
  "thing, the verdict. The stage glyphs carry NO text, because a motif's own 12px labels would fall "
  "under the floor at this size &mdash; the words live in the 18px stage label.",
  "\n".join(_pl))

# ============================================================ 2. before / after
def _surface(cx, cy, radii, walk, colour):
    out = []
    for rx, ry in radii:
        out.append("  " + polyg(ellipse_pts(cx, cy, rx, ry), "none", GRID, 1.5))
    for i in range(len(walk) - 1):
        out.append("  " + arrow(walk[i][0], walk[i][1], walk[i + 1][0], walk[i + 1][1], colour, 2.5))
    for x, y in walk:
        out.append("  " + dot(x, y, 5, colour))
    return "\n".join(out)


_CANYON = [(100, 158), (128, 238), (156, 166), (180, 232), (198, 186), (210, 204)]
_ROUND = [(510, 130), (546, 158), (568, 178), (581, 191), (590, 200)]
_ba = ["  " + t(400, 46, "The same descent, before and after scaling", 24, INK, "middle"),
       "  " + line(400, 80, 400, 336, GRID, 1.5, dash="6 6", cap=False),
       "  " + rect(30, 80, 360, 240, 12, BAD_F, BAD_S, 3),
       "  " + rect(410, 80, 360, 240, 12, OK_F, OK_S, 3),
       "  " + badge_cross(48, 94, 0.42),
       "  " + badge_check(428, 94, 0.42),
       "  " + t(104, 128, "Before", 18, INK),
       "  " + t(484, 128, "After", 18, INK),
       _surface(210, 200, ((150, 34), (110, 25), (70, 16)), _CANYON, BAD_S),
       _surface(590, 200, ((100, 90), (70, 63), (38, 34)), _ROUND, OK_S),
       "  " + t(210, 268, "the steps bounce across the canyon", 12, MUT, "middle"),
       "  " + t(590, 268, "the steps go straight to the bottom", 12, MUT, "middle"),
       "  " + t(210, 300, "one feature 0&#8211;1, another 0&#8211;100000", 12, MUT, "middle"),
       "  " + t(590, 300, "both features scaled to about the same size", 12, MUT, "middle"),
       "  " + t(400, 360, "Scaling does not change the model. It changes the shape of the hill.",
                14, MUT, "middle")]

P("pattern-before-after", "The same descent, before and after scaling",
  "Two mirrored panels. The left panel is marked wrong: the contour rings are stretched into a long thin "
  "canyon and the descent path bounces from wall to wall. The right panel is marked correct: the same "
  "contours are round and the descent path runs straight to the middle.",
  "0 0 800 400",
  "Mirror the geometry EXACTLY so the eye only has to find the one difference. The tick and cross "
  "badges, not the panel colour, say which side is which. One change per figure &mdash; if you changed "
  "two things, draw two figures.",
  "\n".join(_ba))

# ============================================================ 3. three-panel progression
_pr = ["  " + t(400, 42, "Same bowl. Three learning rates.", 24, INK, "middle")]
for _cx, _px, _st, _mid, _h, _f in (
        (149, 32, BAD_S, "motif-lr-too-small", "1. Too small", "loss 9.00 &#8594; 7.97 in 3 steps"),
        (400, 283, OK_S, "motif-lr-right", "2. Just right", "loss 9.00 &#8594; 1.51 in 4 steps"),
        (651, 534, BAD_S, "motif-lr-diverging", "3. Diverging", "loss 9.00 &#8594; 18.66 and rising")):
    _pr.append("  " + t(_cx, 68, _h, 18, INK, "middle"))
    _pr.append("  " + rect(_px, 76, 234, 240, 12, PAPER, _st, 3))
    _pr.append("  " + place(_mid, _px + 9, 86, 1.2))
    _pr.append("  " + t(_cx, 336, _f, 12, MUT, "middle"))
_pr.append("  " + t(400, 372, "The bowl never changes. Only your stride length does.", 14, MUT, "middle"))

P("pattern-progression", "Same bowl, three learning rates",
  "Three panels side by side over the identical bowl-shaped curve. Panel 1's four dots barely separate. "
  "Panel 2's five dots walk steadily to the bottom. Panel 3's dots leap across the bowl and land higher "
  "each time.",
  "0 0 800 400",
  "Three equal panels, numbered, with IDENTICAL data in each. The numbers carry the progression; the "
  "panel colour only says good or bad. Too-small and diverging are both wrong-red, told apart by the "
  "SHAPE of the walk. The embedded motifs sit at scale 1.2, never below 1.0.",
  "\n".join(_pr))

# ============================================================ 4. annotated chart
_SWEEP = (("1", "t = 0.90", "5", "0", "3", "2"),
          ("2", "t = 0.50", "4", "1", "1", "4"),
          ("3", "t = 0.20", "1", "4", "0", "5"))


def _mini_matrix(x0, y0, n, label, tn, fp, fn, tp):
    out = [circ(x0 + 12, y0 + 36, 11, ACC_F, ACC_S, 3),
           t(x0 + 12, y0 + 36, n, 12, INK, "middle", central=True),
           t(x0 + 32, y0 - 8, label, 12, INK)]
    cells = ((0, 0, OK_F, "TN", tn), (1, 0, BAD_F, "FP", fp),
             (0, 1, BAD_F, "FN", fn), (1, 1, OK_F, "TP", tp))
    for c, r, fill, tag, val in cells:
        cx, cy = x0 + 32 + 40 * c, y0 + 34 * r
        out.append(sq(cx, cy, 40, 34, fill, INK, 2))
        out.append(t(cx + 20, cy + 13, tag, 12, MUT, "middle"))
        out.append(t(cx + 20, cy + 29, val, 14, INK, "middle"))
    out.append(rect(x0 + 32, y0, 80, 68, 0, "none", INK, 3))
    return "\n  ".join(out)


_ac = ["  " + t(250, 40, "One model, three thresholds", 24, INK, "middle"),
       "  " + place("motif-roc", 100, 56)]
for _i, (_n, _lab, _tn, _fp, _fn, _tp) in enumerate(_SWEEP):
    _ac.append("  " + _mini_matrix(40 + 152 * _i, 376, _n, _lab, _tn, _fp, _fn, _tp))
_ac += ["  " + t(250, 458, "rows: actual &#183; columns: predicted", 12, MUT, "middle"),
        "  " + t(250, 476, "The threshold decides which mistakes you make.", 14, MUT, "middle")]

P("pattern-annotated-chart", "One model, three thresholds",
  "An ROC curve with three points ringed and numbered 1, 2 and 3, labelled t = 0.90, t = 0.50 and "
  "t = 0.20. Beneath it, three matching numbered two by two matrices give the four counts at each of "
  "those thresholds.",
  "0 0 500 500",
  "The chart and the tables are matched by NUMBER, not by a leader line &mdash; three leaders across a "
  "chart would cross the curve. Every mark on the curve that you name must have its numbers printed "
  "somewhere on the same page, or the reader cannot check you.",
  "\n".join(_ac))

# ============================================================ 5. tensor / shape trace
def _runs(x0, y, parts):
    out, x = [], x0
    for txt, hot in parts:
        w = len(txt) * 8.4
        if hot:
            out.append(rect(x - 3, y - 16, w + 6, 22, 4, ACC_F, ACC_S, 2))
        out.append(t(x, y, txt, 14, INK, mono=True))
        x += w + 4
    return "\n  ".join(out)


_st = ["  " + t(400, 46, "Follow the shapes through one forward pass", 24, INK, "middle"),
       "  " + path("M106 206 V262 H244 V206", "none", ACC_S, 2, dash="6 4"),
       "  " + path("M424 206 V262 H558 V206", "none", ACC_S, 2, dash="6 4"),
       "  " + rect(25, 130, 130, 120, 10, DATA_F, DATA_S, 3),
       "  " + rect(185, 155, 120, 70, 10, MODEL_F, MODEL_S, 3),
       "  " + rect(335, 130, 130, 120, 10, DATA_F, DATA_S, 3),
       "  " + rect(495, 155, 120, 70, 10, MODEL_F, MODEL_S, 3),
       "  " + rect(645, 130, 130, 120, 10, OK_F, OK_S, 3),
       "  " + _runs(56, 196, [("(750,", False), ("2", True), (")", False)]),
       "  " + _runs(203, 196, [("W1 (", False), ("2", True), (", 16)", False)]),
       "  " + _runs(362, 196, [("(750, ", False), ("16", True), (")", False)]),
       "  " + _runs(513, 196, [("W2 (", False), ("16", True), (", 1)", False)]),
       "  " + t(710, 196, "(750, 1)", 14, INK, "middle", mono=True),
       "  " + t(170, 201, "&#215;", 18, INK, "middle"),
       "  " + t(320, 201, "=", 18, INK, "middle"),
       "  " + t(480, 201, "&#215;", 18, INK, "middle"),
       "  " + t(630, 201, "=", 18, INK, "middle"),
       "  " + t(90, 110, "one batch of rows", 12, MUT, "middle"),
       "  " + t(245, 110, "layer 1 weights", 12, MUT, "middle"),
       "  " + t(400, 110, "hidden activations", 12, MUT, "middle"),
       "  " + t(555, 110, "layer 2 weights", 12, MUT, "middle"),
       "  " + t(710, 110, "one number per row", 12, MUT, "middle"),
       "  " + t(175, 282, "these must match", 12, ACC_S, "middle"),
       "  " + t(491, 282, "and these", 12, ACC_S, "middle"),
       "  " + t(400, 332, "The batch size 750 rides along unchanged.", 14, MUT, "middle"),
       "  " + t(400, 372, "Read it out loud: 750 by 2, times 2 by 16, gives 750 by 16.", 14, MUT, "middle")]

P("pattern-structure", "Follow the shapes through one forward pass",
  "Five blocks in a row joined by multiplication and equals signs: 750 by 2, times W1 which is 2 by 16, "
  "equals 750 by 16, times W2 which is 16 by 1, equals 750 by 1. The pairs of inner numbers that have "
  "to agree are boxed in pink and joined underneath by dashed brackets.",
  "0 0 800 400",
  "One block per tensor, one shape per block, and the pairs that must agree boxed and joined. The "
  "vertical legs of the join run over a pale block fill, which is legal and reads cleanly at 2px "
  "dashed. Print the shapes in MONO so the digits line up; everything else stays sans.",
  "\n".join(_st))

# ============================================================ 6. matrix diagram
_mx = ["  " + t(400, 46, "One output cell, multiplied out in full", 24, INK, "middle"),
       "  " + t(120, 138, "one row of X", 12, MUT, "middle"),
       "  " + t(288, 118, "W1", 12, MUT, "middle"),
       "  " + t(456, 138, "one row of Z1", 12, MUT, "middle"),
       "  " + sq(60, 150, 60, 44, DATA_F, INK, 2),
       "  " + sq(120, 150, 60, 44, DATA_F, INK, 2),
       "  " + t(90, 172, "1.0", 14, INK, "middle", central=True),
       "  " + t(150, 172, "2.0", 14, INK, "middle", central=True),
       "  " + t(204, 178, "&#215;", 18, INK, "middle"),
       "  " + sq(228, 128, 60, 44, MODEL_F, INK, 2),
       "  " + sq(288, 128, 60, 44, MODEL_F, INK, 2),
       "  " + sq(228, 172, 60, 44, MODEL_F, INK, 2),
       "  " + sq(288, 172, 60, 44, MODEL_F, INK, 2),
       "  " + t(258, 150, "0.5", 14, INK, "middle", central=True),
       "  " + t(318, 150, "&#8722;0.3", 14, INK, "middle", central=True),
       "  " + t(258, 194, "0.8", 14, INK, "middle", central=True),
       "  " + t(318, 194, "0.2", 14, INK, "middle", central=True),
       "  " + t(372, 178, "=", 18, INK, "middle"),
       "  " + sq(396, 150, 60, 44, OK_F, INK, 2),
       "  " + sq(456, 150, 60, 44, OK_F, INK, 2),
       "  " + t(426, 172, "2.20", 14, INK, "middle", central=True),
       "  " + t(486, 172, "0.15", 14, INK, "middle", central=True),
       "  " + rect(60, 150, 120, 44, 0, "none", ACC_S, 3),
       "  " + rect(228, 128, 60, 88, 0, "none", ACC_S, 3),
       "  " + rect(396, 150, 60, 44, 0, "none", ACC_S, 3),
       "  " + chip(84, 210, 72, "(1, 2)", DATA_S),
       "  " + chip(252, 230, 72, "(2, 2)", MODEL_S),
       "  " + chip(420, 210, 72, "(1, 2)", OK_S),
       "  " + rect(224, 262, 128, 30, 8, MODEL_F, MODEL_S, 2),
       "  " + t(288, 277, "bias 0.10 and 0.05", 12, INK, "middle", central=True),
       "  " + rect(548, 120, 232, 140, 12, PAPER, ACC_S, 2),
       "  " + t(664, 148, "row &#215; column, term by term", 12, INK, "middle"),
       "  " + t(664, 172, "1.0 &#215; 0.5 = 0.50", 12, INK, "middle"),
       "  " + t(664, 192, "2.0 &#215; 0.8 = 1.60", 12, INK, "middle"),
       "  " + t(664, 212, "plus the bias 0.10", 12, INK, "middle"),
       "  " + t(664, 236, "0.50 + 1.60 + 0.10 = 2.20", 12, INK, "middle"),
       "  " + arrow(544, 176, 462, 174, ACC_S, 2),
       "  " + t(400, 332, "The pink row times the pink column lands in the pink cell.", 14, MUT, "middle"),
       "  " + t(400, 372, "A matrix multiply is just this, repeated for every row and column.", 14, MUT, "middle")]

P("pattern-matrix", "One output cell, multiplied out in full",
  "A one by two row of 1.0 and 2.0, a multiplication sign, a two by two block of 0.5, minus 0.3, 0.8 and "
  "0.2, an equals sign, and a one by two answer of 2.20 and 0.15. The row, the first column and the "
  "first answer cell are outlined in pink, and a callout beside them works the cell out: 1.0 times 0.5 "
  "is 0.50, 2.0 times 0.8 is 1.60, plus the bias 0.10, giving 2.20.",
  "0 0 800 400",
  "Outline the ROW you used, the COLUMN you used and the CELL you got, in the same accent, and print "
  "every multiplication. A matrix figure without arithmetic in it has taught nobody anything &mdash; "
  "see &sect;3.2.",
  "\n".join(_mx))

# ============================================================ 7. error and fix
_ef = ["  " + t(400, 42, "Read the shapes, fix the wiring, run again", 24, INK, "middle"),
       "  " + place("motif-traceback-shape", 16, 80),
       '  <g transform="translate(424,172) scale(0.5)">\n%s\n  </g>' % BY_ID["motif-arrow"]["body"],
       "  " + rect(478, 96, 292, 176, 10, PAPER, OK_S, 3),
       "  " + path("M478 106 A10 10 0 0 1 488 96 H760 A10 10 0 0 1 770 106 V126 H478 Z", OK_F, "none", 0),
       "  " + poly("492,112 498,118 510,104", "none", OK_S, 3),
       "  " + line(478, 126, 770, 126, INK, 2, cap=False),
       "  " + t(520, 116, "Terminal", 12, INK),
       "  " + t(494, 158, "&gt;", 14, MUT, mono=True),
       "  " + t(508, 158, "python train.py", 14, INK, mono=True),
       "  " + t(494, 186, "Z1 shape: (750, 16)", 14, INK, mono=True),
       "  " + t(494, 210, "loss 0.6931 -&gt; 0.2417", 14, INK, mono=True),
       "  " + t(494, 238, "&gt;", 14, MUT, mono=True),
       '  <rect x="508" y="226" width="9" height="14" fill="%s"/>' % INK,
       "  " + rect(478, 96, 292, 176, 10, "none", OK_S, 3),
       "  " + t(216, 320, "Before: it stopped", 18, INK, "middle"),
       "  " + t(624, 320, "After: it ran", 18, INK, "middle"),
       "  " + t(216, 342, "W1 was built as (16, 2), the wrong way round", 12, MUT, "middle"),
       "  " + t(624, 342, "one shape fixed &#8212; and the loss falls", 12, MUT, "middle"),
       "  " + t(400, 374, "The error names two shapes. Your job is to make them agree.", 14, MUT, "middle")]

P("pattern-error-fix", "Read the shapes, fix the wiring, run again",
  "On the left, a red-outlined traceback panel with the failing line highlighted and arrowed, ending in "
  "a ValueError that names the shapes 750 by 2 and 16 by 2. On the right, a green-outlined terminal "
  "running the same program and printing Z1 shape 750 by 16 and a loss falling from 0.6931 to 0.2417.",
  "0 0 800 400",
  "The failing artefact on the left, the working one on the right, an arrow between, a one-line "
  "diagnosis under each. Both panels sit at scale 1.0 &mdash; shrinking a terminal would drop its 12px "
  "mono text below the floor. The right panel must be the SAME program, so only one thing changed.",
  "\n".join(_ef))


# ============================================================ hard-rule worked examples
def _ex_header(bad, words):
    fill, stroke = (BAD_F, BAD_S) if bad else (OK_F, OK_S)
    badge = badge_cross(28, 24, 0.3) if bad else badge_check(28, 24, 0.3)
    return "\n  ".join([rect(20, 20, 460, 40, 10, fill, stroke, 3), badge,
                        t(74, 46, words, 14, INK)])


def _ex(eid, title, desc, body):
    return (eid, title,
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" role="img">\n'
            '  <title>%s</title>\n  <desc>%s</desc>\n  %s\n</svg>' % (title, desc, body))


# ---- pair A: code
_CODE_LINES = ("for epoch in range(500):", "    grad = X.T @ (p - y) / n",
               "    w -= lr * grad", "    history.append(loss(w))")
_bad_code = "\n  ".join(
    [_ex_header(True, "Do not do this &#8212; it is a picture of code"),
     rect(20, 80, 460, 170, 10, PANEL, GRID, 1.5)]
    + [t(40, 114 + 30 * i, s, 14, INK, mono=True) for i, s in enumerate(_CODE_LINES)]
    + [t(250, 276, "The reader learns nothing the code block did not already say.", 12, MUT, "middle")])

_MB = lambda w: round(320 + 22.0 * w, 1)
_MBY = lambda L: round(210 - 8.5 * L, 1)
_mbowl = " ".join("%s,%s" % (_MB(w * 0.425), _MBY((w * 0.425) ** 2)) for w in range(-8, 9))
_good_code = "\n  ".join([
    _ex_header(False, "Do this instead &#8212; it shows what the step DOES"),
    rect(20, 76, 460, 180, 12, PANEL, GRID, 1.5),
    line(236, 104, 236, 214, INK, 2, cap=False),
    line(236, 214, 420, 214, INK, 2, cap=False),
    poly(_mbowl, "none", DATA_S, 3),
    arrow(386, 133.5, 372.8, 161, ACC_S, 2.5),
    dot(386, 133.5, 6, ACC_S), dot(372.8, 161, 6, ACC_S),
    t(40, 120, "at w = 3 the slope is 6", 12, INK),
    t(40, 144, "step = 0.1 &#215; 6 = 0.6", 12, INK),
    t(40, 168, "3 &#8722; 0.6 = 2.4", 12, INK),
    t(40, 192, "loss 9.00 &#8594; 5.76", 12, OK_S),
    t(250, 276, "Same lesson, no code &#8212; and the arithmetic is checkable.", 12, MUT, "middle")])

# ---- pair B: formula
_bad_formula = "\n  ".join([
    _ex_header(True, "Do not do this &#8212; it is a picture of a formula"),
    rect(20, 80, 460, 170, 10, PANEL, GRID, 1.5),
    t(180, 150, "dL", 24, INK, "middle"),
    line(158, 162, 202, 162, INK, 2, cap=False),
    t(180, 186, "dw", 24, INK, "middle"),
    t(228, 170, "=", 24, INK, "middle"),
    t(268, 170, "2w", 24, INK, "middle"),
    t(250, 230, "no numbers, nothing to check, nothing to do", 12, MUT, "middle"),
    t(250, 276, "A reader who cannot already read this learns nothing from it.", 12, MUT, "middle")])

_good_formula = "\n  ".join([
    _ex_header(False, "Do this instead &#8212; it shows what the formula DOES"),
    rect(20, 76, 460, 180, 12, PANEL, GRID, 1.5),
    line(236, 104, 236, 214, INK, 2, cap=False),
    line(236, 214, 420, 214, INK, 2, cap=False),
    line(368.4, 174.3, 394.8, 113.1, ACC_S, 3),
    poly(_mbowl, "none", DATA_S, 3),
    circ(386, 133.5, 6, ACC_F, ACC_S, 3),
    t(378, 120, "w = 3", 12, INK, "end"),
    t(40, 112, "nudge w either side of 3:", 12, INK),
    t(40, 136, "loss(3.001) = 9.006001", 12, INK),
    t(40, 158, "loss(2.999) = 8.994001", 12, INK),
    line(38, 172, 196, 172, GRID, 1.5, cap=False),
    t(40, 190, "0.012 &#247; 0.002 = 6.000", 12, INK),
    t(40, 214, "that division IS the slope", 12, OK_S),
    t(250, 276, "Now the reader can check it, and see it is only a division.", 12, MUT, "middle")])

EXAMPLES = [
    _ex("example-bad-code-screenshot", "Wrong: a figure that is only a picture of code",
        "A grey panel containing four lines of Python about a gradient-descent loop, with no diagram, no "
        "arrows and no annotation.", _bad_code),
    _ex("example-good-mental-model", "Right: a figure that shows what one step does to the numbers",
        "A bowl-shaped curve with two dots on its right wall joined by an arrow, beside four lines of "
        "arithmetic: the slope at w equals 3 is 6, the step is 0.1 times 6 which is 0.6, 3 minus 0.6 is "
        "2.4, and the loss falls from 9.00 to 5.76.", _good_code),
    _ex("example-bad-formula-picture", "Wrong: a figure that is only a picture of a formula",
        "A grey panel containing the symbols d L over d w equals 2 w, set large, with no numbers, no "
        "curve and no annotation.", _bad_formula),
    _ex("example-good-formula-in-numbers", "Right: a figure that shows what the formula does to numbers",
        "A bowl-shaped curve with a straight line just touching it at the point where w is 3, beside the "
        "arithmetic: the loss at 3.001 is 9.006001, the loss at 2.999 is 8.994001, and 0.012 divided by "
        "0.002 is 6.000.", _good_formula)]
