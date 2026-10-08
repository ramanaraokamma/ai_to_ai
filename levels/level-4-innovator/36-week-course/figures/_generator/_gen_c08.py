"""Block C8 (weeks 22, 23, 24) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a
hand sum printed beside it (STYLE.md 2.1).

W22 student-guide/week-22.md section 5 (one DPO pair by hand: reference (-20.0, -18.0), policy now
    (-19.0, -19.5); beta 0.1 -> margin 0.25, loss 0.5759; beta 5 -> margin 12.5, loss 0.000004)
    and section 4 (reward.py output: five learned weights, r9 +5.047 against r2 +4.578);
    the blank is workbook page 22.3 part G (reference (-15.0, -14.0), policy now (-13.0, -15.0)),
    no moved / gap / margin / loss values drawn
W23 student-guide/week-23.md stand-in section (p = 0.55 / 0.75 / 0.99 from the one documented line:
    0.55 + 0.15 + 0.05 = 0.75 and 0.55 + 0.15 + 0.24 + 0.05 = 0.99, hand sums) and section 5
    (versions.py output: per-field correct out of 8, seed 0); the blank is the loop of Figure 23.1
    with the six names and the guard's name left empty. Stand-in figures carry the chip.
W24 student-guide/week-24.md "The ceiling" (n = 3: 3/6 x 1 + 3/6 x 1/3 = 0.500 + 0.167 = 0.667) and
    section 5 (scratchpad_run.py: strings for 4211 + 9, per answer character, five-seed table, 0.994);
    the blank is workbook page 24.1e (four keys), the answers are the 24.1e table, no dots drawn
"""
from _gen_core import *

FIGS = {}


def fig(name, vb, title, desc, parts):
    FIGS[name] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=374):
    return t(400, y, s, 14, MUT, "middle")


def blank_line(x1, x2, y):
    return line(x1, y, x2, y, GRID, 2)


# ---------------------------------------------------------------- W22-4  moved, then margin, then loss
def w22_4():
    X = lambda v: 110 + (v + 21) * 95
    o = [ctitle("Moved = now minus the frozen copy")]
    o.append(line(110, 262, 490, 262, INK, 2))
    for v in (-21, -20, -19, -18, -17):
        o.append(line(X(v), 262, X(v), 268, MUT, 1.5))
        o.append(t(X(v), 284, "&#8722;%d" % -v, 12, MUT, "middle"))
    o.append(t(300, 304, "log-chance of the answer (higher = more likely)", 12, MUT, "middle"))
    rows = [("chosen", 120, -20.0, -19.0, "+1.0"), ("rejected", 200, -18.0, -19.5, "&#8722;1.5")]
    for name, y, ref, now, mv in rows:
        o.append(line(110, y, 490, y, GRID, 1.5, "6 4"))
        o.append(t(20, y + 5, name, 14, INK, "start"))
        s = 1 if now > ref else -1
        o.append(arrow(X(ref) + 10 * s, y, X(now) - 10 * s, y, ACC_S, 3))
        o.append(mark("circle", X(ref), y, 7, MODEL_S, PAPER, 2))
        o.append(mark("square", X(now), y, 7, MODEL_S, MODEL_F, 2))
        o.append(t(X(ref), y - 18, "ref &#8722;%.1f" % -ref, 12, MUT, "middle"))
        o.append(t(X(now), y - 18, "now &#8722;%.1f" % -now, 12, INK, "middle"))
        o.append(t((X(ref) + X(now)) / 2.0, y + 28, "moved " + mv, 14, ACC_S, "middle"))
    o.append(rect(130, 314, 340, 40, 10, ACC_F, ACC_S, 3))
    o.append(t(300, 334, "gap = 1.0 &#8722; (&#8722;1.5) = 2.5", 18, INK, "middle", central=True))
    # the two leashes: the same gap, two betas (hand sums from the lesson)
    cards = [(90, "beta = 0.1", "margin = 0.1 &#215; 2.5 = 0.25", "sigmoid = 0.5622", "loss 0.5759"),
             (215, "beta = 5", "margin = 5 &#215; 2.5 = 12.5", "sigmoid = 1.0000", "loss 0.000004")]
    for y, h1, l1, l2, l3 in cards:
        o.append(rect(530, y, 250, 110, 10, PANEL, GRID, 2))
        o.append(t(655, y + 24, h1, 18, INK, "middle"))
        o.append(t(655, y + 50, l1, 14, INK, "middle"))
        o.append(t(655, y + 72, l2, 14, MUT, "middle"))
        o.append(t(655, y + 97, l3, 18, ACC_S, "middle"))
    o.append(cap("The frozen copy never moves; the same gap gives two very different losses."))
    fig("fig-w22-4-dpo-moved-and-margin.svg", "0 0 800 400",
        "DPO measures how far each answer moved from a frozen copy, and beta scales the gap before the loss",
        "Two number lines of log-chance from minus 21 to minus 17. Chosen answer: reference minus 20.0, now minus 19.0, "
        "an arrow to the right marked moved plus 1.0. Rejected answer: reference minus 18.0, now minus 19.5, an arrow to the "
        "left marked moved minus 1.5. The gap is 1.0 minus minus 1.5, which is 2.5. On the right, the same gap at beta 0.1 gives "
        "margin 0.25, sigmoid 0.5622 and loss 0.5759; at beta 5 it gives margin 12.5, sigmoid 1.0000 and loss 0.000004.", o)


# ---------------------------------------------------------------- W22-5  the reward model's five weights
def w22_5():
    # reward.py output (seed 1, 500 steps)
    W = [("has_numbered_steps", 5.047), ("gives_direct_answer", 4.578), ("hedges_a_lot", -2.794),
         ("over_400_chars", -2.534), ("refuses", -6.091)]
    x0, S = 300, 30.0
    o = [ctitle("What the scorer learned from ten judgements")]
    o.append(t(20, 82, "the five learned weights", 14, INK, "start"))
    for i, (name, v) in enumerate(W):
        y = 104 + i * 46
        o.append(t(20, y + 8, name, 12, MUT, "start", mono=True))
        x1, x2 = sorted((x0, x0 + v * S))
        if v > 0:
            o.append(rect(x1, y + 14, x2 - x1, 18, 2, DATA_F, DATA_S, 2))
            o.append(t(x2 + 6, y + 28, "+%.3f" % v, 12, INK, "start"))
        else:
            o.append(rect(x1, y + 14, x2 - x1, 18, 2, PANEL, DATA_S, 2, "4 3"))
            o.append(t(x1 - 6, y + 28, "&#8722;%.3f" % -v, 12, INK, "end"))
    o.append(line(x0, 94, x0, 338, INK, 2))
    o.append(t(x0, 354, "0", 12, MUT, "middle"))
    # right: the hack
    o.append(rect(520, 70, 260, 270, 12, PANEL, GRID, 2))
    o.append(t(650, 96, "an answer that only has steps", 14, INK, "middle"))
    o.append(t(650, 116, "scores above a direct answer", 14, INK, "middle"))
    rx, RS = 540, 36.0
    for y, name, feats, v, bad in ((142, "r9", "[1, 0, 0, 0, 0]", 5.047, True), (222, "r2", "[0, 1, 0, 0, 0]", 4.578, False)):
        o.append(t(rx, y, name + " " + feats, 12, INK, "start", mono=True))
        o.append(rect(rx, y + 10, v * RS, 22, 2, BAD_F if bad else DATA_F, BAD_S if bad else DATA_S, 2))
        o.append(t(rx + v * RS + 6, y + 26, "+%.3f" % v, 12, INK, "start"))
    o.append(t(rx, 190, "steps only, answers nothing", 12, MUT, "start"))
    o.append(t(rx, 270, "direct and short", 12, MUT, "start"))
    o.append(t(650, 306, "r9 beats r2? True", 14, BAD_S, "middle"))
    o.append(t(650, 326, "loss 0.6931 &#8594; 0.0135 &#8594; 0.0017", 12, MUT, "middle"))
    o.append(cap("Ten invented judgements, no raters: the biggest positive weight rewards formatting."))
    fig("fig-w22-5-reward-weights-and-hack.svg", "0 0 800 400",
        "A reward model trained on ten judgements over-rewards numbered steps, so an answer with only steps beats a direct one",
        "Left, five horizontal bars for the learned reward weights: has_numbered_steps plus 5.047, gives_direct_answer plus 4.578, "
        "hedges_a_lot minus 2.794, over_400_chars minus 2.534, refuses minus 6.091. Negative bars are dashed and extend left of zero. "
        "Right, two bars: r9, numbered steps only, reward plus 5.047, above r2, a short direct answer, plus 4.578; r9 beats r2 is True. "
        "The Bradley-Terry loss falls from 0.6931 to 0.0135 to 0.0017 at steps 1, 100 and 500. The judgements are invented.", o)


# ---------------------------------------------------------------- W22-6  BLANK: one DPO pair (workbook 22.3 G)
def w22_6():
    X = lambda v: 110 + (v + 16) * 95
    o = [ctitle("Blank: one DPO pair, then two leashes")]
    o.append(line(110, 206, 490, 206, INK, 2))
    for v in (-16, -15, -14, -13, -12):
        o.append(line(X(v), 206, X(v), 212, MUT, 1.5))
        o.append(t(X(v), 228, "&#8722;%d" % -v, 12, MUT, "middle"))
    o.append(t(300, 248, "log-chance of the answer", 12, MUT, "middle"))
    for name, y, ref in (("chosen", 100, -15.0), ("rejected", 160, -14.0)):
        o.append(line(110, y, 490, y, GRID, 1.5, "6 4"))
        o.append(t(20, y + 5, name, 14, INK, "start"))
        o.append(mark("circle", X(ref), y, 7, MODEL_S, PAPER, 2))
        o.append(t(X(ref), y - 18, "ref &#8722;%.1f" % -ref, 12, MUT, "middle"))
        o.append(rect(520, y - 17, 260, 34, 8, PAPER, GRID, 2, "6 4"))
        o.append(t(534, y + 5, "moved", 14, INK, "start"))
        o.append(blank_line(594, 700, y + 8))
    cells = [(20, "gap", False), (280, "beta = 0.1", True), (540, "beta = 0.5", True)]
    for x, lab, two in cells:
        o.append(rect(x, 268, 240, 84, 10, PANEL, GRID, 2, "6 4"))
        o.append(t(x + 14, 292, lab, 14, INK, "start"))
        if two:
            o.append(t(x + 14, 322, "margin", 12, MUT, "start"))
            o.append(blank_line(x + 66, x + 116, 326))
            o.append(t(x + 130, 322, "loss", 12, MUT, "start"))
            o.append(blank_line(x + 166, x + 226, 326))
        else:
            o.append(blank_line(x + 14, x + 150, 326))
    o.append(t(300, 372, "now: chosen &#8722;13.0, rejected &#8722;15.0. Mark each, draw the arrows, fill the boxes.", 12, MUT, "middle"))
    fig("fig-w22-6-blank-dpo-pair.svg", "0 0 800 400",
        "Blank DPO pair: plot where the policy now sits, then find moved, gap, margin and loss",
        "A blank worksheet. Two log-chance number lines from minus 16 to minus 12, one for the chosen answer with a hollow reference marker "
        "at minus 15.0 and one for the rejected answer with a hollow reference marker at minus 14.0. At the right of each line is an empty "
        "dashed box labelled moved. Below, three empty dashed boxes: gap, beta 0.1 with blanks for margin and loss, and beta 0.5 with blanks "
        "for margin and loss. The policy now values, minus 13.0 and minus 15.0, are in the instruction line; no answers are drawn.", o)


# ---------------------------------------------------------------- W23-4  the stand-in's one line, as three switches
def w23_4():
    cx = [420, 560, 700]
    o = [ctitle("What the stand-in does: three switches set one chance")]
    o.append(stand_in_frame(20, 80, 760, 250))
    for c, name in zip(cx, ("v1 zero-shot", "v2 rules", "v3 few-shot")):
        o.append(t(c, 106, name, 14, INK, "middle"))
    o.append(line(36, 118, 764, 118, GRID, 1.5))
    o.append(t(40, 144, "every prompt starts at", 14, INK, "start"))
    for c in cx:
        o.append(t(c, 144, "0.55", 14, INK, "middle"))
    # (label, [(on, text)] per version); hand sums: 0.55+0.15+0.05 = 0.75 ; 0.55+0.15+0.24+0.05 = 0.99
    rws = [("&quot;rules:&quot; in the system prompt", [(0, "no: +0"), (1, "yes: +0.15"), (1, "yes: +0.15")]),
           ("&lt;example&gt; tags (at most 3)", [(0, "0: +0"), (0, "0: +0"), (1, "3: +0.24")]),
           ("&quot;schema&quot; or &quot;json&quot; in it", [(0, "no: +0"), (1, "yes: +0.05"), (1, "yes: +0.05")])]
    for i, (lab, cells) in enumerate(rws):
        y = 178 + i * 36
        o.append(t(40, y + 5, lab, 14, INK, "start"))
        for c, (on, txt) in zip(cx, cells):
            o.append(tick(c - 40, y, 8, OK_S) if on else cross(c - 40, y, 6, MUT))
            o.append(t(c - 24, y + 4, txt, 12, INK, "start"))
    o.append(line(36, 268, 764, 268, GRID, 1.5))
    o.append(t(40, 306, "chance a box is right", 14, INK, "start"))
    for c, p in zip(cx, ("0.55", "0.75", "0.99")):
        o.append(rect(c - 46, 284, 92, 40, 10, ACC_F, ACC_S, 3))
        o.append(t(c, 304, p, 18, INK, "middle", central=True))
    o.append(t(400, 352, "each of the 32 boxes is rolled with this chance, using the seed", 14, MUT, "middle"))
    o.append(cap("The order v1 &lt; v2 &lt; v3 is built in; this is a script, not evidence about a real model.", 374))
    fig("fig-w23-4-stand-in-switches.svg", "0 0 800 400",
        "The stand-in's chance of getting a box right depends only on three features of the prompt, so the ordering is built in",
        "A dashed panel marked stand-in, not a model. Three columns for v1 zero-shot, v2 rules and v3 few-shot. Every column starts at 0.55. "
        "Rules in the system prompt adds 0.15 for v2 and v3 and nothing for v1. Example tags add 0.08 each, at most 3: nothing for v1 and v2, "
        "plus 0.24 for v3. The words schema or json add 0.05 for v2 and v3. The resulting chance a box is right is 0.55, 0.75 and 0.99. "
        "Each of the 32 boxes is rolled with that chance using the seed.", o)


# ---------------------------------------------------------------- W23-5  per-field counts, three versions
def w23_5():
    FIELDS = ["category", "urgency", "order_id", "refund_requested"]
    # versions.py seed 0 output, per-field correct out of 8
    DATA = [("v1", [6, 3, 4, 3], "50.0%"), ("v2", [6, 5, 7, 4], "68.8%"), ("v3", [8, 6, 8, 8], "93.8%")]
    assert [sum(r[1]) for r in DATA] == [16, 22, 30]
    x0, cw = 110, 168
    o = [ctitle("Which boxes each prompt got right (out of 8 messages)")]
    o.append(stand_in_frame(20, 80, 760, 252))
    for j, f in enumerate(FIELDS):
        o.append(t(x0 + j * cw, 108, f, 12, INK, "start", mono=True))
    for i, (name, vals, pct) in enumerate(DATA):
        y = 120 + i * 68
        o.append(t(32, y + 15, name, 14, INK, "start"))
        for j, v in enumerate(vals):
            for k in range(8):
                on = k < v
                o.append(sq(x0 + j * cw + k * 15, y, 14, 22, DATA_F if on else PANEL, DATA_S if on else GRID, 2))
            o.append(t(x0 + j * cw + 124, y + 16, "%d/8" % v, 12, INK, "start"))
        o.append(t(x0, y + 40, "%s = %d of 32 = %s" % (" + ".join(str(v) for v in vals), sum(vals), pct), 12, MUT, "start"))
    o.append(t(400, 320, "the constant-answer floor: 14 of 32 = 43.8%", 14, INK, "middle"))
    o.append(cap("Counts from the stand-in, seed 0: each row's four counts add to its field score."))
    fig("fig-w23-5-per-field-counts.svg", "0 0 800 400",
        "Per-field counts for the three prompts against the stand-in add up to 16, 22 and 30 of 32 boxes",
        "A dashed panel marked stand-in, not a model. Three rows of squares, eight squares per cell, filled for each message right. "
        "Columns category, urgency, order_id, refund_requested. v1: 6, 3, 4, 3, which adds to 16 of 32, 50.0 percent. "
        "v2: 6, 5, 7, 4, which adds to 22 of 32, 68.8 percent. v3: 8, 6, 8, 8, which adds to 30 of 32, 93.8 percent. "
        "The constant-answer floor is 14 of 32, 43.8 percent. Seed 0.", o)


# ---------------------------------------------------------------- W23-6  BLANK: name the six parts of the loop
def w23_6():
    JOBS = [("cases and their", "right answers,", "written first"),
            ("what you tell", "the model, kept", "under a name"),
            ("send it to the", "model and get", "text back"),
            ("pull the record", "out of a chatty", "reply"),
            ("count the boxes", "that match the", "right answers"),
            ("list the scores", "and what was", "right, now wrong")]
    w, gap = 112, 17.6
    o = [ctitle("Blank: name the six parts of the prompt loop")]
    xs = [20 + i * (w + gap) for i in range(6)]
    # connectors first, boxes second
    for i in range(5):
        o.append(arrow(xs[i] + w + 1, 140, xs[i + 1] - 1, 140, INK, 3))
    o.append(poly([(xs[5] + w / 2.0, 110), (xs[5] + w / 2.0, 82), (xs[1] + w / 2.0, 82)], "none", INK, 3, "6 4"))
    o.append(arrow(xs[1] + w / 2.0, 82, xs[1] + w / 2.0, 108, INK, 3, "6 4"))
    o.append(t((xs[1] + xs[5] + w) / 2.0, 72, "change one thing, then go round again", 12, MUT, "middle"))
    for i, x in enumerate(xs):
        o.append(rect(x, 110, w, 60, 8, PAPER, DATA_S, 2, "6 4"))
        o.append(ring_num(x + 18, 128, i + 1))
        o.append(blank_line(x + 12, x + w - 12, 158))
        for k, s in enumerate(JOBS[i]):
            o.append(t(x + w / 2.0, 194 + k * 17, s, 12, MUT, "middle"))
    o.append(rect(20, 262, 760, 70, 10, PANEL, GRID, 2, "6 4"))
    o.append(t(40, 292, "around the whole loop, stops the run when the money runs out:", 14, INK, "start"))
    o.append(t(40, 316, "its name", 12, MUT, "start"))
    o.append(blank_line(100, 320, 320))
    fig("fig-w23-6-blank-prompt-loop.svg", "0 0 800 400",
        "Blank prompt loop: write the name of each of the six parts and of the guard around them",
        "A blank worksheet. Six empty dashed boxes in a row, numbered 1 to 6 and joined by arrows, each with a write-in line and a short job "
        "description underneath: cases and their right answers written first; what you tell the model kept under a name; send it to "
        "the model and get text back; pull the record out of a chatty reply; count the boxes that match the right answers; list the scores and "
        "what was right and is now wrong. A dashed arrow loops from box 6 back to box 2, labelled change one thing, then go round again. "
        "Below, a wide dashed panel with a write-in line for the name of the part that stops the run when the money runs out. No names are drawn.", o)


# ---------------------------------------------------------------- W24-4  the ceiling at n = 3, as two cases
def w24_4():
    o = [ctitle("The ceiling at n = 3: two cases, added")]
    x0, cw, gp = 170, 60, 20
    letters = "abcdef"
    for i, ch in enumerate(letters):
        x = x0 + i * (cw + gp)
        shown = i < 3
        if shown:
            o.append(rect(x, 70, cw, 52, 8, DATA_F, DATA_S, 2))
        else:
            o.append(rect(x, 70, cw, 52, 8, PANEL, GRID, 2, "6 4"))
        o.append(t(x + cw / 2.0, 90, ch, 18, INK, "middle", mono=True, central=True))
        if shown:
            o.append(tick(x + cw / 2.0, 108, 8, OK_S))
        else:
            o.append(t(x + cw / 2.0, 108, "?", 14, MUT, "middle", central=True))
    a1, a2 = x0, x0 + 2 * (cw + gp) + cw
    b1, b2 = x0 + 3 * (cw + gp), x0 + 5 * (cw + gp) + cw
    o.append(bracket(a1, a2, 134, 8, MUT, True))
    o.append(bracket(b1, b2, 134, 8, MUT, True))
    o.append(t((a1 + a2) / 2.0, 164, "on the page: 3 of 6", 12, MUT, "middle"))
    o.append(t((b1 + b2) / 2.0, 164, "not on the page: 3 of 6", 12, MUT, "middle"))
    o.append(arrow((a1 + a2) / 2.0, 172, (a1 + a2) / 2.0, 194, INK, 2))
    o.append(arrow((b1 + b2) / 2.0, 172, (b1 + b2) / 2.0, 194, INK, 2))
    o.append(rect(60, 198, 320, 100, 10, OK_F, OK_S, 3))
    for k, (s, sz, col) in enumerate((("asked letter is on the page", 14, INK), ("3 times in 6", 14, INK),
                                       ("copy it: right every time", 14, INK), ("3/6 &#215; 1 = 0.500", 18, INK))):
        o.append(t(220, 220 + k * 22 + (6 if k == 3 else 0), s, sz, col, "middle"))
    o.append(rect(420, 198, 320, 100, 10, PANEL, GRID, 3, "6 4"))
    for k, (s, sz, col) in enumerate((("asked letter is not on the page", 14, INK), ("3 times in 6", 14, INK),
                                       ("3 digits unused: a 1-in-3 guess", 14, INK), ("3/6 &#215; 1/3 = 0.167", 18, INK))):
        o.append(t(580, 220 + k * 22 + (6 if k == 3 else 0), s, sz, col, "middle"))
    o.append(rect(200, 314, 400, 40, 10, ACC_F, ACC_S, 3))
    o.append(t(400, 334, "0.500 + 0.167 = 0.667 = (3 + 1) &#247; 6", 18, INK, "middle", central=True))
    fig("fig-w24-4-ceiling-two-cases.svg", "0 0 800 400",
        "The best possible score splits into the keys on the page, copied, and the keys off the page, guessed",
        "Six cards a to f. The first three are filled and ticked, on the page; the last three are dashed with a question mark, not on the page. "
        "Left case: the asked letter is on the page, 3 times in 6, copy it and be right every time, 3 over 6 times 1 equals 0.500. "
        "Right case: not on the page, 3 times in 6, three digits are unused so it is a 1-in-3 guess, 3 over 6 times 1 over 3 equals 0.167. "
        "Added: 0.500 plus 0.167 equals 0.667, which is (3 plus 1) divided by 6.", o)


# ---------------------------------------------------------------- W24-5  scratchpad: strings, characters, seeds
def w24_5():
    # scratchpad_run.py output: full_text(4211, 9, ...), seed 0 per-answer-character, the five-seed table
    Q, WK, A = "04211+00009=", "19011020202040400000#", "004220."
    DIRECT = [1.0, 0.98, 0.82, 0.11, 0.11, 0.13]
    PAD = [1.0] * 6
    SEEDS = [("direct", [0.000, 0.038, 0.052, 0.082, 0.000]),
             ("with working", [1.000, 1.000, 1.000, 1.000, 1.000]),
             ("compact working", [1.000, 0.090, 0.974, 1.000, 0.000])]
    cw = lambda s: int(len(s) * 7.2) + 14
    o = [ctitle("Working first: the same sum written two ways")]
    x = 100
    o.append(t(20, 90, "direct", 14, INK, "start"))
    o.append(chip(x, 74, cw(Q), Q, DATA_S, DATA_F))
    o.append(chip(x + cw(Q) + 8, 74, cw(A), A, DATA_S, DATA_F))
    o.append(t(20, 132, "with working", 14, INK, "start"))
    o.append(chip(x, 116, cw(Q), Q, DATA_S, DATA_F))
    o.append(rect(x + cw(Q) + 8, 116, cw(WK), 26, 6, ACC_F, ACC_S, 3))
    o.append(t(x + cw(Q) + 8 + cw(WK) / 2.0, 129, WK, 12, INK, "middle", mono=True, central=True))
    o.append(chip(x + cw(Q) + cw(WK) + 16, 116, cw(A), A, DATA_S, DATA_F))
    o.append(t(x + cw(Q) / 2.0, 162, "question", 12, MUT, "middle"))
    o.append(t(x + cw(Q) + 8 + cw(WK) / 2.0, 162, "working", 12, ACC_S, "middle"))
    o.append(t(x + cw(Q) + cw(WK) + 16 + cw(A) / 2.0, 162, "answer", 12, MUT, "middle"))
    # left chart
    cx0, cyb, ch = 70, 330, 120
    Y = lambda v: cyb - v * ch
    o.append(t(20, 196, "right, per answer character", 14, INK, "start"))
    o.append(rect(232, 186, 12, 12, 2, PANEL, DATA_S, 2, "4 3"))
    o.append(t(250, 196, "direct", 12, INK, "start"))
    o.append(rect(306, 186, 12, 12, 2, OK_F, OK_S, 2))
    o.append(t(324, 196, "with working", 12, INK, "start"))
    for v, lab in ((0, "0"), (0.5, "0.5"), (1.0, "1.0")):
        o.append(line(cx0, Y(v), 420, Y(v), GRID, 1.5, "6 4" if v else None))
        o.append(t(cx0 - 6, Y(v) + 4, lab, 12, MUT, "end"))
    o.append(line(cx0, Y(0.10), 420, Y(0.10), MUT, 2, "2 4"))
    for i in range(6):
        gx = cx0 + 8 + i * 57
        o.append(rect(gx, Y(DIRECT[i]), 22, cyb - Y(DIRECT[i]), 2, PANEL, DATA_S, 2, "4 3"))
        o.append(rect(gx + 24, Y(PAD[i]), 22, cyb - Y(PAD[i]), 2, OK_F, OK_S, 2))
        o.append(t(gx + 11, Y(DIRECT[i]) - 5, "%s" % ("1.0" if DIRECT[i] == 1.0 else "%.2f" % DIRECT[i]), 12, INK, "middle"))
        o.append(t(gx + 35, Y(PAD[i]) - 5, "1.0", 12, INK, "middle"))
        o.append(t(gx + 23, cyb + 17, str(i + 1), 12, MUT, "middle"))
    o.append(line(cx0, 210, cx0, cyb, INK, 2))
    o.append(line(cx0, cyb, 420, cyb, INK, 2))
    o.append(t(245, 366, "answer character (seed 0); dotted line: a pure guess, 0.10", 12, MUT, "middle"))
    # right table
    tx, cols = 440, [566, 612, 658, 704, 750]
    o.append(t(tx, 196, "exact match on 500 held-out sums", 14, INK, "start"))
    for s, c in enumerate(cols):
        o.append(t(c, 224, "seed %d" % s, 12, MUT, "middle"))
    for i, (lab, vals) in enumerate(SEEDS):
        y = 252 + i * 34
        o.append(t(tx, y + 4, lab, 12, INK, "start"))
        for c, v in zip(cols, vals):
            hi, lo = v >= 0.9, v < 0.1
            o.append(sq(c - 22, y - 14, 44, 28, OK_F if hi else (BAD_F if lo else PANEL), OK_S if hi else (BAD_S if lo else GRID), 2))
            o.append(t(c, y + 4, "%.3f" % v, 12, INK, "middle"))
    o.append(t(tx, 340, "direct, 4 times the steps (12,000):", 12, MUT, "start"))
    o.append(t(tx, 357, "0.994, one seed", 12, MUT, "start"))
    fig("fig-w24-5-scratchpad-numbers.svg", "0 0 800 400",
        "Writing the working first fixes the last three answer characters that direct answering leaves at chance",
        "Top, the same sum 4211 plus 9 as text: direct is 04211+00009= then 004220.; with working is 04211+00009=, then the working "
        "19011020202040400000# highlighted, then 004220. Bottom left, paired bars for the share right at each of six answer characters, seed 0. "
        "Direct: 1.0, 0.98, 0.82, 0.11, 0.11, 0.13. With working: 1.0 at every character. A dotted line marks a pure guess at 0.10. "
        "Bottom right, exact match on 500 held-out sums for seeds 0 to 4. Direct: 0.000, 0.038, 0.052, 0.082, 0.000. With working: 1.000 at all five. "
        "Compact working: 1.000, 0.090, 0.974, 1.000, 0.000. Direct with 12,000 steps scored 0.994 on one seed.", o)


# ---------------------------------------------------------------- W24-6  BLANK: draw the four-key ceiling (workbook 24.1e)
def w24_6():
    x0, x1, yb, yt = 110, 540, 330, 90
    X = lambda n: x0 + 40 + n * 100
    Y = lambda v: yb - v * (yb - yt)
    o = [ctitle("Blank: draw the ceiling for the four-key game")]
    for v, lab in ((0, "0"), (0.25, "0.25"), (0.5, "0.50"), (0.75, "0.75"), (1.0, "1.00")):
        o.append(line(x0, Y(v), x1, Y(v), GRID, 1.5, "6 4" if v else None))
        o.append(t(x0 - 8, Y(v) + 4, lab, 12, MUT, "end"))
    o.append(line(x0, yt - 10, x0, yb, INK, 2))
    o.append(line(x0, yb, x1, yb, INK, 2))
    for n in range(5):
        o.append(line(X(n), yb, X(n), yb + 6, MUT, 1.5))
        o.append(t(X(n), yb + 22, str(n), 12, MUT, "middle"))
    o.append(t((x0 + x1) / 2.0, yb + 44, "n pairs shown (of 4 keys)", 12, MUT, "middle"))
    o.append(trot(40, (yt + yb) / 2.0, "best possible accuracy", 12))
    o.append(rect(580, 110, 200, 150, 12, PANEL, GRID, 2, "6 4"))
    for k, s in enumerate(("Plot your table", "from 24.1e: one dot", "for each n, then", "join the dots.")):
        o.append(t(596, 140 + k * 24, s, 14, INK, "start"))
    fig("fig-w24-6-blank-four-key-ceiling.svg", "0 0 800 400",
        "Blank chart: plot the best possible accuracy for the four-key game at n = 0 to 4",
        "A blank chart. The horizontal axis is n pairs shown, 0 to 4. The vertical axis is best possible accuracy from 0 to 1.00 with grid "
        "lines at 0.25 steps. No dots or lines are drawn. A dashed box at the right says to plot the table from 24.1e, one dot for each n, "
        "then join the dots.", o)


def build():
    for f in (w22_4, w22_5, w22_6, w23_4, w23_5, w23_6, w24_4, w24_5, w24_6):
        f()
    return FIGS
