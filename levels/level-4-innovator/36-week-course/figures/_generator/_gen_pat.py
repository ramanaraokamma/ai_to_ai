"""Level 4 composition patterns (STYLE.md section 6). Each is a standalone figure on a standard canvas.

Every pattern is built to be a real, finished figure: the audit checks them at the 20px padding.
Numbers come from _gen_data.py (same provenance rules as the motifs).
"""
from _gen_core import *
import _gen_data as D
import _gen_motifs as MO
from _gen_motifs import E_MINUS, E_TIMES, E_DIV, E_ARROW, E_MID, E_ELL, frame, curve, every

import xml.etree.ElementTree as _ET  # noqa: F401

BY_ID = {m["id"]: m for m in MOTIFS}
PATTERNS = []
EXAMPLES = []          # Level 3 had banned-vs-good worked examples; Level 4's rules live in STYLE.md 3.


def place(mid, x, y):
    """Place a motif at 1:1 (never scaled: STYLE 1.8)."""
    return '  <g transform="translate(%s,%s)">\n%s\n  </g>' % (x, y, BY_ID[mid]["body"])


def P(pid, title, desc, vb, note, body):
    PATTERNS.append(dict(id=pid, title=title, desc=desc, vb=vb, note=note, body=body.strip("\n")))


# ============================================================ 1. pipeline
def _glyph_chunks(x, y):
    o = []
    for i in range(5):
        o.append(sq(x + i * 22, y, 22, 40, DATA_F, DATA_S, 2))
    o.append(rect(x, y, 110, 40, 0, "none", DATA_S, 3))
    return o


def _glyph_embed(x, y):
    pts = [(10, 40), (30, 14), (46, 48), (70, 26), (90, 52)]
    o = [line(x, y + 62, x + 100, y + 62, INK, 2), line(x, y, x, y + 62, INK, 2)]
    o += [circ(x + px, y + py, 6, DATA_F, DATA_S, 2) for px, py in pts]
    return o


def _glyph_retrieve(x, y):
    o = [rect(x + 34, y + 16, 32, 32, 4, ACC_F, ACC_S, 3)]
    for px, py, ok in ((6, 0, 0), (82, 6, 1), (88, 46, 1), (10, 52, 0), (56, 62, 0)):
        o.append(circ(x + px + 8, y + py + 8, 7, OK_F if ok else PANEL, OK_S if ok else GRID, 2))
    o.append(line(x + 50, y + 32, x + 90, y + 14, OK_S, 2))
    o.append(line(x + 50, y + 32, x + 96, y + 54, OK_S, 2))
    return o


def _glyph_cite(x, y):
    o = [rect(x + 6, y, 84, 62, 8, PAPER, INK, 3)]
    for i in range(3):
        o.append(line(x + 18, y + 16 + i * 14, x + 78 - (i == 2) * 24, y + 16 + i * 14, GRID, 3))
    o.append(circ(x + 90, y + 64, 12, OK_F, OK_S, 2))
    o.append(tick(x + 90, y + 64, 6))
    return o


def _pipeline():
    o = [t(400, 46, "Retrieval pipeline: chunk, embed, retrieve, cite", 24, INK, "middle")]
    stages = [(30, _glyph_chunks, "1. Chunk", "15 notes cut up"), (230, _glyph_embed, "2. Embed", "a point for each"),
              (430, _glyph_retrieve, "3. Retrieve", "top k = 2 nearest"), (630, _glyph_cite, "4. Cite", "[14] checked")]
    for x, fn, a, b in stages:
        o.append(rect(x, 96, 140, 200, 12, PAPER, DATA_S, 3))
        o += fn(x + 18, 150)
        o.append(t(x + 70, 326, a, 18, INK, "middle"))
        o.append(t(x + 70, 346, b, 12, MUT, "middle"))
    for x in (176, 376, 576):
        o.append(arrow(x, 196, x + 48, 196, INK, 3))
    o.append(t(400, 376, "Each stage can be wrong: diagnose by reading the chunks.", 14, MUT, "middle"))
    return J(o)


P("pattern-pipeline", "Retrieval is four stages, left to right",
  "Four boxes joined by arrows: chunk the 15 notes, embed each as a point, retrieve the top 2 nearest to "
  "the question, and cite [14] with a check. Each stage has a text-free picture and an 18px label.",
  "0 0 800 400", "3-5 stages, text-free glyphs, 18px labels (words never ride on a scaled glyph).", _pipeline())


# ============================================================ 2. before / after
def _bars(x0, ybase, per, ymap, items):
    o = []
    for i, (lab, v, f, s) in enumerate(items):
        x = x0 + i * (per + 14)
        o.append(sq(x, ymap(v), per, ybase - ymap(v), f, s, 3))
        o.append(t(x + per / 2.0, ymap(v) - 8, "%.3f" % v, 14, INK, "middle"))
        o.append(t(x + per / 2.0, ybase + 20, lab, 12, MUT, "middle"))
    return o


def _before_after():
    ymap = lambda v: 320 - 200 * v / 3.0
    o = [t(400, 46, "No residual path, no learning", 24, INK, "middle")]
    for px, ok, ttl, items in ((30, False, "no residual", [("train", 2.843, DATA_F, DATA_S), ("val", 2.849, HUMAN_F, HUMAN_S)]),
                               (420, True, "with residual", [("train", 0.411, DATA_F, DATA_S), ("val", 1.336, HUMAN_F, HUMAN_S)])):
        o.append(rect(px, 68, 350, 290, 12, BAD_F if not ok else OK_F, BAD_S if not ok else OK_S, 3))
        o.append(t(px + 20, 98, ttl, 18, INK, "start"))
        o.append(line(px + 40, 120, px + 40, 320, INK, 2))
        o.append(line(px + 40, 320, px + 330, 320, INK, 2))
        for v in (0, 1, 2, 3):
            o.append(line(px + 40, ymap(v) - 0, px + 330, ymap(v), GRID, 1.5, cap=False))
            o.append(t(px + 34, ymap(v), str(v), 12, MUT, "end", central=True))
        o += _bars(px + 90, 320, 70, ymap, items)
        if ok:
            o.append(tick(px + 312, 98, 10))
        else:
            o.append(cross(px + 312, 98, 9))
    o.append(t(400, 374, "Final loss after 1,500 steps %s seed 1337 %s same axes both sides" % (E_MID, E_MID), 12, MUT, "middle"))
    return J(o)


P("pattern-before-after", "Residual connections decide whether the network learns at all",
  "Two panels with the same loss axis from 0 to 3. Left, no residual path: final training loss 2.843 and "
  "validation loss 2.849 after 1,500 steps, flat and broken, marked with a cross. Right, with the residual "
  "path: training loss 0.411 and validation loss 1.336, marked with a tick.",
  "0 0 800 400", "Two panels, wrong left and correct right, identical axes. Real ablation numbers (Week 19 ledger).",
  _before_after())


# ============================================================ 3. knob sweep
def _knob_sweep():
    o = [t(400, 46, "One knob, three settings: the learning rate", 24, INK, "middle")]
    kinds = {0.02: ("diamond", HUMAN_S, "2 4"), 0.2: ("square", MODEL_S, "6 4"), 1.0: ("circle", DATA_S, None)}
    for i, lr in enumerate(D.DEMO_LRS):
        px = 20 + i * 262
        ys = D.DEMO[lr]
        xs = list(range(len(ys)))
        xm = lambda v, px=px: px + 50 + 170 * v / 40.0
        ym = lambda v: 300 - 190 * v / 0.8
        k, col, dash = kinds[lr]
        o.append(rect(px, 70, 236, 290, 12, PANEL, GRID, 2))
        o.append(t(px + 120, 96, "learning rate %s" % lr, 18, INK, "middle"))
        o.append(line(px + 50, 110, px + 50, 300, INK, 2))
        o.append(line(px + 50, 300, px + 220, 300, INK, 2))
        for v in (0, 0.4, 0.8):
            o.append(line(px + 50, ym(v), px + 220, ym(v), GRID, 1.5, cap=False))
            o.append(t(px + 44, ym(v), "%.1f" % v, 12, MUT, "end", central=True))
        o.append(line(px + 50, ym(D.LN2), px + 220, ym(D.LN2), GRID, 2, "6 4"))
        o.append(curve(xs, ys, xm, ym, col, 3, dash))
        o += every(xs, ys, xm, ym, k, col, 10, 4)
        o.append(mark(k, xm(40), ym(ys[-1]), 6, col, PAPER, 3))
        o.append(t(px + 120, 324, "step", 12, MUT, "middle"))
        o.append(t(px + 120, 346, "last loss %.3f" % ys[-1], 14, INK, "middle"))
    o.append(t(400, 374, "Same y axis in all three. Dashed line: ln 2 = 0.693. seed 0, 40 steps.", 12, MUT, "middle"))
    return J(o)


P("pattern-knob-sweep", "Same run, learning rate changed: 0.02, 0.2 and 1.0",
  "Three small panels sharing a loss axis from 0 to 0.8, each with the dashed ln 2 = 0.693 line. Learning "
  "rate 0.02 (dotted, diamonds) ends at %.3f, 0.2 (dashed, squares) at %.3f and 1.0 (solid, circles) at %.3f, "
  "after 40 steps with seed 0." % (D.DEMO[0.02][-1], D.DEMO[0.2][-1], D.DEMO[1.0][-1]),
  "0 0 800 400", "Three small multiples, same y axis, one knob changed; dash + marker + printed end value per panel.",
  _knob_sweep())


# ============================================================ 4. worked attention
def _worked_attention():
    toks, S, W, V, O = D.ATT_TOKENS, D.ATT_SCORES[2], D.ATT_W[2], D.ATT_V, D.ATT_OUT[2]
    o = [t(400, 46, "Attention for the word sat: compare, weigh, blend", 24, INK, "middle")]
    cols = [(30, "1. scores"), (230, "2. weights"), (430, "3. values")]
    for x, h in cols:
        o.append(t(x + 80, 92, h, 18, INK, "middle"))
    o.append(t(690, 92, "4. blend", 18, INK, "middle"))
    ys = [130, 190, 250]
    for i, tk in enumerate(toks):
        y = ys[i]
        me = i == 2
        o.append(rect(30, y, 160, 42, 8, ACC_F if me else DATA_F, ACC_S if me else DATA_S, 4 if me else 3))
        o.append(t(42, y + 21, tk, 14, INK, "start", mono=True, central=True))
        bw = 30 * S[i]
        o.append(sq(92, y + 10, bw, 22, DATA_F, DATA_S, 2))
        o.append(t(184, y + 21, str(S[i]), 14, INK, "end", mono=True, central=True))
        o.append(rect(230, y, 160, 42, 8, PAPER, MODEL_S, 3))
        o.append(sq(240, y + 10, 90 * W[i], 22, MODEL_F, MODEL_S, 2))
        o.append(t(382, y + 21, "%.4f" % W[i], 14, INK, "end", mono=True, central=True))
        o.append(rect(430, y, 160, 42, 8, DATA_F, DATA_S, 3))
        o.append(t(510, y + 21, "(%.0f, %.0f)" % tuple(V[i]), 14, INK, "middle", mono=True, central=True))
    for x in (194, 394):
        for y in ys:
            o.append(arrow(x, y + 21, x + 32, y + 21, INK, 2.5))
    o.append(arrow(594, 190 + 21, 626, 190 + 21, INK, 3))
    o.append(rect(630, 150, 140, 100, 12, MODEL_F, MODEL_S, 4))
    o.append(t(700, 190, "(0.788,", 18, INK, "middle", mono=True, central=True))
    o.append(t(700, 218, "0.788)", 18, INK, "middle", mono=True, central=True))
    o.append(shape_chip(666, 262, "(2,)"))
    o.append(t(400, 322, "0.2119 %s (0, 1) + 0.2119 %s (1, 0) + 0.5761 %s (1, 1) = (0.788, 0.788)" % (E_TIMES, E_TIMES, E_TIMES), 14, INK, "middle"))
    o.append(t(400, 348, "Scores 1, 1, 2 become three weights that add to 1. 3 tokens, 2 numbers each.", 12, MUT, "middle"))
    o.append(t(400, 372, "The weights are a blend recipe; the answer is the blend of the values.", 12, MUT, "middle"))
    return J(o)


P("pattern-worked-attention", "One word's attention pass: scores, weights, values, blended answer",
  "Three token rows the, cat, sat; sat is the query, outlined in accent. Scores 1, 1 and 2 become weights "
  "0.2119, 0.2119 and 0.5761 that add to 1. The values (0, 1), (1, 0), (1, 1) are blended into the answer "
  "(0.788, 0.788), with the sum worked out underneath.",
  "0 0 800 400", "Tokens, scores, weights, values, blended output, left to right; the sum on the page.",
  _worked_attention())


# ============================================================ 5. loop
P("pattern-loop", "The agent loop, with the trace beneath it",
  BY_ID["motif-agent-loop"]["desc"], "0 0 800 400",
  "A cycle with the current step accent and the real trace strip under it; stand-in framed and chipped.",
  J([t(400, 44, "The agent loop and what it did", 24, INK, "middle")]) + "\n" + place("motif-agent-loop", 0, 52))

# ============================================================ 6. table plus chart
def _table_chart():
    o = [t(400, 46, "The average rose; one category fell", 24, INK, "middle")]
    rows = [("all (average)", 30, 18, 19)] + [(c, n, b, a) for c, n, b, a in D.LORA_TABLE]
    o.append(t(40, 96, "category", 14, INK, "start", weight="600"))
    o.append(t(230, 96, "before", 14, INK, "middle", weight="600"))
    o.append(t(310, 96, "after", 14, INK, "middle", weight="600"))
    o.append(line(30, 108, 360, 108, INK, 2))
    ym = lambda v: 330 - 190 * v
    for i, (c, n, b, a) in enumerate(rows):
        y = 120 + i * 70
        bad = a < b
        o.append(rect(30, y, 330, 58, 8, BAD_F if bad else PAPER, BAD_S if bad else GRID, 3 if bad else 2))
        o.append(ring_num(54, y + 29, i + 1))
        o.append(t(74, y + 29, c, 14, INK, "start", central=True))
        o.append(t(230, y + 29, "%d / %d" % (b, n), 14, INK, "middle", central=True))
        o.append(t(310, y + 29, "%d / %d" % (a, n), 14, INK, "middle", central=True))
        if bad:
            o.append(cross(346, y + 12, 5))
    o.append(line(430, 130, 430, 330, INK, 2))
    o.append(line(430, 330, 770, 330, INK, 2))
    for v in (0, 0.5, 1):
        o.append(line(430, ym(v), 770, ym(v), GRID, 1.5, cap=False))
        o.append(t(422, ym(v), "%.1f" % v, 12, MUT, "end", central=True))
    for i, (c, n, b, a) in enumerate(rows):
        gx = 450 + i * 108
        bv, av = b / n, a / n
        o.append(sq(gx, ym(bv), 36, 330 - ym(bv), DATA_F, DATA_S, 3))
        o.append(sq(gx + 40, ym(av), 36, 330 - ym(av), MODEL_F, MODEL_S, 3))
        o.append(t(gx + 18, ym(bv) - 7, "%.2f" % bv, 12, INK, "middle"))
        o.append(t(gx + 58, ym(av) - 7, "%.2f" % av, 12, INK, "middle"))
        o.append(ring_num(gx + 38, 350, i + 1))
    o.append(sq(440, 100, 14, 14, DATA_F, DATA_S, 2))
    o.append(t(460, 107, "before (base)", 12, INK, "start", central=True))
    o.append(sq(580, 100, 14, 14, MODEL_F, MODEL_S, 2))
    o.append(t(600, 107, "after (LoRA patch)", 12, INK, "start", central=True))
    o.append(t(400, 374, "Same numbers in table and chart, matched by ringed number. Billing: one ticket of n = 5.", 12, MUT, "middle"))
    return J(o)


P("pattern-table-plus-chart", "Table and chart show the same three rows, matched by number",
  "A table on the left and a paired bar chart on the right, rows matched by ringed numbers 1, 2, 3. "
  "1 all: 18 of 30 before, 19 of 30 after. 2 technical: 2 of 7 to 4 of 7. 3 billing: 2 of 5 to 1 of 5, "
  "highlighted as the regression. Bars show fractions 0.60 to 0.63, 0.29 to 0.57 and 0.40 to 0.20.",
  "0 0 800 400", "A chart with ringed numbers matching a table (STYLE 2.8). Week 31 numbers.", _table_chart())


# ============================================================ 7. error / fix
def _error_fix():
    o = [t(400, 46, "Read the error, fix the path, run again", 24, INK, "middle")]
    o.append(t(200, 92, "before", 18, BAD_S, "middle"))
    o.append(t(600, 92, "after", 18, OK_S, "middle"))
    left = ["turn 3", "write_file  ERR", "ValueError: directory 'reports'", "does not exist in the sandbox"]
    right = ["turn 4", "write_file  ok", "wrote 47 bytes to", "extraction-250.md"]
    o.append(terminal(30, 110, 350, left, 12, 22, hi=2))
    o.append(terminal(420, 110, 350, right, 12, 22, hi=1))
    o.append(cross(360, 124, 7))
    o.append(tick(750, 124, 9))
    o.append(arrow(384, 170, 416, 170, INK, 3))
    o.append(t(200, 250, "the error names the problem:", 14, INK, "middle"))
    o.append(t(200, 272, "no folder called reports", 14, INK, "middle"))
    o.append(t(600, 250, "same request, flat file name:", 14, INK, "middle"))
    o.append(t(600, 272, "the write lands", 14, INK, "middle"))
    o.append(chip(314, 306, 172, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))
    o.append(t(400, 364, "Errors are curriculum: the stand-in recovered because a person scripted it to.", 12, MUT, "middle"))
    return J(o)


P("pattern-error-fix", "A failed tool call, the error it printed, then the fixed call",
  "Two terminal panels. Before: turn 3 write_file returned ValueError, directory 'reports' does not exist "
  "in the sandbox, marked with a cross. After: turn 4 write_file ok, wrote 47 bytes to extraction-250.md, "
  "marked with a tick. A chip says stand-in, not a model.",
  "0 0 800 400", "Terminal of at most 5 lines with annotation, then the fixed run (section 1.9).", _error_fix())


# ============================================================ 8. trace (tall)
P("pattern-trace", "One agent run, row by row",
  BY_ID["motif-trace"]["desc"], "0 0 500 700",
  "One row per step: action, observation, tokens so far. Current step accent and weight 600.",
  J([t(250, 44, "One agent run, row by row", 24, INK, "middle")]) + "\n" + place("motif-trace", 0, 56))


BY_PAT = {p["id"]: p for p in PATTERNS}
