"""EVALUATION motifs: the confusion matrix and its overlays, ROC, splits, leakage.

Counts are the Module 3 spam example, verified: TN=75, FP=5, FN=4, TP=16 out of 100.
  precision = 16 / 21 = 0.7619   recall = 16 / 20 = 0.8000
ROC points are the Module 3 threshold sweep over ten ranked predictions.
Split counts are the Module 1 example: 2000 rows -> 1200 / 400 / 400.
"""
from _gen_core import *
import _gen_net  # noqa: F401  (registers the network motifs first)

_TICK = lambda x, y: poly("%s,%s %s,%s %s,%s" % (x, y + 6, x + 6, y + 12, x + 18, y),
                          "none", OK_S, 3)
_CROSS = lambda x, y: ('<g stroke="%s" stroke-width="3" stroke-linecap="round">\n  %s\n  %s\n  </g>'
                       % (BAD_S, line(x, y, x + 14, y + 12, BAD_S, 3),
                          line(x + 14, y, x, y + 12, BAD_S, 3)))


def _matrix(col2_header, row2_header, tags, counts_y):
    """The shared 2x2 skeleton: cells, border, glyphs, headers. 120x64 cells at (120,96)."""
    return [t(180, 84, "predicted ham", 12, MUT, "middle"),
            col2_header,
            t(114, 128, "actual ham", 12, MUT, "end"),
            row2_header,
            sq(120, 96, 120, 64, OK_F, INK, 2),
            sq(240, 96, 120, 64, BAD_F, INK, 2),
            sq(120, 160, 120, 64, BAD_F, INK, 2),
            sq(240, 160, 120, 64, OK_F, INK, 2),
            _TICK(128, 104), _CROSS(248, 104), _CROSS(128, 104 + 64), _TICK(248, 168),
            t(180, 124, tags[0], 12, INK, "middle"),
            t(300, 124, tags[1], 12, INK, "middle"),
            t(180, 188, tags[2], 12, INK, "middle"),
            t(300, 188, tags[3], 12, INK, "middle"),
            t(180, counts_y[0], "75", 24, INK, "middle"),
            t(300, counts_y[0], "5", 24, INK, "middle"),
            t(180, counts_y[1], "4", 24, INK, "middle"),
            t(300, counts_y[1], "16", 24, INK, "middle"),
            rect(120, 96, 240, 128, 0, "none", INK, 3)]


# ================================================================== confusion matrix
M("motif-confusion", "The confusion matrix: all four numbers named",
  "A two by two table. Rows are what actually happened, columns are what the model said. Top left, "
  "True Negative, 75, with a tick. Top right, False Positive, 5, with a cross. Bottom left, False "
  "Negative, 4, with a cross. Bottom right, True Positive, 16, with a tick.",
  "0 0 380 260",
  J(t(240, 44, "100 emails: 80 ham, 20 spam", 12, MUT, "middle"),
    _matrix(t(300, 84, "predicted spam", 12, MUT, "middle"),
            t(114, 192, "actual spam", 12, MUT, "end"),
            ("True Negative", "False Positive", "False Negative", "True Positive"),
            (150, 214)),
    t(190, 246, "one accuracy number hides three of these", 12, MUT, "middle")),
  "Name all four cells in words and put a tick or a cross in each &mdash; the diagonal is not obvious "
  "to a beginner. Rows are ACTUAL, columns are PREDICTED, class 0 first, which is sklearn's order.")

# ================================================================== precision overlay
M("motif-precision-overlay", "Precision reads down the predicted-spam column",
  "The same two by two table of 75, 5, 4 and 16. A pink outline surrounds the whole predicted-spam "
  "column, whose header now reads predicted spam, 21. Underneath: of the 21 I flagged, 16 were spam, "
  "and 16 divided by 21 equals 0.7619.",
  "0 0 380 280",
  J(t(240, 44, "100 emails &#183; threshold 0.50", 12, MUT, "middle"),
    _matrix(t(300, 84, "predicted spam (21)", 12, ACC_S, "middle"),
            t(114, 192, "actual spam", 12, MUT, "end"),
            ("TN", "FP", "FN", "TP"), (152, 216)),
    rect(240, 96, 120, 128, 0, "none", ACC_S, 3),
    t(190, 246, "precision: of the 21 I flagged, 16 were spam", 12, MUT, "middle"),
    t(190, 268, "16 &#247; 21 = 0.7619", 14, INK, "middle")),
  "Precision and recall are the SAME four numbers read in two directions. Keep the table identical "
  "between the two overlays so only the outlined region moves.")

# ================================================================== recall overlay
M("motif-recall-overlay", "Recall reads across the actual-spam row",
  "The same two by two table of 75, 5, 4 and 16. A pink outline surrounds the whole actual-spam row, "
  "whose label now reads actual spam, 20. Underneath: of the 20 real spam, I caught 16, and 16 divided "
  "by 20 equals 0.8000.",
  "0 0 380 280",
  J(t(240, 44, "100 emails &#183; threshold 0.50", 12, MUT, "middle"),
    _matrix(t(300, 84, "predicted spam", 12, MUT, "middle"),
            t(114, 192, "actual spam (20)", 12, ACC_S, "end"),
            ("TN", "FP", "FN", "TP"), (152, 216)),
    rect(120, 160, 240, 64, 0, "none", ACC_S, 3),
    t(190, 246, "recall: of the 20 real spam, I caught 16", 12, MUT, "middle"),
    t(190, 268, "16 &#247; 20 = 0.8000", 14, INK, "middle")),
  "The outlined ROW, against precision's outlined COLUMN. Show the pair together or neither: the "
  "lesson is the contrast.")

# ================================================================== ROC
_RX = lambda f: round(60 + 200.0 * f, 1)
_RY = lambda tp: round(250 - 200.0 * tp, 1)
_ROC = [(0, 0), (0, .2), (0, .4), (.2, .4), (.2, .6), (.2, .8), (.4, .8),
        (.4, 1), (.6, 1), (.8, 1), (1, 1)]
_roc_pts = " ".join("%s,%s" % (_RX(f), _RY(tp)) for f, tp in _ROC)
_MARKS = ((_RX(0), _RY(.4), "1", 76, 166, "t = 0.90"),
          (_RX(.2), _RY(.8), "2", 116, 86, "t = 0.50"),
          (_RX(.8), _RY(1), "3", 232, 68, "t = 0.20"))

M("motif-roc", "One ROC curve, three thresholds marked",
  "A staircase curve climbing from the bottom-left corner to the top-right of a square, well above the "
  "dashed diagonal marked chance. Three points on it are ringed and numbered 1, 2 and 3, labelled "
  "t = 0.90, t = 0.50 and t = 0.20. The axes are false positive rate and true positive rate.",
  "0 0 300 300",
  J(line(60, 250, 260, 50, GRID, 1.5, dash="6 5", cap=False),
    t(206, 116, "chance", 12, MUT),
    poly(_roc_pts, "none", DATA_S, 3),
    line(60, 40, 60, 250, INK, 2, cap=False),
    line(60, 250, 270, 250, INK, 2, cap=False),
    [t(52, y, s, 12, MUT, "end") for y, s in ((254, "0"), (154, "0.5"), (54, "1"))],
    [t(x, 268, s, 12, MUT, "middle") for x, s in ((60, "0"), (160, "0.5"), (260, "1"))],
    [circ(x, y, 9, ACC_F, ACC_S, 3) for x, y, _n, _lx, _ly, _lt in _MARKS],
    [t(x, y, n, 12, INK, "middle", central=True) for x, y, n, _lx, _ly, _lt in _MARKS],
    [t(lx, ly, lt, 12, INK) for _x, _y, _n, lx, ly, lt in _MARKS],
    t(165, 286, "false positive rate", 12, MUT, "middle"),
    trot(26, 145, "true positive rate", 12, MUT, "middle")),
  "The curve is one model; each dot is one THRESHOLD on that model. Number the dots so they can be "
  "matched to the confusion matrices printed beside them (see pattern-annotated-chart).")

# ================================================================== three-way split
M("motif-split-three", "One split, three piles, three jobs",
  "A single wide bar cut into three: a large train segment holding 1200, then a validation segment "
  "holding 400, then a test segment holding 400, labelled 60 percent, 20 percent and 20 percent. Below, "
  "three colour-keyed lines give each pile its one job.",
  "0 0 400 240",
  J([t(x, 42, s, 14, INK, "middle") for x, s in ((132, "train"), (268, "validation"), (336, "test"))],
    [line(x, 46, x, 58, MUT, 1.5, cap=False) for x in (132, 268, 336)],
    sq(30, 60, 204, 44, DATA_F, INK, 2),
    sq(234, 60, 68, 44, HUMAN_F, INK, 2),
    sq(302, 60, 68, 44, ACC_F, INK, 2),
    rect(30, 60, 340, 44, 8, "none", INK, 3),
    t(132, 82, "1200", 18, INK, "middle", central=True),
    t(268, 82, "400", 18, INK, "middle", central=True),
    t(336, 82, "400", 18, INK, "middle", central=True),
    [t(x, 124, s, 12, MUT, "middle") for x, s in ((132, "60%"), (268, "20%"), (336, "20%"))],
    bracket(30, 370, 136, 8, MUT, down=True),
    t(200, 162, "2000 rows in all", 12, MUT, "middle"),
    rect(30, 176, 12, 12, 3, DATA_F, DATA_S, 2),
    t(48, 186, "train &#8212; fit the model on this", 12, INK),
    rect(30, 194, 12, 12, 3, HUMAN_F, HUMAN_S, 2),
    t(48, 204, "validation &#8212; choose options, again and again", 12, INK),
    rect(30, 212, 12, 12, 3, ACC_F, ACC_S, 2),
    t(48, 222, "test &#8212; open once, at the very end", 12, INK)),
  "Segment widths must be to scale and the counts must add up to the printed total &mdash; a learner "
  "will check. Validation is amber because it is where a PERSON makes choices; test is accent pink "
  "because it is the pile you must not touch.")

# ================================================================== leakage pair
def _leak(badge, heading, box2_fill, box2_stroke, l1, l2, note):
    return J(badge,
             t(56, 32, heading, 14, INK),
             rect(40, 52, 220, 34, 8, PAPER, INK, 2),
             t(150, 69, "all 2000 rows", 12, INK, "middle", central=True),
             arrow(150, 86, 150, 106, INK, 2.5),
             rect(40, 110, 220, 52, 10, box2_fill, box2_stroke, 3),
             t(150, 130, l1, 12, INK, "middle"),
             t(150, 148, l2, 12, INK, "middle"),
             arrow(150, 162, 150, 182, INK, 2.5),
             rect(40, 186, 130, 34, 8, DATA_F, DATA_S, 3),
             t(105, 203, "train 1600", 12, INK, "middle", central=True),
             rect(180, 186, 80, 34, 8, ACC_F, ACC_S, 3),
             t(220, 203, "test 400", 12, INK, "middle", central=True),
             t(150, 242, note, 12, MUT, "middle"))


M("motif-leakage-wrong", "The leaking pipeline: scale first, split second",
  "A column of three boxes. All 2000 rows flow into a red box reading fit the scaler on all 2000 rows, "
  "and split afterwards, which then flows into a train pile of 1600 and a test pile of 400. The note "
  "underneath reads the mean has already seen the test rows.",
  "0 0 300 250",
  _leak(badge_cross(20, 14, 0.28), "the wrong order", BAD_F, BAD_S,
        "fit the scaler on all 2000", "rows, and split afterwards",
        "the mean has already seen the test rows"),
  "Half of a pair; never publish it without motif-leakage-right beside it. The arrow ORDER is the "
  "whole lesson, so keep the boxes in a vertical column where order is unmissable.")

M("motif-leakage-right", "The clean pipeline: split first, fit second",
  "The same column of three boxes. All 2000 rows flow into a green box reading split first, then fit "
  "the scaler on the train rows only, which then flows into a train pile of 1600 and a test pile of "
  "400. The note underneath reads the test rows never touched the mean.",
  "0 0 300 250",
  _leak(badge_check(20, 14, 0.28), "the right order", OK_F, OK_S,
        "split first, then fit the scaler", "on the train rows only",
        "the test rows never touched the mean"),
  "Geometry identical to motif-leakage-wrong, down to the pixel. Only the middle box's words and "
  "colour change, so the eye lands on the one thing that differs.")
