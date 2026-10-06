"""Block 7 (weeks 19, 20, 21): two concept figures per week.

    fig-w19-1-ablation-bars.svg         validation loss of five ablated TinyGPTs          (week-19 student guide, 5. five-model run)
    fig-w19-2-task-table.svg            share of answers right, 3 tasks x 5 models        (week-19, 8. the task table)
    fig-w20-1-bpe-by-hand.svg           count pairs, glue the winner, use the merges       (week-20, 3./7. the rule, the trace)
    fig-w20-2-bytes-per-token.svg       bytes per token as merges are learned             (week-20, 9. what does it learn?)
    fig-w21-1-power-law-miss.svg        four widths, a line, a prediction and the miss    (week-21, 10./11. fit.py, check.py)
    fig-w21-2-characters-per-knob.svg   characters read per knob, five widths             (week-21, 11. check.py)

Every number below is copied from an executed block printed in the same week's student guide, or is a
hand sum printed on the figure (STYLE.md 2.1). Nothing is invented. No stand-ins appear here: every
model is a network the student trained from scratch, so the model role is drawn solid.
"""
import math
import os
from _gen_core import *

MINUS, TIMES, DIV, ARROW, MID = "&#8722;", "&#215;", "&#247;", "&#8594;", "&#183;"


def _ttl(s):
    return t(400, 44, s, 24, INK, "middle")


def _cap(s, y=376):
    return t(400, y, s, 14, MUT, "middle")


def _doc(vb, title, desc, parts):
    return svg_doc(vb, title, desc, "\n".join("  " + p for p in parts)) + "\n"


# ------------------------------------------------------------------ W19-1
ABL = [  # label, train, val, change vs full (printed in the week), note, kind
    ("full", 1.597, 1.673, "baseline", "gap 0.076", "model"),
    ("no mask", 0.070, 0.077, MINUS + "1.596 a leak", "gap 0.007", "leak"),
    ("no positions", 1.451, 1.739, "+0.066 a little worse", "gap 0.288", "data"),
    ("no residual", 2.664, 2.679, "+1.006 much worse", "gap 0.015", "wrecked"),
    ("no norm", 1.150, 1.478, MINUS + "0.195 better", "gap 0.327", "data"),
]


def w19_1():
    X0, K = 170, 130.0
    p = [_ttl("Delete one part, score on unseen text")]
    xf = X0 + 1.673 * K
    p.append(line(xf, 76, xf, 346, MUT, 1.5, "6 4"))
    p.append(t(xf, 70, "full model 1.673", 12, MUT, "middle"))
    p.append(line(X0, 80, X0, 346, INK, 2))
    for i, (lab, tr, va, chg, note, kind) in enumerate(ABL):
        cy = 108 + i * 54
        w = va * K
        fill, stroke = {"model": (MODEL_F, MODEL_S), "leak": (BAD_F, BAD_S), "data": (DATA_F, DATA_S),
                        "wrecked": (BAD_F, BAD_S)}[kind]
        p.append(t(X0 - 12, cy, lab, 18, INK, "end", central=True))
        p.append(rect(X0, cy - 16, max(w, 4), 32, 6, fill, stroke, 3, "6 4" if kind == "leak" else None))
        p.append(t(X0 + w + 10, cy, "%.3f" % va, 14, INK, "start", central=True))
        tx = 610
        p.append(t(tx, cy - 8, chg, 14, INK, "start", central=True))
        p.append(t(tx, cy + 10, "train %.3f %s %s" % (tr, MID, note), 12, MUT, "start", central=True))
        if kind == "leak":
            p.append(badge_cross(X0 + w + 52, cy - 14))
        if kind == "wrecked":
            p.append(badge_cross(X0 + w + 62, cy - 14))
    p.append(t(20, 346 + 20, "bar = validation loss (nats per character), shorter is lower", 12, MUT, "start"))
    p.append(_cap("Same seed, 800 steps, unseen text. Change = validation loss " + MINUS + " 1.673."))
    title = "Deleting a part can make the score look better, so a low number needs a leak check"
    desc = ("Horizontal bars of validation loss for five TinyGPTs trained 800 steps with the same seed and scored on unseen text. "
            "Full 1.673, dashed baseline line. No mask 0.077, dashed red bar with a cross, change " + MINUS + "1.596, a leak. "
            "No positions 1.739, +0.066, a little worse. No residual 2.679, +1.006, wrecked, marked with a cross. "
            "No norm 1.478, " + MINUS + "0.195, better, with the largest gap of 0.327. Train loss and gap are printed under each change.")
    return "fig-w19-1-ablation-bars.svg", _doc("0 0 800 400", title, desc, p)


# ------------------------------------------------------------------ W19-2
TASKS_ROWS = [("copy", [1.00, 1.00, 0.95, 1.00, 1.00], "0.125", "1 " + DIV + " 8"),
              ("reverse", [1.00, 1.00, 0.92, 1.00, 1.00], "0.125", "1 " + DIV + " 8"),
              ("lookup", [1.00, 0.37, 1.00, 1.00, 0.33], "0.1", "1 " + DIV + " 10")]
COLS = ["full", "no mask", "no pos", "no res", "no norm"]


def w19_2():
    GX, CW, RH, GY = 150, 110, 56, 100
    p = [_ttl("Share of answers right, three tasks")]
    for j, c in enumerate(COLS):
        p.append(t(GX + j * CW + CW / 2, GY - 12, c, 18, INK, "middle"))
    p.append(t(GX + 5 * CW + 34 + 12, GY - 12, "chance", 18, INK, "middle"))
    for i, (task, vals, ch, _) in enumerate(TASKS_ROWS):
        y = GY + i * RH
        p.append(t(GX - 12, y + RH / 2, task, 18, INK, "end", central=True))
        for j, v in enumerate(vals):
            x = GX + j * CW
            ringed = (i < 2 and j == 1)
            if v >= 0.99:
                fill, stroke, sw = OK_F, OK_S, 2
            elif v >= 0.9:
                fill, stroke, sw = DATA_F, DATA_S, 2
            else:
                fill, stroke, sw = BAD_F, BAD_S, 2
            if ringed:
                stroke, sw = ACC_S, 4
            p.append(sq(x, y, CW, RH, fill, stroke, sw))
            p.append(t(x + CW / 2 + 8, y + RH / 2, "%.2f" % v, 18, INK, "middle", central=True))
            if v >= 0.99:
                p.append(tick(x + 22, y + RH / 2, 9))
            elif v < 0.5:
                p.append(cross(x + 22, y + RH / 2, 7))
        p.append(sq(GX + 5 * CW + 10, y, 68, RH, PAPER, GRID, 2))
        p.append(t(GX + 5 * CW + 44, y + RH / 2, ch, 14, INK, "middle", central=True))
    p.append(ring_num(GX + 1 * CW + CW - 4, GY + 4, 1))
    p.append(ring_num(GX + 1 * CW + CW - 4, GY + RH + 4, 1))
    p.append(ring_num(GX + 1 * CW + CW - 4, GY + 2 * RH + 4, 2))
    p.append(ring_num(GX + 4 * CW + CW - 4, GY + 2 * RH + 4, 2))
    ly = GY + 3 * RH + 22
    for k, (fl, st, lab, mk) in enumerate([(OK_F, OK_S, "1.00, with a tick", "tick"), (DATA_F, DATA_S, "0.90 to 0.99", None),
                                            (BAD_F, BAD_S, "below 0.50, with a cross", "cross")]):
        lx = 150 + k * 210
        p.append(sq(lx, ly - 10, 20, 20, fl, st, 2))
        p.append(t(lx + 28, ly, lab, 12, MUT, "start", central=True))
    p.append(ring_num(33, 318, 1))
    p.append(t(52, 318, "no mask on copy and reverse: 1.00 because the answer sits one place ahead (a leak)", 12, INK, "start", central=True))
    p.append(ring_num(33, 344, 2))
    p.append(t(52, 344, "lookup: 0.37 without the mask, 0.33 without norm; one seed, cause an open question", 12, INK, "start", central=True))
    p.append(_cap("600 steps per model. Chance: copy and reverse 1 " + DIV + " 8 = 0.125, lookup 1 " + DIV + " 10 = 0.1.", 376))
    title = "A perfect score on a task can be a leak; only the lookup column shows what deleting a part does"
    desc = ("A grid of share of answers right, three made-up tasks by five models, plus a chance column. "
            "Copy: full 1.00, no mask 1.00, no pos 0.95, no res 1.00, no norm 1.00. "
            "Reverse: 1.00, 1.00, 0.92, 1.00, 1.00. Lookup: 1.00, 0.37, 1.00, 1.00, 0.33. Chance is 0.125 on copy and reverse (1 in 8) and 0.1 on lookup (1 in 10). "
            "Cells at 1.00 carry a tick, cells below 0.5 carry a cross. The two no-mask cells on copy and reverse are ringed number 1, a leak; "
            "the lookup cells 0.37 and 0.33 are ringed number 2, causes not tested.")
    return "fig-w19-2-task-table.svg", _doc("0 0 800 400", title, desc, p)


# ------------------------------------------------------------------ W20-1
def _tok(x, y, w, s, kind="data", sw=2, h=34):
    fill, stroke = {"data": (DATA_F, DATA_S), "model": (MODEL_F, MODEL_S), "acc": (ACC_F, ACC_S)}[kind]
    return (rect(x, y, w, h, 6, fill, stroke, sw) + "\n  " +
            t(x + w / 2.0, y + h / 2.0, s, 14, INK, "middle", mono=True, central=True))


def w20_1():
    p = [_ttl("Byte-pair encoding: count, glue, repeat")]
    # panels
    for x, w, lab in ((20, 250, "1  count the pairs"), (290, 250, "2  glue the winner"), (560, 220, "3  use the merges")):
        p.append(rect(x, 70, w, 250, 12, PANEL, GRID, 1.5))
        p.append(t(x + w / 2.0, 98, lab, 18, INK, "middle"))
    p.append(t(145, 124, "low low low low low lower lower", 12, MUT, "middle", mono=True))
    p.append(t(145, 140, "widest widest widest", 12, MUT, "middle", mono=True))
    rows = [("l o", 7, "acc"), ("o w", 7, "data"), ("w i", 3, "data")]
    for i, (lab, n, kind) in enumerate(rows):
        y = 160 + i * 44
        fill, stroke = (ACC_F, ACC_S) if kind == "acc" else (DATA_F, DATA_S)
        p.append(t(34, y + 17, lab, 14, INK, "start", mono=True, central=True))
        p.append(rect(80, y, n * 22, 34, 6, fill, stroke, 4 if kind == "acc" else 2))
        p.append(t(80 + n * 22 + 10, y + 17, str(n), 14, INK, "start", central=True))
    p.append(t(145, 306, "tie on 7: smaller numbers win", 12, MUT, "middle"))
    # glue
    p.append(t(415, 126, "merge 1  (108, 111) " + ARROW + " 256", 12, MUT, "middle", mono=True))
    p.append(_tok(320, 138, 34, "l"))
    p.append(_tok(358, 138, 34, "o"))
    p.append(arrow(398, 155, 424, 155, INK, 2))
    p.append(_tok(432, 138, 60, "lo", "model", 3))
    p.append(t(462, 188, "id 256, count 7", 12, MUT, "middle"))
    p.append(t(415, 224, "merge 2  (256, 119) " + ARROW + " 257", 12, MUT, "middle", mono=True))
    p.append(_tok(308, 236, 44, "lo", "model"))
    p.append(_tok(356, 236, 34, "w"))
    p.append(arrow(396, 253, 424, 253, INK, 2))
    p.append(_tok(432, 236, 70, "low", "model", 3))
    p.append(t(467, 286, "id 257, count 7", 12, MUT, "middle"))
    # use
    p.append(t(670, 124, "&#8220;lowest&#8221; is not in the text", 12, MUT, "middle"))
    for k, ch in enumerate("lowest"):
        p.append(_tok(578 + k * 30, 140, 28, ch))
    p.append(arrow(670, 182, 670, 206, INK, 2))
    p.append(_tok(578, 214, 76, "low", "model", 3))
    p.append(_tok(660, 214, 40, "e", "data"))
    p.append(_tok(706, 214, 56, "st", "model", 3))
    p.append(t(616, 264, "257", 12, MUT, "middle", mono=True))
    p.append(t(680, 264, "101", 12, MUT, "middle", mono=True))
    p.append(t(734, 264, "260", 12, MUT, "middle", mono=True))
    p.append(t(670, 296, "3 tokens, no hole", 14, INK, "middle"))
    p.append(_cap("The ordered list of merges is the whole tokenizer. 300 merges + 256 bytes = vocabulary 556.", 352))
    p.append(_cap("Letters stand in for bytes here: l = 108, o = 111, w = 119.", 372))
    title = "The list of merges, learned by counting, is the tokenizer"
    desc = ("Three panels left to right. One: counts of neighbouring letter pairs inside the words of the tiny text low low low low low lower lower widest widest widest: "
            "l o 7 (highlighted, wins the tie with o w on smaller numbers), o w 7, w i 3. "
            "Two: merge 1 glues l and o, bytes 108 and 111, into token 256 with count 7; merge 2 glues token 256 and w, byte 119, into token 257 low with count 7. "
            "Three: the word lowest, which is not in the text, is written as three tokens low, e, st with ids 257, 101, 260.")
    return "fig-w20-1-bpe-by-hand.svg", _doc("0 0 800 400", title, desc, p)


# ------------------------------------------------------------------ W20-2
BPT = [(0, 1.00), (10, 1.20), (50, 1.49), (100, 1.69), (200, 1.99), (300, 2.16), (400, 2.30)]


def w20_2():
    PX0, PY0, SX, SY = 90, 320, 1.15, 164.3
    X = lambda m: PX0 + m * SX
    Y = lambda v: PY0 - (v - 1.0) * SY
    p = [_ttl("Bytes per token as merges are learned")]
    for v in (1.0, 1.5, 2.0):
        p.append(line(PX0, Y(v), 560, Y(v), GRID, 1.5))
        p.append(t(PX0 - 10, Y(v), "%.1f" % v, 12, MUT, "end", central=True))
    for m in (0, 100, 200, 300, 400):
        p.append(line(X(m), PY0, X(m), PY0 + 6, INK, 2))
        p.append(t(X(m), PY0 + 22, str(m), 12, MUT, "middle"))
    p.append(line(PX0, 80, PX0, PY0, INK, 2))
    p.append(line(PX0, PY0, 560, PY0, INK, 2))
    p.append(trot(40, 200, "bytes per token (higher = shorter text)"))
    p.append(t(325, PY0 + 44, "merges learned", 12, MUT, "middle"))
    p.append(poly([(X(m), Y(v)) for m, v in BPT], "none", DATA_S, 3))
    for m, v in BPT:
        p.append(circ(X(m), Y(v), 6, DATA_F, DATA_S, 2))
        p.append(t(X(m) + 10, Y(v) + 18, "%.2f" % v, 12, INK, "start"))
    # plateau
    p.append(line(X(400), Y(2.30), 560, Y(2.30), ACC_S, 2, "6 4"))
    p.append(ring_num(X(400) + 4, Y(2.30) - 24, 1))
    # callouts
    p.append(rect(590, 90, 190, 124, 10, PAPER, INK, 2))
    for k, s in enumerate(["At 300 merges:", "3,227 tokens", "2.161 bytes per token", "1,277 lone spaces", "(40% of the tokens)"]):
        p.append(t(602, 112 + k * 22, s, 14, INK, "start", central=True))
    p.append(rect(590, 232, 190, 100, 10, ACC_F, ACC_S, 3))
    p.append(ring_num(608, 252, 1))
    for k, s in enumerate(["Asked for 500 or", "1,000: learned 400.", "No pair occurs twice,", "so it stops at 2.30."]):
        p.append(t(626 if k == 0 else 602, 252 + k * 20, s, 14, INK, "start", central=True))
    p.append(_cap("Week 17 corpus, 6,972 characters; measured on the training text itself.", 376))
    title = "More merges shorten the text, until no pair is left worth gluing"
    desc = ("Line chart of bytes per token against merges learned on the 6,972-character Week 17 corpus: 0 merges 1.00, 10 merges 1.20, 50 merges 1.49, "
            "100 merges 1.69, 200 merges 1.99, 300 merges 2.16, 400 merges 2.30. A dashed pink line continues flat at 2.30: asking for 500 or 1,000 merges still learns only 400, "
            "because no pair occurs twice. A box states that at 300 merges there are 3,227 tokens, 2.161 bytes per token, and 1,277 of the tokens are lone spaces, 40 percent.")
    return "fig-w20-2-bytes-per-token.svg", _doc("0 0 800 400", title, desc, p)


# ------------------------------------------------------------------ W21-1
PTS = [(4.1628, 0.3572, "2.2760"), (4.6146, 0.3197, "2.0878"), (5.1182, 0.2337, "1.7127"), (5.6618, 0.1758, "1.4991")]
SLOPE, ICPT = -0.1262, 0.8886
XP, YM = 6.2316, 0.1660        # log10(1,704,149) ; log10(1.4656)


def w21_1():
    PX0, PY0, SX, SY = 90, 330, 195.8, 685.7
    X = lambda v: PX0 + (v - 4.0) * SX
    Y = lambda v: PY0 - (v - 0.05) * SY
    p = [_ttl("A line through four points, then a fifth")]
    for v in (0.1, 0.2, 0.3, 0.4):
        p.append(line(PX0, Y(v), 560, Y(v), GRID, 1.5))
        p.append(t(PX0 - 10, Y(v), "%.2f" % v, 12, MUT, "end", central=True))
    for v in (4.0, 4.5, 5.0, 5.5, 6.0):
        p.append(line(X(v), PY0, X(v), PY0 + 6, INK, 2))
        p.append(t(X(v), PY0 + 22, "%.1f" % v, 12, MUT, "middle"))
    p.append(line(PX0, 80, PX0, PY0, INK, 2))
    p.append(line(PX0, PY0, 560, PY0, INK, 2))
    p.append(trot(34, 205, "log10 of validation loss"))
    p.append(t(325, PY0 + 44, "log10 of knobs (14,549 up to 1,704,149)", 12, MUT, "middle"))
    yl = lambda x: SLOPE * x + ICPT
    p.append(line(X(4.1628), Y(yl(4.1628)), X(5.6618), Y(yl(5.6618)), DATA_S, 2))
    p.append(line(X(5.6618), Y(yl(5.6618)), X(XP), Y(yl(XP)), ACC_S, 2, "6 4"))
    for x, y, lab in PTS:
        p.append(circ(X(x), Y(y), 6, DATA_F, DATA_S, 2))
        p.append(t(X(x) + 10, Y(y) - 8, lab, 12, INK, "start"))
    p.append(mark("diamond", X(XP), Y(yl(XP)), 6, ACC_S, PAPER, 3))
    p.append(mark("square", X(XP), Y(YM), 6, BAD_S, BAD_F, 3))
    p.append(t(575, Y(yl(XP)) + 4, "line predicted 1.2654", 14, INK, "start"))
    p.append(t(575, Y(YM) + 4, "measured 1.4656", 14, INK, "start"))
    p.append(line(X(XP) + 14, Y(YM) + 2, X(XP) + 14, Y(yl(XP)) - 2, ACC_S, 2))
    p.append(rect(575, 96, 205, 100, 10, PAPER, INK, 2))
    for k, s in enumerate(["the line, from 4 points:", "slope " + MINUS + "0.1262", "10" + TIMES + " knobs: loss " + TIMES + " 0.748", "2" + TIMES + " knobs: loss " + TIMES + " 0.916"]):
        p.append(t(585, 116 + k * 22, s, 14 if k != 0 else 12, INK if k else MUT, "start", central=True))
    p.append(rect(575, 212, 205, 30, 8, ACC_F, ACC_S, 3))
    p.append(t(677, 227, "15.8% worse than the line", 14, INK, "middle", central=True))
    p.append(_cap("Circles: widths 16 to 128. Diamond: predicted for width 256. Square: what it scored.", 376))
    title = "The line fitted the four models it was drawn through and missed the fifth"
    desc = ("Log-log scatter. X is log10 of knobs, 4.0 to 6.4; y is log10 of validation loss. Four circles for widths 16, 32, 64 and 128 with losses 2.2760, 2.0878, 1.7127, 1.4991 "
            "lie close to a solid straight line of slope " + MINUS + "0.1262. A dashed pink extension reaches the width-256 model at 1,704,149 knobs, where a hollow diamond marks the prediction 1.2654. "
            "A square marks what that model scored, 1.4656, higher than predicted: 15.8 percent worse. A box says ten times the knobs multiplies the loss by 0.748 and twice the knobs by 0.916.")
    return "fig-w21-1-power-law-miss.svg", _doc("0 0 800 400", title, desc, p)


# ------------------------------------------------------------------ W21-2
CPK = [("14,549", 211.1, "2.2760"), ("41,173", 74.6, "2.0878"), ("131,285", 23.4, "1.7127"),
       ("458,965", 6.7, "1.4991"), ("1,704,149", 1.8, "1.4656")]


def w21_2():
    X0, K = 190, 360 / 211.1
    p = [_ttl("Characters read per knob, five widths")]
    p.append(t(X0, 84, "characters read per knob", 14, MUT, "start"))
    p.append(t(670, 84, "validation loss", 14, MUT, "middle"))
    p.append(t(20, 84, "knobs", 14, MUT, "start"))
    p.append(line(X0, 92, X0, 350, INK, 2))
    for i, (kn, c, lo) in enumerate(CPK):
        cy = 120 + i * 52
        last = i == 4
        p.append(t(20, cy, kn, 14, INK, "start", mono=True, central=True))
        p.append(rect(X0, cy - 15, max(c * K, 4), 30, 6, ACC_F if last else DATA_F, ACC_S if last else DATA_S, 4 if last else 2))
        p.append(t(X0 + c * K + 10, cy, "%.1f" % c, 14, INK, "start", central=True))
        p.append(t(670, cy - (7 if last else 0), lo, 14, INK, "middle", central=True))
        if last:
            p.append(t(670, cy + 11, "line said 1.2654", 12, MUT, "middle", central=True))
    p.append(t(X0 + 220, 120 + 4 * 52 - 6, "each knob gets 1.8 characters to learn from", 12, INK, "start", central=True))
    p.append(_cap("Every run reads 3,072,000 characters. 3,072,000 " + DIV + " 14,549 = 211.1; " + DIV + " 1,704,149 = 1.8.", 376))
    title = "The biggest model has the least text per knob, so the budget has two numbers"
    desc = ("Horizontal bars of characters read per knob, since every run reads 3,072,000 characters: 14,549 knobs 211.1, 41,173 knobs 74.6, 131,285 knobs 23.4, "
            "458,965 knobs 6.7, 1,704,149 knobs 1.8, the last bar short and highlighted pink. Beside each bar the validation loss: 2.2760, 2.0878, 1.7127, 1.4991, 1.4656 "
            "(the line had said 1.2654 for the last). Hand sums 3,072,000 divided by 14,549 = 211.1 and by 1,704,149 = 1.8 are printed.")
    return "fig-w21-2-characters-per-knob.svg", _doc("0 0 800 400", title, desc, p)


FIGURES = [w19_1, w19_2, w20_1, w20_2, w21_1, w21_2]


def emit(figures_dir):
    names = []
    for f in FIGURES:
        name, svg = f()
        open(os.path.join(figures_dir, name), "w").write(svg)
        names.append(name)
    return names
