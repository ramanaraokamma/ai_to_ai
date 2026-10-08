"""Block C10 (weeks 28, 29, 30) extra figures: a mental-model figure, a worked-numbers figure and a
blank workbook figure per week. Every number is copied from the week's printed output or is a hand
sum printed beside it (STYLE.md 2.1).

W28  student-guide/week-28.md Big Idea (the loop and the fences), section 8 (fences.py: eight scripted
     requests, printed stop= / iterations / result) ; the blank is workbook page 28.3 Part 1 (the five
     turns, tokens in and out as given in the workbook table, price 1.00 in / 5.00 out per million)
W29  student-guide/week-29.md Big Idea (the three layers), sections 6 and 7 (weak.py and reworded.py,
     100 seeded runs each, a stand-in) ; the blank is workbook page 29.3 (the triangular-sum bill, drawn
     as total input tokens against steps)
W30  student-guide/week-30.md Big Idea (the four ideas), sections 4 and 5 (p3_jaccard.py, p4_leak.py) ;
     the blank is workbook page 30.2 Part 1 (kappa by hand on a fresh twenty)
"""
from _gen_core import *

FIGS = {}


def fig(name, vb, title, desc, parts):
    FIGS[name] = svg_doc(vb, title, desc, J(*parts))


def ctitle(s):
    return t(400, 44, s, 24, INK, "middle")


def cap(s, y=374):
    return t(400, y, s, 14, MUT, "middle")


def box(x, y, w, h, l1, l2=None, fill=DATA_F, stroke=DATA_S, sw=2, dash=None, mono1=False):
    o = [rect(x, y, w, h, 8, fill, stroke, sw, dash)]
    if l2:
        o.append(t(x + w / 2.0, y + h / 2.0 - 9, l1, 14, INK, "middle", mono=mono1, central=True))
        o.append(t(x + w / 2.0, y + h / 2.0 + 11, l2, 12, MUT, "middle", central=True))
    else:
        o.append(t(x + w / 2.0, y + h / 2.0, l1, 14, INK, "middle", mono=mono1, central=True))
    return "\n  ".join(o)


# ---------------------------------------------------------------- W28-4  who does what in the loop
def w28_4():
    o = [ctitle("The model asks; your code decides")]
    o.append(rect(30, 74, 250, 220, 12, PANEL, MODEL_S, 2))
    o.append(t(155, 98, "the model", 16, INK, "middle", weight="600"))
    o.append(box(48, 112, 214, 52, "perceive", "sent everything so far", MODEL_F, MODEL_S))
    o.append(box(48, 176, 214, 52, "decide", "words, or a tool call", MODEL_F, MODEL_S))
    o.append(t(155, 252, "never sees the function:", 12, MUT, "middle"))
    o.append(t(155, 270, "only a name and its arguments", 12, MUT, "middle"))
    o.append(rect(440, 74, 330, 220, 12, PANEL, HUMAN_S, 2))
    o.append(t(605, 98, "your code (every fence lives here)", 16, INK, "middle", weight="600"))
    steps = [("1  look the name up", "allowlist"), ("2  check the arguments", "contract"),
             ("3  run it", "sandbox, timeout, human"), ("4  result becomes text", "observe")]
    for i, (a, b) in enumerate(steps):
        y = 110 + i * 44
        o.append(rect(456, y, 298, 38, 6, HUMAN_F, HUMAN_S, 2))
        o.append(t(468, y + 19, a, 14, INK, "start", central=True))
        o.append(t(742, y + 19, b, 12, INK, "end", central=True))
    o.append(arrow(284, 140, 434, 140, INK, 3))
    o.append(t(359, 128, "tool call:", 12, INK, "middle"))
    o.append(t(359, 164, "name + arguments", 12, INK, "middle"))
    o.append(arrow(434, 248, 284, 248, ACC_S, 3))
    o.append(t(359, 236, "tool result,", 12, INK, "middle"))
    o.append(t(359, 272, "as plain text", 12, INK, "middle"))
    o.append(arrow(155, 296, 155, 322, INK, 3))
    o.append(rect(30, 326, 250, 36, 8, PAPER, MODEL_S, 2, "6 4"))
    o.append(t(155, 344, "words, no call: stop", 14, INK, "middle", central=True))
    o.append(t(300, 344, "stop reason: end_turn, max_iterations or budget_exhausted", 12, MUT, "start", central=True))
    o.append(cap("Each pass round the loop is one iteration; the six fences are all in the right-hand box.", 376))
    fig("fig-w28-4-model-asks-code-decides", "0 0 800 400",
        "The model only picks a tool name and arguments; your code looks it up, checks it, runs it inside the fences and returns the result as text",
        "On the left a panel for the model with two boxes, perceive and decide. An arrow labelled tool call, name plus arguments, runs right to a panel for your code with four steps: "
        "look the name up, check the arguments, run it held in, and turn the result into text. A pink arrow labelled tool result as plain text runs back to the model. "
        "A downward arrow from the model leads to a dashed box, words with no call: stop, with the three stop reasons beside it.", o)


# ---------------------------------------------------------------- W28-5  eight requests, six fences
def w28_5():
    # student guide section 8, fences.py printed output: (label, stop, iterations, note)
    ROWS = [("1 max_iterations", "max_iterations", 3, "result: 2", False),
            ("2 budget_usd", "budget_exhausted", 2, "result: 2", False),
            ("3 sandbox", "end_turn", 2, "PermissionError: refused: '../escape.md'", True),
            ("4 timeout", "end_turn", 2, "'slow' timed out.", True),
            ("5 allowlist", "end_turn", 2, "no tool named 'delete_everything'.", True),
            ("6 confirmation", "end_turn", 2, "the human declined this action.", True),
            ("bad arguments", "end_turn", 2, "bad arguments for 'calculate'", True),
            ("hostile calculate", "end_turn", 2, "ValueError: unsupported expression element: Call", True)]
    o = [ctitle("Eight scripted requests, no model")]
    o.append(t(20, 80, "request", 12, MUT, "start"))
    o.append(t(180, 80, "stop reason", 12, MUT, "start"))
    o.append(t(340, 80, "turns", 12, MUT, "start"))
    o.append(t(400, 80, "what the tool handed back (a cross: it began Error:)", 12, MUT, "start"))
    for i, (lab, stop, it, note, err) in enumerate(ROWS):
        y = 90 + i * 29
        o.append(rect(20, y, 760, 27, 0, PANEL if i % 2 == 0 else PAPER, GRID, 1))
        o.append(t(20, y + 13, lab, 12, INK, "start", mono=True, central=True))
        changed = stop != "end_turn"
        o.append(rect(176, y + 3, 150, 22, 6, ACC_F if changed else PAPER, ACC_S if changed else GRID, 3 if changed else 2))
        o.append(t(251, y + 14, stop, 12, INK, "middle", mono=True, central=True))
        o.append(t(348, y + 14, str(it), 12, INK, "middle", central=True))
        if err:
            o.append(cross(412, y + 14, 5))
        else:
            o.append(tick(412, y + 14, 7))
        o.append(t(428, y + 14, note, 12, INK, "start", central=True))
    o.append(t(400, 340, "Only the two ringed stop reasons differ. The other six read end_turn,", 12, MUT, "middle"))
    o.append(t(400, 356, "because the scripted model was handed an error, read it and said ok.", 12, MUT, "middle"))
    o.append(cap("The Error text, not the stop reason, names the fence (a scripted plan, not a model).", 376))
    fig("fig-w28-5-eight-requests-six-fences", "0 0 800 400",
        "Eight scripted requests meet the fences: only the turns cap and the money cap change the stop reason, the other six end with end_turn and an Error text",
        "A table of eight rows: 1 max_iterations, 2 budget_usd, 3 sandbox, 4 timeout, 5 allowlist, 6 confirmation, bad arguments and hostile calculate. Columns give the stop reason, the number of turns "
        "(3, 2, then 2 for every row) and the tool's reply. Rows 1 and 2 have ringed stop reasons, max_iterations and budget_exhausted, and a tick beside the result 2; the other six say end_turn "
        "and each has a cross beside an Error text such as PermissionError, timed out, no tool named, the human declined, bad arguments, and unsupported expression element.", o)


# ---------------------------------------------------------------- W28-6  blank: pay the bill, turn by turn
def w28_6():
    TURNS = [(1, 247, 28), (2, 415, 10), (3, 448, 25), (4, 519, 19), (5, 566, 20)]    # workbook 28.3 table
    cols = [(40, 80, "turn"), (130, 80, "in"), (220, 80, "out"), (360, 80, "in x 1"), (500, 80, "out x 5"), (620, 160, "in x 1 + out x 5")]
    RH, RS, Y0 = 32, 36, 112
    o = [ctitle("Pay the bill, turn by turn")]
    o.append(t(400, 76, "price: 1.00 per million tokens in, 5.00 per million out; costs in millionths of a dollar", 12, MUT, "middle"))
    for cx, w, lab in cols:
        o.append(t(cx + w / 2.0, 100, lab, 14, INK, "middle"))
    for i, (n, a, b) in enumerate(TURNS):
        y = Y0 + i * RS
        for j, (cx, w, lab) in enumerate(cols):
            if j == 0:
                o.append(rect(cx, y, w, RH, 6, PANEL, GRID, 2))
                o.append(t(cx + w / 2.0, y + RH / 2.0, str(n), 14, INK, "middle", central=True))
            elif j in (1, 2):
                o.append(rect(cx, y, w, RH, 6, DATA_F, DATA_S, 2))
                o.append(t(cx + w / 2.0, y + RH / 2.0, str(a if j == 1 else b), 14, INK, "middle", central=True))
            else:
                o.append(rect(cx, y, w, RH, 6, PAPER, GRID, 2, "6 4"))
    y = Y0 + 5 * RS
    o.append(t(80, y + RH / 2.0, "totals", 14, INK, "middle", central=True))
    for cx, w, lab in cols[1:]:
        o.append(rect(cx, y, w, RH, 6, PAPER, GRID, 2, "6 4"))
    y2 = y + RS
    o.append(t(690, y2 + RH / 2.0, "dollars: $", 14, INK, "end", central=True))
    o.append(rect(700, y2, 80, RH, 6, PAPER, GRID, 2, "6 4"))
    o.append(cap("Pencil: fill every dashed box, then compare the total with the run's printed spend.", 376))
    fig("fig-w28-6-blank-bill-grid", "0 0 800 400",
        "A blank grid for pricing the five turns of the worked run: multiply tokens in by 1 and tokens out by 5, add, and total the columns",
        "A table with six columns: turn, in, out, in times 1, out times 5, and in times 1 plus out times 5. Five rows for turns 1 to 5 have the turn and the in and out token counts printed "
        "(247 and 28, 415 and 10, 448 and 25, 519 and 19, 566 and 20). Every other box is an empty dashed box, including a totals row and a box for the dollars. Nothing is filled in.", o)


# ---------------------------------------------------------------- W29-4  where the soft layers sit and where the hard one sits
def w29_4():
    o = [ctitle("A planted note travels as data")]
    xs = [30, 220, 410, 640]
    o.append(box(30, 78, 150, 70, "planted note", "written by somebody else", BAD_F, BAD_S, 2, "6 4"))
    o.append(box(220, 78, 150, 70, "search result", "comes back as text", DATA_F, DATA_S))
    o.append(box(410, 78, 150, 70, "the model", STAND_IN, MODEL_F, MODEL_S, 2, "6 4"))
    o.append(box(640, 78, 130, 70, "the order", "write_file outside", PAPER, BAD_S, 2, "6 4"))
    o.append(arrow(184, 113, 214, 113, INK, 3))
    o.append(arrow(374, 113, 404, 113, INK, 3))
    o.append(arrow(564, 113, 634, 113, INK, 3))
    # the wall
    o.append(rect(584, 62, 18, 184, 4, OK_F, OK_S, 3))
    o.append(t(593, 262, "layer 3", 14, INK, "middle", weight="600"))
    o.append(t(593, 282, "allowlist  ·  human  ·  sandbox", 12, INK, "middle"))
    o.append(t(593, 300, "never reads the prompt", 12, INK, "middle"))
    o.append(bracket(222, 560, 170, 8, MUT, True))
    o.append(t(391, 202, "layers 1 and 2: wrap the result", 14, INK, "middle", weight="600"))
    o.append(t(391, 222, "and flag marker phrases", 12, INK, "middle"))
    o.append(t(391, 240, "the model is asked to cooperate", 12, INK, "middle"))
    o.append(t(391, 258, "they change how often", 12, MUT, "middle"))
    o.append(t(112, 192, "to the model, the order", 12, MUT, "middle"))
    o.append(t(112, 208, "and the data arrive in", 12, MUT, "middle"))
    o.append(t(112, 224, "the same place: text", 12, MUT, "middle"))
    o.append(t(710, 190, "layer 3 changes what", 12, MUT, "middle"))
    o.append(t(710, 206, "can happen at all", 12, MUT, "middle"))
    o.append(cap("Soft layers lower a rate; only the hard layer bounds the damage.", 350))
    o.append(t(400, 376, "defence in depth: stack the soft layers, rely on the hard one", 12, MUT, "middle"))
    fig("fig-w29-4-note-travels-as-data", "0 0 800 400",
        "A planted note reaches the model as ordinary text; layers 1 and 2 only ask the model to cooperate, layer 3 is a wall that never reads the prompt",
        "A left-to-right chain of four boxes joined by arrows: a dashed planted note written by somebody else, a search result that comes back as text, the model marked stand-in not a model, "
        "and a dashed box for the order, write_file outside the folder. A bracket under the first two arrows is labelled layers 1 and 2, wrap the result and flag marker phrases, which change how often. "
        "A tall green wall between the model and the order is labelled layer 3: allowlist, human and sandbox, which never read the prompt.", o)


# ---------------------------------------------------------------- W29-5  the three fences and the reworded note
def w29_5():
    # student guide section 6 weak.py (100 fully fooled runs, layers 1 and 2 OFF) and section 7 reworded.py (layers 1+2 ON)
    A = [("strict sandbox, human yes", 100, 100, 0), ("WEAK sandbox, human yes", 100, 100, 100), ("WEAK sandbox, human NO", 100, 0, 0)]
    B = [("original note", 32, 0), ("reworded note", 69, 0)]
    bx = [(290, "obeyed"), (450, "reached the sandbox"), (630, "file landed")]
    o = [ctitle("Fooled in every run; the fences decide the rest")]
    o.append(t(20, 76, "100 fully fooled runs, layers 1 and 2 off", 14, INK, "start"))
    for x, lab in bx:
        o.append(t(x, 98, lab, 12, MUT, "start"))
    for i, (lab, ob, rc, ld) in enumerate(A):
        cy = 124 + i * 36
        o.append(t(20, cy, lab, 14, INK, "start", central=True))
        for (x, _), v, kind in zip(bx, (ob, rc, ld), ("d", "d", "l")):
            if v:
                bad = kind == "l"
                o.append(rect(x, cy - 11, v * 1.0, 22, 4, BAD_F if bad else DATA_F, BAD_S if bad else DATA_S, 2))
                o.append(t(x + v + 8, cy, str(v), 12, INK, "start", central=True))
            else:
                o.append(line(x, cy - 11, x, cy + 11, INK, 2))
                o.append(t(x + 8, cy, "0", 12, INK, "start", central=True))
                if kind == "l":
                    o.append(tick(x + 34, cy, 7))
    o.append(line(20, 238, 780, 238, GRID, 2, "6 4"))
    o.append(t(20, 262, "100 fully fooled runs, layers 1 and 2 on, strict sandbox", 14, INK, "start"))
    for i, (lab, ob, ld) in enumerate(B):
        cy = 292 + i * 36
        o.append(t(20, cy, lab, 14, INK, "start", central=True))
        o.append(rect(290, cy - 11, ob, 22, 4, DATA_F, DATA_S, 2))
        o.append(t(290 + ob + 8, cy, str(ob), 12, INK, "start", central=True))
        o.append(line(630, cy - 11, 630, cy + 11, INK, 2))
        o.append(t(638, cy, "0", 12, INK, "start", central=True))
        o.append(tick(664, cy, 7))
    o.append(t(450, 292, "—", 12, MUT, "start", central=True))
    o.append(cap("Rewording raised obeying from 32 to 69; landed stayed 0 (stand-in, not a model).", 376))
    fig("fig-w29-5-fences-and-reworded-note", "0 0 800 400",
        "With every run fooled, the strict sandbox and the human each keep the landed count at 0; a reworded note raises obeying from 32 to 69 but still lands 0",
        "Top block, three rows of horizontal bars out of 100 runs for obeyed, reached the sandbox and file landed: strict sandbox with human yes, 100, 100 and 0; weak sandbox with human yes, 100, 100 and 100; "
        "weak sandbox with human no, 100, 0 and 0. Bottom block, layers 1 and 2 on: the original note obeyed 32 and landed 0, the reworded note obeyed 69 and landed 0. Zero values carry a tick.", o)


# ---------------------------------------------------------------- W29-6  blank: draw the bill
def w29_6():
    x0, y0, x1, y1 = 130, 80, 560, 300         # plot box: k 0..15 across, input tokens 0..8000 up
    o = [ctitle("Draw the bill")]
    for k in (0, 5, 10, 15):
        x = x0 + (x1 - x0) * k / 15.0
        o.append(line(x, y0, x, y1, GRID, 1, cap=False))
        o.append(t(x, y1 + 20, str(k), 12, MUT, "middle"))
    for v in (0, 2000, 4000, 6000, 8000):
        y = y1 - (y1 - y0) * v / 8000.0
        o.append(line(x0, y, x1, y, GRID, 1, cap=False))
        o.append(t(x0 - 8, y, str(v), 12, MUT, "end", central=True))
    o.append(line(x0, y0, x0, y1, INK, 2))
    o.append(line(x0, y1, x1, y1, INK, 2))
    o.append(t((x0 + x1) / 2.0, y1 + 42, "steps k (tool calls)", 12, MUT, "middle"))
    o.append(trot(52, (y0 + y1) / 2.0, "total input tokens", 12, MUT))
    o.append(rect(590, 90, 190, 150, 12, PANEL, GRID, 2))
    o.append(t(685, 112, "your three points", 14, INK, "middle"))
    for i, k in enumerate((0, 5, 15)):
        y = 134 + i * 36
        o.append(t(604, y + 12, "k = %d:" % k, 14, INK, "start", central=True))
        o.append(rect(670, y, 100, 26, 6, PAPER, GRID, 2, "6 4"))
    o.append(cap("Pencil: plot the three points, then join them in order with a ruler.", 372))
    fig("fig-w29-6-blank-bill-axes", "0 0 800 400",
        "Blank axes for the bill: steps k from 0 to 15 across, total input tokens from 0 to 8000 up; plot the totals for k equal to 0, 5 and 15",
        "An empty graph with a grid. The horizontal axis is steps k, a count of tool calls, marked 0, 5, 10 and 15. The vertical axis is total input tokens, marked 0, 2000, 4000, 6000 and 8000. "
        "To the right a panel called your three points has three empty dashed boxes for k equal to 0, 5 and 15. Nothing is plotted.", o)


# ---------------------------------------------------------------- W30-4  four checks on the claim 'it scores 90'
def w30_4():
    o = [ctitle("Before you believe a score")]
    o.append(box(20, 70, 170, 96, "1  freeze first", "write the 30 tickets,", HUMAN_F, HUMAN_S))
    o.append(t(105, 150, "then store a fingerprint", 12, MUT, "middle"))
    o.append(box(215, 70, 170, 96, "2  baseline first", "floor, free rules,", DATA_F, DATA_S))
    o.append(t(300, 150, "then the trained one", 12, MUT, "middle"))
    o.append(box(410, 70, 170, 96, "3  keep test out", "training tickets come", DATA_F, DATA_S))
    o.append(t(495, 150, "after, and are scanned", 12, MUT, "middle"))
    o.append(box(605, 70, 170, 96, "4  check the judge", "agree beyond luck,", MODEL_F, MODEL_S))
    o.append(t(690, 150, "and survive a swap", 12, MUT, "middle"))
    for x in (192, 387, 582):
        o.append(arrow(x, 118, x + 20, 118, INK, 3))
    o.append(t(105, 200, "an edit makes the", 12, INK, "middle"))
    o.append(t(105, 218, "fingerprint shout", 12, INK, "middle"))
    o.append(t(300, 200, "a fancy system must", 12, INK, "middle"))
    o.append(t(300, 218, "beat the rung below", 12, INK, "middle"))
    o.append(t(495, 200, "overlap counts words,", 12, INK, "middle"))
    o.append(t(495, 218, "so it finds copies only", 12, INK, "middle"))
    o.append(t(690, 200, "ask twice, both orders:", 12, INK, "middle"))
    o.append(t(690, 218, "a change is position", 12, INK, "middle"))
    o.append(rect(20, 250, 755, 56, 12, PANEL, GRID, 2))
    o.append(t(397, 270, "then read every category, not only the average", 14, INK, "middle"))
    o.append(t(397, 290, "an average can rise or hold while one category collapses", 12, MUT, "middle"))
    o.append(cap("Four questions in order: what was frozen, what is the rung below, what leaked, who marked it.", 340))
    fig("fig-w30-4-four-checks-before-a-score", "0 0 800 400",
        "Four checks stand between a score and a claim: freeze the test first, beat the rung below, keep the test out of the lessons, and check the judge",
        "Four boxes joined by arrows, numbered 1 to 4. Freeze first: write the thirty tickets, then store a fingerprint, so an edit makes it shout. Baseline first: floor, free rules, then the trained system, "
        "which must beat the rung below. Keep the test out: training tickets come after and are scanned, but overlap is a word count that finds copies and not rewordings. "
        "Check the judge: agree beyond luck and survive a swap of order. A panel underneath says to read every category, not only the average.", o)


# ---------------------------------------------------------------- W30-5  Jaccard by hand and what the scan caught
def w30_5():
    # student guide section 4 (p3_jaccard.py) and section 5 (p4_leak.py)
    BOTH = ["am", "i", "month", "now", "paying", "right", "what"]
    o = [ctitle("Words in common, and what the scan saw")]
    o.append(t(20, 76, "a training ticket and an eval ticket", 14, INK, "start"))
    o.append(rect(20, 90, 396, 100, 12, PANEL, GRID, 2))
    o.append(t(32, 112, "A only", 12, MUT, "start"))
    o.append(chip(32, 122, 56, "each", DATA_S, PAPER, 12, 26))
    o.append(t(404, 112, "B only", 12, MUT, "end"))
    o.append(chip(350, 122, 54, "per", DATA_S, PAPER, 12, 26))
    o.append(t(208, 112, "in both: 7", 12, INK, "middle"))
    for i, w in enumerate(BOTH):
        o.append(chip(122 + (i % 4) * 56, 122 + (i // 4) * 30, 54, w, ACC_S, ACC_F, 12, 26))
    o.append(t(20, 214, "7 in both  /  9 in either  =  0.778", 14, INK, "start"))
    o.append(t(20, 238, "same question, other words:  0 in both  =  0.000", 14, INK, "start"))
    o.append(t(20, 266, "The scan compares words, not meaning.", 12, MUT, "start"))
    # right: scores
    o.append(t(450, 76, "three training sets, one classifier", 14, INK, "start"))
    S = [("64 kept by the scan", 21), ("all 66, no scan", 22), ("64 + 5 paraphrases", 23)]
    for i, (lab, v) in enumerate(S):
        cy = 112 + i * 40
        o.append(t(450, cy - 18, lab, 12, INK, "start"))
        o.append(rect(450, cy - 8, v * 10.0, 24, 4, DATA_F, DATA_S, 2))
        o.append(t(450 + v * 10 + 8, cy + 4, "%d/30" % v, 12, INK, "start", central=True))
    o.append(line(450, 84, 450, 236, INK, 2))
    o.append(t(450, 252, "paraphrases the scan caught: 0 of 5", 14, INK, "start"))
    o.append(t(450, 272, "highest overlap with any eval", 12, MUT, "start"))
    o.append(t(450, 288, "ticket: 0.077 to 0.200", 12, MUT, "start"))
    o.append(rect(20, 296, 760, 44, 8, PAPER, GRID, 2, "6 4"))
    o.append(t(400, 318, "23 beats 21 only by memory of the paraphrases; it does not mean a better system", 14, INK, "middle", central=True))
    o.append(cap("A threshold on word overlap catches copies; it never saw the five rewordings.", 372))
    fig("fig-w30-5-overlap-and-what-it-missed", "0 0 800 400",
        "Word overlap of 7 in both over 9 in either is 0.778 for a near-copy, 0.000 for a reworded question; the scan caught none of five paraphrases, which still lifted the score from 21 to 23 of 30",
        "Left, a panel with two word sets for the tickets what am I paying each month right now and what am I paying per month right now: each is only in A, per is only in B, and seven words are in both. "
        "Beneath it the sum seven over nine is 0.778 and a reworded question scores 0.000. Right, three bars of the same classifier scored out of 30: 21 with 64 tickets kept by the scan, "
        "22 with all 66, and 23 with 64 plus five paraphrases, then the note that the scan caught none of five and the highest overlap was 0.077 to 0.200.", o)


# ---------------------------------------------------------------- W30-6  blank: kappa worksheet
def w30_6():
    o = [ctitle("Kappa by hand: fill the worksheet")]
    gx, gy, cw, ch = 130, 112, 96, 56
    o.append(t(gx + cw / 2.0, 100, "H pass", 14, INK, "middle"))
    o.append(t(gx + cw * 1.5 + 8, 100, "H fail", 14, INK, "middle"))
    o.append(t(gx + 2 * (cw + 8) + 35, 100, "row total", 12, MUT, "middle"))
    o.append(t(gx - 12, gy + ch / 2.0 - 2, "J pass", 14, INK, "end", central=True))
    o.append(t(gx - 12, gy + ch * 1.5 - 2, "J fail", 14, INK, "end", central=True))
    for r in range(2):
        for c in range(2):
            o.append(rect(gx + c * (cw + 8), gy + r * ch, cw, ch - 4, 6, PAPER, GRID, 2, "6 4"))
        o.append(rect(gx + 2 * (cw + 8), gy + r * ch, 70, ch - 4, 6, PAPER, GRID, 2, "6 4"))
    for c in range(2):
        o.append(rect(gx + c * (cw + 8), gy + 2 * ch, cw, ch - 4, 6, PAPER, GRID, 2, "6 4"))
    o.append(t(gx - 12, gy + 2.5 * ch - 2, "column total", 12, MUT, "end", central=True))
    sx = 500
    o.append(rect(sx - 20, 90, 300, 232, 12, PANEL, GRID, 2))
    steps = [("p_o  =", "both pass + both fail, over 20"), ("p_e  =", "J pass x H pass + J fail x H fail"), ("kappa =", "(p_o - p_e) / (1 - p_e)")]
    for i, (a, b) in enumerate(steps):
        y = 104 + i * 70
        o.append(ring_num(sx, y + 12, i + 1))
        o.append(t(sx + 20, y + 12, a, 14, INK, "start", central=True))
        o.append(rect(sx + 90, y, 100, 26, 6, PAPER, GRID, 2, "6 4"))
        o.append(t(sx, y + 46, b, 12, MUT, "start", central=True))
    o.append(cap("Pencil: tally the 20 tickets into the grid, add the totals, then do the three steps.", 372))
    fig("fig-w30-6-blank-kappa-worksheet", "0 0 800 400",
        "A blank worksheet for Cohen's kappa: a two by two grid of J and H verdicts with row and column totals, and three empty boxes for p_o, p_e and kappa",
        "On the left a two by two grid of empty dashed boxes. The columns are H pass and H fail, the rows are J pass and J fail, with an empty box for each row total and each column total. "
        "On the right a panel with three numbered steps, p_o, p_e and kappa, each with an empty box and a one-line reminder of what to compute. Nothing is filled in.", o)


def build():
    for f in (w28_4, w28_5, w28_6, w29_4, w29_5, w29_6, w30_4, w30_5, w30_6):
        f()
    return FIGS
