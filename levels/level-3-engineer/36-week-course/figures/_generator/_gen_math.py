"""MATHS motifs: slope/tangent, the loss bowl with descent steps, learning rates.

Every number in this file is checkable arithmetic taken from Module 4:
  loss(w) = w**2 ; slope at w = 3 is 6 ; steps use w <- w - lr * slope.
"""
from _gen_core import *

# ================================================================== tangent
# f(w) = w**2 on axes.  w in [0,4] -> x = 40 + 58w ; loss in [0,16] -> y = 196 - 9.6L
_CX = lambda w: round(40 + 58.0 * w, 1)
_CY = lambda L: round(196 - 9.6 * L, 1)
_curve = " ".join("%s,%s" % (_CX(w / 2.0), _CY((w / 2.0) ** 2)) for w in range(0, 9))

M("motif-tangent", "The slope at one point on a curve",
  "A curve rising to the right. At the point where w is 3 and the loss is 9, a straight line just "
  "touches the curve. A small step of plus 0.5 across and plus 3.0 up is marked on that line, and a "
  "callout says 3.0 divided by 0.5 gives a slope of 6.",
  "0 0 320 240",
  J(line(40, 36, 40, 196, INK, 2, cap=False),
    line(40, 196, 286, 196, INK, 2, cap=False),
    # the tangent line, drawn under the curve so the curve reads as the subject
    line(167.6, 155.7, 260.4, 63.5, ACC_S, 3),
    poly(_curve, "none", DATA_S, 3),
    line(214, 109.6, 243, 109.6, MUT, 1.5, dash="5 4", cap=False),
    # the rise leg must stop on the TANGENT (loss 12.0 at w = 3.5), not on the curve
    # (which is at 12.25 there) -- otherwise the drawn triangle is +3.25, not +3.0.
    line(243, 109.6, 243, 80.8, MUT, 1.5, dash="5 4", cap=False),
    t(228.5, 124, "+0.5", 12, MUT, "middle"),
    t(249, 94, "+3.0", 12, MUT),
    circ(214, 109.6, 6, ACC_F, ACC_S, 3),
    t(206, 134, "(3, 9)", 12, INK, "end"),
    rect(46, 40, 150, 44, 10, PAPER, ACC_S, 2),
    t(121, 58, "3.0 &#247; 0.5 = 6", 14, INK, "middle"),
    t(121, 74, "so the slope here is 6", 12, MUT, "middle"),
    arrow(196, 66, 206, 100, ACC_S, 2),
    line(214, 196, 214, 202, MUT, 1.5, cap=False),
    t(214, 216, "w = 3", 12, MUT, "middle"),
    t(96, 216, "w (the weight)", 12, MUT, "middle"),
    trot(24, 116, "loss", 12, MUT, "middle"),
    t(300, 34, "loss = w &#215; w", 12, MUT, "end")),
  "The slope is not a symbol, it is a division: rise over run, both printed. Draw the tangent BEFORE "
  "the curve so the curve stays on top. Mark the point, print its coordinates.")

# ================================================================== loss bowl
# loss(w) = w**2, w in [-3.4, 3.4] -> x = 160 + 40w ; loss -> y = 200 - 13.8L
_BX = lambda w: round(160 + 40.0 * w, 1)
_BY = lambda L: round(200 - 13.8 * L, 1)
_bowl = " ".join("%s,%s" % (_BX(w / 5.0), _BY((w / 5.0) ** 2)) for w in range(-17, 18, 2))

# w <- w - 0.1 * 2w  (lr = 0.1)
_STEPS = [(3.0, 9.00), (2.4, 5.76), (1.92, 3.69), (1.54, 2.36)]
_sp = [(_BX(w), _BY(L)) for w, L in _STEPS]
_lab_y = (80, 116, 152, 188)

_body = [line(24, 200, 296, 200, GRID, 1.5, cap=False),
         poly(_bowl, "none", DATA_S, 3),
         t(210, 24, "each step moves 0.1 &#215; slope downhill", 12, MUT, "middle")]
for _i in range(3):
    _body.append(arrow(_sp[_i][0] - 3, _sp[_i][1] + 4, _sp[_i + 1][0] + 5,
                       _sp[_i + 1][1] - 3, ACC_S, 2.5))
for _i, ((_x, _y), (_w, _L)) in enumerate(zip(_sp, _STEPS)):
    _body.append(line(_x + 10, _y, 302, _lab_y[_i], GRID, 1.5, cap=False))
    _body.append(circ(_x, _y, 9, ACC_F, ACC_S, 3))
    _body.append(t(_x, _y, str(_i + 1), 12, INK, "middle", central=True))
    _body.append(t(306, _lab_y[_i] + 4, "(%.2f, %.2f)" % (_w, _L), 12, INK))
_body += [t(160, 216, "w = 0", 12, MUT, "middle"),
          t(160, 232, "the bottom: slope 0, nowhere left to go", 12, MUT, "middle")]

M("motif-loss-bowl", "Four steps down the loss bowl",
  "A bowl-shaped curve. Four numbered points walk down the right-hand wall towards the bottom, each "
  "one labelled with its own w and loss: 3.00 and 9.00, then 2.40 and 5.76, then 1.92 and 3.69, then "
  "1.54 and 2.36. The bottom of the bowl is marked as the place where the slope is zero.",
  "0 0 420 250", J(_body),
  "Number every step and print BOTH its coordinates. The steps must get shorter as the wall flattens "
  "&mdash; that is the whole behaviour, and a reader can check it against the printed numbers.")

# ================================================================== learning rate trio
# Shared mini-bowl: w in [-4.6, 4.6] -> x = 90 + 15.2w ; loss -> y = 130 - 4.1L
_MX = lambda w: round(90 + 15.2 * w, 1)
_MY = lambda L: round(130 - 4.1 * L, 1)
_mini = " ".join("%s,%s" % (_MX(w * 1.15), _MY((w * 1.15) ** 2)) for w in range(-4, 5))


def _lr_panel(walk, lr, verdict, colour):
    pts = [(_MX(w), _MY(w * w)) for w in walk]
    b = [line(20, 36, 20, 130, INK, 2, cap=False),
         line(20, 130, 160, 130, INK, 2, cap=False),
         poly(_mini, "none", GRID, 3),
         trot(12, 84, "loss", 12, MUT, "middle"),
         t(155, 126, "w", 12, MUT, "end")]
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        b.append(arrow(x1, y1, x2, y2, colour, 2.5))
    for x, y in pts:
        b.append(dot(x, y, 5, colour))
    b.append(t(90, 148, "lr = %s" % lr, 14, INK, "middle"))
    b.append(t(90, 162, verdict, 12, MUT, "middle"))
    return J(b)


M("motif-lr-too-small", "A learning rate that is too small",
  "The same bowl-shaped curve. Four dots sit almost on top of each other high on the right-hand wall, "
  "joined by arrows so short they are hard to see. The caption reads lr = 0.01, barely moves.",
  "0 0 180 175",
  _lr_panel([3.0, 2.94, 2.8812, 2.8236], "0.01", "barely moves", DATA_S),
  "Panel 1 of 3. The bowl is IDENTICAL in all three panels and drawn in grid grey &mdash; only the "
  "walk changes. Four steps that barely separate is the picture of a learning rate too small.")

M("motif-lr-right", "A learning rate that works",
  "The same bowl-shaped curve. Five dots step steadily down the right-hand wall towards the bottom, "
  "each step a little shorter than the last. The caption reads lr = 0.1, walks down.",
  "0 0 180 175",
  _lr_panel([3.0, 2.4, 1.92, 1.536, 1.2288], "0.1", "walks down", OK_S),
  "Panel 2 of 3. Steps shorten as the wall flattens. This is the only one of the three whose dots "
  "are monotone &mdash; every dot lower than the one before.")

M("motif-lr-diverging", "A learning rate that diverges",
  "The same bowl-shaped curve. A dot high on the right wall leaps across the bowl to the far wall, "
  "then leaps back even higher, each jump landing further up than the last. The caption reads "
  "lr = 1.1, leaps and climbs.",
  "0 0 180 175",
  _lr_panel([3.0, -3.6, 4.32], "1.1", "leaps and climbs", BAD_S),
  "Panel 3 of 3. The step must visibly cross the bottom and land HIGHER. Too-small and diverging are "
  "told apart by the shape of the walk, not only by colour.")
