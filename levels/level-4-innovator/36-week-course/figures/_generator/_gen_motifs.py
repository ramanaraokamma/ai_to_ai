"""Level 4 motif library (STYLE.md section 4) -- the motifs weeks will actually use.

Every number printed here is traced in _gen_data.py (seeded demo run, ledger output, or a
printed hand sum). Motifs are drawn to their own viewBox with the origin top-left. No
text-bearing motif is ever placed below scale 1.0 (STYLE.md 1.8).
"""
from _gen_core import *
import _gen_data as D

E_MINUS = "&#8722;"
E_TIMES = "&#215;"
E_DIV = "&#247;"
E_ARROW = "&#8594;"
E_INF = "&#8734;"
E_DASH = "&#8211;"
E_MID = "&#183;"
E_ELL = "&#8230;"


# ------------------------------------------------------------------ chart scaffolding
def frame(x0, y_top, x1, y_bot, xmap, ymap, xticks, yticks, xtitle, ytitle, xfmt=str, yfmt=str):
    """Axes, light grid lines at the y ticks, tick numbers, and axis titles (all 12px)."""
    o = []
    for v in yticks:
        o.append(line(x0, ymap(v), x1, ymap(v), GRID, 1.5, cap=False))
    o.append(line(x0, y_top, x0, y_bot, INK, 2))
    o.append(line(x0, y_bot, x1, y_bot, INK, 2))
    for v in yticks:
        o.append(t(x0 - 8, ymap(v), yfmt(v), 12, MUT, "end", central=True))
    for v in xticks:
        o.append(t(xmap(v), y_bot + 18, xfmt(v), 12, MUT, "middle"))
    o.append(t((x0 + x1) / 2.0, y_bot + 40, xtitle, 12, MUT, "middle"))
    o.append(trot(x0 - 50, (y_top + y_bot) / 2.0, ytitle))
    return o


def curve(xs, ys, xmap, ymap, color, sw=3, dash=None):
    return poly([(xmap(x), ymap(y)) for x, y in zip(xs, ys)], "none", color, sw, dash)


def every(xs, ys, xmap, ymap, kind, color, step, r=4):
    out = []
    for i in range(0, len(xs) - 1, step):
        out.append(mark(kind, xmap(xs[i]), ymap(ys[i]), r, color, PAPER, 2))
    return out


# ------------------------------------------------------------------ TRAINING AND LOSS
def _loss_scales(x0=80, x1=440, y_top=60, y_bot=420, ymax=0.8, xmax=D.DEMO_STEPS):
    return (lambda v: x0 + (x1 - x0) * v / xmax), (lambda v: y_bot - (y_bot - y_top) * v / ymax)


def _body_loss_curve():
    lr = 0.2
    ys = D.DEMO[lr]
    xs = list(range(len(ys)))
    xm, ym = _loss_scales()
    o = frame(80, 60, 440, 420, xm, ym, [0, 10, 20, 30, 40], [0, 0.2, 0.4, 0.6], "step", "loss",
              yfmt=lambda v: "%.1f" % v)
    o.append(line(80, ym(D.LN2), 440, ym(D.LN2), GRID, 2, "6 4"))
    o.append(t(440, ym(D.LN2) - 8, "coin flip: ln 2 = 0.693", 12, MUT, "end"))
    o.append(curve(xs, ys, xm, ym, DATA_S, 3))
    o.append(mark("circle", xm(0), ym(ys[0]), 6, DATA_S, ACC_F, 3))
    o.append(mark("circle", xm(40), ym(ys[-1]), 6, DATA_S, PAPER, 3))
    o.append(t(94, ym(ys[0]) + 28, "first %.3f" % ys[0], 12, INK))
    o.append(t(432, ym(ys[-1]) - 14, "last %.3f" % ys[-1], 12, INK, "end"))
    o.append(t(250, 480, "seed %d %s %d steps %s learning rate %s" % (D.DEMO_SEED, E_MID, D.DEMO_STEPS, E_MID, lr),
               12, MUT, "middle"))
    return J(o)


M("motif-loss-curve", "One run's loss falls from the coin-flip line",
  "Loss against step for one seeded run (seed 0, learning rate 0.2, 40 steps): it starts at 0.693, "
  "the dashed ln 2 coin-flip line, and ends at %.3f." % D.DEMO[0.2][-1],
  "0 0 500 500", _body_loss_curve(),
  "A single run. Print first and last loss and the seed. Generator demo run: numpy logistic "
  "regression, 200 seeded points, weights start at zero (so the first loss is exactly ln 2).")


def _body_loss_compare():
    xm, ym = _loss_scales(80, 360)
    o = frame(80, 60, 360, 420, xm, ym, [0, 10, 20, 30, 40], [0, 0.2, 0.4, 0.6], "step", "loss",
              yfmt=lambda v: "%.1f" % v)
    o.append(line(80, ym(D.LN2), 360, ym(D.LN2), GRID, 2, "6 4"))
    style = {0.02: (HUMAN_S, "2 4", "diamond"), 0.2: (MODEL_S, "6 4", "square"), 1.0: (DATA_S, None, "circle")}
    ends = []
    for lr in D.DEMO_LRS:
        col, dash, kind = style[lr]
        ys = D.DEMO[lr]
        xs = list(range(len(ys)))
        o.append(curve(xs, ys, xm, ym, col, 3, dash))
        o += every(xs, ys, xm, ym, kind, col, 8, 4)
        o.append(mark(kind, xm(40), ym(ys[-1]), 6, col, PAPER, 3))
        ends.append((ym(ys[-1]), lr, ys[-1]))
    ends.sort()
    last = -99
    for y, lr, v in ends:                      # nudge end labels apart (>= 18 px)
        ly = max(y, last + 18)
        o.append(t(374, ly, "lr %s %s %.3f" % (lr, E_ARROW, v), 12, INK, central=True))
        last = ly
    o.append(t(250, 480, "seed %d %s %d steps %s same start, ln 2 = 0.693" % (D.DEMO_SEED, E_MID, D.DEMO_STEPS, E_MID),
               12, MUT, "middle"))
    return J(o)


M("motif-loss-compare", "Three learning rates, told apart by dash, marker and end label",
  "Three loss curves on shared axes, all starting at 0.693. Learning rate 1.0 is solid with circles and "
  "ends at %.3f; 0.2 is dashed with squares and ends at %.3f; 0.02 is dotted with diamonds and ends at %.3f."
  % (D.DEMO[1.0][-1], D.DEMO[0.2][-1], D.DEMO[0.02][-1]),
  "0 0 500 500", _body_loss_compare(),
  "Two to three runs only (three roles max). Each series: its own dash, marker shape and a direct "
  "end label; no legend-only identification (STYLE 2.3). Print every end value and the seed.")


def _body_train_val():
    xs, tr, va = D.GPT_STEPS, D.GPT_TRAIN, D.GPT_VAL
    xm = lambda v: 80 + 310 * v / 2500.0
    ym = lambda v: 420 - 360 * v / 3.5
    o = frame(80, 60, 390, 420, xm, ym, [0, 500, 1000, 1500, 2000, 2500], [0, 1, 2, 3], "step", "loss",
              xfmt=lambda v: str(v) if v < 1000 else "%d,%03d" % (v // 1000, v % 1000),
              yfmt=lambda v: str(v))
    o.append(curve(xs, tr, xm, ym, DATA_S, 3))
    o += [mark("circle", xm(x), ym(y), 4, DATA_S, PAPER, 2) for x, y in zip(xs[:-1], tr[:-1])]
    o.append(mark("circle", xm(xs[-1]), ym(tr[-1]), 6, DATA_S, PAPER, 3))
    o.append(curve(xs, va, xm, ym, HUMAN_S, 3, "6 4"))
    o += [mark("square", xm(x), ym(y), 4, HUMAN_S, PAPER, 2) for x, y in zip(xs[:-1], va[:-1])]
    o.append(mark("square", xm(xs[-1]), ym(va[-1]), 6, HUMAN_S, PAPER, 3))
    xe = xm(xs[-1]) + 10
    o.append(path("M%s %s H%s V%s H%s" % (f2(xe - 4), f2(ym(va[-1])), f2(xe + 8), f2(ym(tr[-1])), f2(xe - 4)),
                  "none", ACC_S, 3))
    o.append(t(xe + 16, ym(va[-1]) - 2, "val %.3f" % va[-1], 12, INK, central=True))
    o.append(t(xe + 16, (ym(va[-1]) + ym(tr[-1])) / 2.0, "gap %.3f" % D.GPT_GAP, 14, ACC_S, central=True))
    o.append(t(xe + 16, ym(tr[-1]) + 2, "train %.3f" % tr[-1], 12, INK, central=True))
    o.append(t(250, 480, "seed 1337 %s printed every 500 steps %s gap = %.3f %s %.3f" % (E_MID, E_MID, va[-1], E_MINUS, tr[-1]),
               12, MUT, "middle"))
    return J(o)


M("motif-train-val-gap", "Training loss keeps falling while validation loss turns up",
  "Training loss (solid, circles) falls from 3.340 to 0.148 over 2,499 steps. Validation loss (dashed, "
  "squares) falls to 1.328 at step 1000 then rises to 1.682. The gap at the end is 1.534, bracketed.",
  "0 0 500 500", _body_train_val(),
  "TinyGPT, seed 1337, ledger run. Print both end values and their difference. Role pairing: "
  "train = data, validation = human, bracket = accent.")


def _body_coin():
    ys = D.DEMO[0.2]
    xm = lambda v: 90 + 640 * v / D.DEMO_STEPS
    ym = lambda v: 210 - 170 * v / 0.8
    o = [line(90, 30, 90, 210, INK, 2), line(90, 210, 730, 210, INK, 2)]
    o.append(t(82, ym(0), "0", 12, MUT, "end", central=True))
    o.append(t(82, ym(0.4), "0.4", 12, MUT, "end", central=True))
    o.append(line(90, ym(D.LN2), 730, ym(D.LN2), GRID, 3, "6 4"))
    o.append(curve(list(range(len(ys))), ys, xm, ym, DATA_S, 3))
    o.append(mark("circle", xm(0), ym(ys[0]), 6, DATA_S, ACC_F, 3))
    o.append(chip(480, ym(D.LN2) - 31, 250, "ln 2 = 0.693: a coin flip", ACC_S, ACC_F, 12, 26, mono=False))
    o.append(t(410, 232, "step", 12, MUT, "middle"))
    o.append(t(400, 254, "Two classes, no skill: loss = ln 2. Learning means falling below this line.",
               14, MUT, "middle"))
    return J(o)


M("motif-coin-floor", "A two-class model that knows nothing sits at 0.693",
  "A dashed horizontal line at loss 0.693, which is ln 2, the coin-flip floor. A run starting there "
  "falls below it to %.3f after 40 steps." % D.DEMO[0.2][-1],
  "0 0 800 260", _body_coin(),
  "Print 0.693. Use above any loss plot of a two-class problem so 'no better than a coin' is visible.")


def _body_lr():
    xm = lambda v: 80 + 360 * v / D.LR_TOTAL
    ym = lambda v: 420 - 360 * v / 3.2e-4
    ticks = [0, 1e-4, 2e-4, 3e-4]
    lab = {0: "0", 1e-4: "1e-4", 2e-4: "2e-4", 3e-4: "3e-4"}
    steps = list(range(0, D.LR_TOTAL + 1, 25))
    o = frame(80, 60, 440, 420, xm, ym, [0, 500, 1000, 1500, 2000, 2500], ticks, "step", "learning rate",
              xfmt=lambda v: str(v) if v < 1000 else "%d,%03d" % (v // 1000, v % 1000), yfmt=lambda v: lab[v])
    o.append(curve(steps, [D.lr_at(s) for s in steps], xm, ym, MODEL_S, 3))
    o.append(mark("circle", xm(D.LR_WARM), ym(D.LR_PEAK), 7, ACC_S, ACC_F, 3))
    o.append(t(xm(D.LR_WARM) + 14, ym(D.LR_PEAK) - 4, "peak 3e-4 at step 100", 12, INK))
    o.append(t(250, 480, "warmup 100 steps %s then cosine down to 0 at step 2,500" % E_MID, 12, MUT, "middle"))
    return J(o)


M("motif-lr-schedule", "Learning rate warms up for 100 steps, then decays",
  "Learning rate against step: it climbs in a straight line from 0 to the peak 3e-4 at step 100 "
  "(marked), then follows a cosine down to 0 at step 2,500.",
  "0 0 500 500", _body_lr(),
  "AdamW peak 3e-4, 100 warmup steps, 2,500 total (the Week 17 run). Print peak lr and warmup steps.")


# ------------------------------------------------------------------ SEQUENCES AND ATTENTION
def _body_tokens():
    src, toks, ids = D.BPE_LOWEST
    o = [t(400, 56, '&quot;%s&quot; %s %d letters, %d bytes' % (src, E_MID, len(src), len(src.encode())), 18, INK, "middle")]
    x = 225
    for i, (tk, tid) in enumerate(zip(toks, ids)):
        sw = 3 if i % 2 == 0 else 2                       # alternating stroke weight
        o.append(rect(x, 96, 110, 64, 8, DATA_F, DATA_S, sw))
        o.append(t(x + 55, 128, tk, 24, INK, "middle", mono=True, central=True))
        o.append(t(x + 55, 184, str(tid), 14, MUT, "middle", mono=True))
        x += 120
    o.append(t(400, 232, "%d tokens %s ids %s" % (len(toks), E_MID, ", ".join(str(i) for i in ids)), 14, MUT, "middle"))
    return J(o)


M("motif-token-stream", "Text cut into subword tokens, each with an id",
  "The word lowest, six letters, cut into three tokens: low, e and st, with ids 257, 101 and 260. "
  "Neighbouring boxes alternate stroke weight.",
  "0 0 800 260", _body_tokens(),
  "Mono token text so whitespace and byte boundaries are visible. Print the token count and the source "
  "text. Ids from the Week 20 merge table.")


def _body_bpe():
    a, b, ab, cnt = D.BPE_MERGE1
    o = [t(400, 40, "Merge step 1: the most common neighbouring pair becomes one token", 18, INK, "middle")]
    o.append(rect(150, 130, 90, 90, 10, DATA_F, ACC_S, 4))
    o.append(rect(250, 130, 90, 90, 10, DATA_F, ACC_S, 4))
    o.append(t(195, 175, a, 24, INK, "middle", mono=True, central=True))
    o.append(t(295, 175, b, 24, INK, "middle", mono=True, central=True))
    o.append(t(195, 242, "108", 14, MUT, "middle", mono=True))
    o.append(t(295, 242, "111", 14, MUT, "middle", mono=True))
    o.append(bracket(150, 340, 118, 12, ACC_S))
    o.append(t(245, 96, "pair seen %d times" % cnt, 14, ACC_S, "middle"))
    o.append(arrow(380, 175, 470, 175, INK, 3))
    o.append(rect(520, 130, 130, 90, 10, MODEL_F, MODEL_S, 3))
    o.append(t(585, 175, ab, 24, INK, "middle", mono=True, central=True))
    o.append(t(585, 242, "256", 14, MUT, "middle", mono=True))
    o.append(t(400, 320, "5 in low + 2 in lower = 7. Two tokens become one, so a text gets shorter by 7 symbols.",
               14, MUT, "middle"))
    o.append(t(400, 345, "The new token is the model's: it is added to the vocabulary as id 256.", 14, MUT, "middle"))
    return J(o)


M("motif-bpe-merge", "One merge: the commonest pair of tokens becomes a single new token",
  "The pair l and o, ids 108 and 111, seen 7 times (5 in low, 2 in lower), is replaced by one new token lo "
  "with id 256.",
  "0 0 800 400", _body_bpe(),
  "Week 20. Pair = accent, new token = model. Print the pair count.")


def _att_cells(x0, y0, cw, ch, W, toks, size=14, fmt="%.4f"):
    o = []
    for i, row in enumerate(W):
        m = max(row)
        for j, v in enumerate(row):
            fill, stroke, sw = cell_tint(v, m)
            o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, fill, stroke, sw))
    for i, row in enumerate(W):                      # redraw rings last so neighbours do not hide them
        m = max(row)
        for j, v in enumerate(row):
            if abs(v - m) < 1e-9:
                o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, "none", ACC_S, 3))
    for i, row in enumerate(W):
        for j, v in enumerate(row):
            o.append(t(x0 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, fmt % v, size, INK, "middle", mono=True, central=True))
    return o


def _legend_cells(x, y):
    o = [sq(x, y, 22, 22, ACC_F, ACC_S, 3), t(x + 30, y + 11, "largest in its row", 12, MUT, central=True),
         sq(x + 180, y, 22, 22, DATA_F, GRID, 2), t(x + 210, y + 11, "0.10 or more", 12, MUT, central=True),
         sq(x + 330, y, 22, 22, PANEL, GRID, 2), t(x + 360, y + 11, "below 0.10", 12, MUT, central=True)]
    return o


def _body_att_grid():
    toks, W = D.ATT_TOKENS, D.ATT_W
    x0, y0, cw, ch = 130, 150, 82, 82
    o = [t(x0 + 1.5 * cw, 70, "key (being looked at)", 14, MUT, "middle")]
    for j, tk in enumerate(toks):
        o.append(t(x0 + j * cw + cw / 2.0, 138, tk, 14, INK, "middle", mono=True))
    for i, tk in enumerate(toks):
        o.append(t(x0 - 10, y0 + i * ch + ch / 2.0, tk, 14, INK, "end", mono=True, central=True))
    o.append(trot(30, y0 + 1.5 * ch, "query (asking)", 14))
    o += _att_cells(x0, y0, cw, ch, W, toks)
    for i, row in enumerate(W):
        o.append(t(x0 + 3 * cw + 14, y0 + i * ch + ch / 2.0, "sum %.2f" % sum(row), 12, MUT, central=True))
    o.append(shape_chip(x0 + 3 * cw + 14, 112, "(3, 3)"))
    o += _legend_cells(30, 420)
    o.append(t(250, 475, "Week 14 hand pass %s every row adds to 1" % E_MID, 12, MUT, "middle"))
    return J(o)


M("motif-attention-grid", "Each word's row of attention weights adds to 1",
  "A 3 by 3 grid of attention weights for the words the, cat, sat. Rows are the query, columns are the key. "
  "Row the: 0.4223, 0.1554, 0.4223. Row cat: 0.1554, 0.4223, 0.4223. Row sat: 0.2119, 0.2119, 0.5761. "
  "The largest weight in each row is ringed; every row sums to 1.",
  "0 0 500 500", _body_att_grid(),
  "Heatmap rules (STYLE 2.9): three discrete tints, every cell prints its number, axes named query / key. "
  "Largest-in-row (ties both ringed) is accent; the legend states the cut-offs.")


def _body_causal():
    toks, W = D.ATT_TOKENS, D.MASK_W
    x0, y0, cw, ch = 130, 150, 82, 82
    o = [t(x0 + 1.5 * cw, 70, "key (being looked at)", 14, MUT, "middle")]
    for j, tk in enumerate(toks):
        o.append(t(x0 + j * cw + cw / 2.0, 138, tk, 14, INK, "middle", mono=True))
    for i, tk in enumerate(toks):
        o.append(t(x0 - 10, y0 + i * ch + ch / 2.0, tk, 14, INK, "end", mono=True, central=True))
    o.append(trot(30, y0 + 1.5 * ch, "query (asking)", 14))
    for i, row in enumerate(W):
        m = max(row)
        for j, v in enumerate(row):
            if j > i:
                o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, PANEL, GRID, 2))
                o.append(line(x0 + j * cw + 8, y0 + i * ch + 8, x0 + j * cw + cw - 8, y0 + i * ch + ch - 8, GRID, 2))
                o.append(t(x0 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0 + 24, E_MINUS + E_INF, 12, MUT, "middle"))
            else:
                fill, stroke, sw = cell_tint(v, m)
                o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, fill, stroke, sw))
                o.append(t(x0 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, "%.4f" % v, 14, INK, "middle", mono=True, central=True))
    for i, row in enumerate(W):
        o.append(t(x0 + 3 * cw + 14, y0 + i * ch + ch / 2.0, "sum %.2f" % sum(row), 12, MUT, central=True))
    o += _legend_cells(30, 420)
    o.append(t(250, 475, "later words struck out: score %s%s before the softmax, so weight 0" % (E_MINUS, E_INF), 12, MUT, "middle"))
    return J(o)


M("motif-causal-mask", "A word may only read itself and earlier words",
  "The same 3 by 3 grid with the cells above the diagonal struck through and marked minus infinity. "
  "Row the: 1, 0, 0. Row cat: 0.3302, 0.6698, 0. Row sat: 0.2483, 0.2483, 0.5035. Rows still sum to 1.",
  "0 0 500 500", _body_causal(),
  "Week 15 (teacher-only box numbers: divide by the square root of 2 and mask). Masked cells are grid "
  "with a diagonal strike and the words minus infinity; the mask is applied before the softmax.")


def _body_arcs():
    toks, W = D.ATT_TOKENS, D.ATT_W[2]
    cx = [160, 400, 640]
    o = []
    o.append(t(400, 40, "Query: sat reads the, cat and itself", 18, INK, "middle"))
    def band(v):
        return 6 if v >= 0.5 else (3 if v >= 0.1 else 1.5)
    o.append(path("M%d 270 Q 400 70 %d 270" % (cx[2], cx[0]), "none", DATA_S, band(W[0])))
    o.append(path("M%d 270 Q 520 140 %d 270" % (cx[2], cx[1]), "none", DATA_S, band(W[1])))
    o.append(path("M%d 270 C %d 160 %d 160 %d 270" % (cx[2] - 24, cx[2] - 70, cx[2] + 70, cx[2] + 24), "none", ACC_S, band(W[2])))
    o.append(rect(cx[0] - 60, 280, 120, 54, 10, DATA_F, DATA_S, 3))
    o.append(rect(cx[1] - 60, 280, 120, 54, 10, DATA_F, DATA_S, 3))
    o.append(rect(cx[2] - 60, 280, 120, 54, 10, ACC_F, ACC_S, 4))
    for c, tk in zip(cx, toks):
        o.append(t(c, 307, tk, 24, INK, "middle", mono=True, central=True))
    o.append(t(400, 122, "%.4f" % W[0], 14, INK, "middle", mono=True))
    o.append(t(540, 188, "%.4f" % W[1], 14, INK, "middle", mono=True))
    o.append(t(640, 156, "%.4f" % W[2], 14, ACC_S, "middle", mono=True))
    o.append(t(400, 365, "arc width = weight band: 0.50 or more thick, 0.10 to 0.49 medium %s 3 tokens" % E_MID, 12, MUT, "middle"))
    return J(o)


M("motif-attention-arcs", "The word sat spends most of its attention on itself",
  "Three tokens on a line. Arcs run from the current token sat, outlined in accent, to the, cat and itself. "
  "The weights are 0.2119 to the, 0.2119 to cat and 0.5761 to itself; the 0.5761 arc is the thickest.",
  "0 0 800 400", _body_arcs(),
  "Week 14 row sat. Current token = accent with a thick ring; arc width = weight band (three widths); "
  "print the weight on each arc.")


def _body_compound():
    xm = lambda i: 80 + i * 74
    ym = lambda v: 400 - 320 * v
    o = [line(70, 80, 70, 400, INK, 2), line(70, 400, 440, 400, INK, 2),
         line(70, ym(1), 440, ym(1), GRID, 1.5, cap=False)]
    o.append(t(62, ym(1), "1", 12, MUT, "end", central=True))
    o.append(t(62, ym(0), "0", 12, MUT, "end", central=True))
    for i, (T, v) in enumerate(zip(D.COMPOUND_T, D.COMPOUND_VALS)):
        last = i == len(D.COMPOUND_T) - 1
        o.append(sq(xm(i), ym(v), 54, 400 - ym(v), ACC_F if last else DATA_F, ACC_S if last else DATA_S, 3 if last else 2))
        o.append(t(xm(i) + 27, ym(v) - 8, "%.3f" % v, 14 if last else 12, ACC_S if last else INK, "middle"))
        o.append(t(xm(i) + 27, 420, "T = %d" % T, 12, MUT, "middle"))
    o.append(t(250, 455, "0.9526 multiplied by itself T times: 40 times leaves 0.143", 14, MUT, "middle"))
    o.append(t(250, 478, "The same slope used again and again; below 1 it fades.", 12, MUT, "middle"))
    return J(o)


M("motif-gradient-compound", "A number below 1, multiplied by itself, fades to almost nothing",
  "Five bars for T = 1, 10, 20, 30 and 40: 0.953, 0.615, 0.379, 0.233 and 0.143. The T = 40 bar is "
  "highlighted in accent.",
  "0 0 500 500", _body_compound(),
  "Week 10 hand calculation: 0.9526 to the power T. Print the base, T and the result (0.143 at T = 40).")


def _body_block():
    o = []
    sx = 90                                                       # the residual stream
    o.append(line(sx, 56, sx, 640, OK_S, 4))
    o.append(head(sx, 650, 90, OK_S, 4))
    o.append(shape_chip(sx + 16, 40, "(64, 128)", OK_S))
    o.append(shape_chip(sx + 16, 618, "(64, 128)", OK_S))
    o.append(trot(52, 340, "residual stream", 12, OK_S))
    # branch 1
    o.append(line(sx, 128, 190, 128, OK_S, 3))
    o.append(rect(190, 100, 200, 56, 10, MODEL_F, MODEL_S, 3))
    o.append(t(290, 128, "LayerNorm", 18, INK, "middle", central=True))
    o.append(arrow(290, 156, 290, 200, INK, 3))
    o.append(rect(190, 200, 200, 90, 10, MODEL_F, MODEL_S, 3))
    o.append(t(290, 236, "attention", 18, INK, "middle", central=True))
    o.append(t(290, 264, "4 heads", 12, MUT, "middle", central=True))
    o.append(path("M290 290 V335 H%d" % (sx + 18), "none", INK, 3))
    o.append(head(sx + 18, 335, 180, INK, 3))
    o.append(circ(sx, 335, 17, PAPER, OK_S, 3))
    o.append(t(sx, 335, "+", 18, INK, "middle", central=True))
    # branch 2
    o.append(line(sx, 395, 190, 395, OK_S, 3))
    o.append(rect(190, 367, 200, 56, 10, MODEL_F, MODEL_S, 3))
    o.append(t(290, 395, "LayerNorm", 18, INK, "middle", central=True))
    o.append(arrow(290, 423, 290, 467, INK, 3))
    o.append(rect(190, 467, 200, 90, 10, MODEL_F, MODEL_S, 3))
    o.append(t(290, 503, "MLP", 18, INK, "middle", central=True))
    o.append(t(290, 531, "4 times wider inside", 12, MUT, "middle", central=True))
    o.append(path("M290 557 V602 H%d" % (sx + 18), "none", INK, 3))
    o.append(head(sx + 18, 602, 180, INK, 3))
    o.append(circ(sx, 602, 17, PAPER, OK_S, 3))
    o.append(t(sx, 602, "+", 18, INK, "middle", central=True))
    o.append(t(250, 672, "One block of the course's TinyGPT; four blocks stacked.", 12, MUT, "middle"))
    o.append(t(250, 690, "807,196 parameters in the whole model (ledger run).", 12, MUT, "middle"))
    return J(o)


M("motif-block-stack", "A transformer block: two sub-layers, each added back onto the residual stream",
  "A tall diagram. A green residual stream runs straight down the left, carrying a (64, 128) table. "
  "It branches into LayerNorm then attention (4 heads) and the result is added back at a plus circle; "
  "then LayerNorm then an MLP four times wider inside, added back again.",
  "0 0 500 700", _body_block(),
  "Residual path = correct stroke with a bypass; blocks = model. Shape (T, d) = (64, 128) for the ledger "
  "TinyGPT. Print a parameter count only if the week counts it.")


def _body_tensor2d():
    V = D.ATT_V
    o = [t(250, 56, "V: one row of values per token", 18, INK, "middle")]
    x0, y0, cw, ch = 175, 100, 70, 56
    for i, row in enumerate(V):
        o.append(t(x0 - 12, y0 + i * ch + ch / 2.0, D.ATT_TOKENS[i], 14, INK, "end", mono=True, central=True))
        for j, v in enumerate(row):
            o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, DATA_F, DATA_S, 2))
            o.append(t(x0 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, "%.1f" % v, 14, INK, "middle", mono=True, central=True))
    o.append(rect(x0, y0, 2 * cw, 3 * ch, 0, "none", DATA_S, 3))
    o.append(shape_chip(x0 + 2 * cw + 18, y0 + 71, "(3, 2)"))
    o.append(t(250, 330, "3 tokens (rows) %s 2 numbers each (columns)" % E_MID, 14, MUT, "middle"))
    return J(o)


M("motif-tensor-2d", "A 2-D tensor: a row per token, its shape stated",
  "A grid of 3 rows and 2 columns holding the Week 14 values: the 0.0 1.0, cat 1.0 0.0, sat 1.0 1.0, "
  "labelled with the shape (3, 2).",
  "0 0 500 360", _body_tensor2d(),
  "Every tensor carries a mono shape chip with the week's real numbers (STYLE 2.2). Rows = tokens.")


# ------------------------------------------------------------------ RETRIEVAL, AGENTS, SYSTEMS
def _body_cos():
    A, B, C = D.COS_A, D.COS_B, D.COS_C
    o = []
    names = ["A", "B", "C"]
    for i, (n, v) in enumerate(zip(names, (A, B, C))):
        y = 90 + i * 64
        o.append(t(52, y + 24, n, 18, INK, "middle", central=True))
        for j, x in enumerate(v):
            o.append(sq(72 + j * 46, y, 46, 48, DATA_F, DATA_S, 2))
            o.append(t(72 + j * 46 + 23, y + 24, str(x), 14, INK, "middle", mono=True, central=True))
        o.append(shape_chip(224, y + 11, "(3,)"))
    o.append(t(180, 66, "three vectors", 14, MUT, "middle"))
    o.append(t(560, 66, "cosine of every pair", 14, MUT, "middle"))
    x0, y0, cw, ch = 440, 100, 80, 56
    for j, n in enumerate(names):
        o.append(t(x0 + j * cw + cw / 2.0, 92, n, 14, INK, "middle"))
        o.append(t(x0 - 12, y0 + j * ch + ch / 2.0, n, 14, INK, "end", central=True))
    for i, row in enumerate(D.COS_TABLE):
        m = max(row)
        for j, v in enumerate(row):
            fill, stroke, sw = cell_tint(v, m)
            o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, fill, stroke, sw))
    for i, row in enumerate(D.COS_TABLE):
        m = max(row)
        for j, v in enumerate(row):
            if abs(v - m) < 1e-9:
                o.append(sq(x0 + j * cw, y0 + i * ch, cw, ch, "none", ACC_S, 3))
            o.append(t(x0 + j * cw + cw / 2.0, y0 + i * ch + ch / 2.0, "%.3f" % v, 14, INK, "middle", mono=True, central=True))
    o.append(t(400, 300, "A %s C = 1%s4 + 0%s2 + 3%s0 = 4     length of A = 3.162     length of C = 4.472" % (E_MID, E_TIMES, E_TIMES, E_TIMES), 14, INK, "middle"))
    o.append(t(400, 324, "cosine = 4 %s (3.162 %s 4.472) = 4 %s 14.142 = 0.283" % (E_DIV, E_TIMES, E_DIV), 14, INK, "middle"))
    o.append(t(400, 356, "B is A doubled, so it points the same way: cosine 1.000. Length cancels.", 12, MUT, "middle"))
    return J(o)


M("motif-cosine-table", "Cosine compares direction, not length",
  "Three 3-number vectors A (1, 0, 3), B (2, 0, 6) and C (4, 2, 0) and a 3 by 3 table of cosines: A with B is "
  "1.000 because B is A doubled; A with C and B with C are 0.283. The sum for A with C is worked out: "
  "the dot product 4 divided by 3.162 times 4.472 gives 0.283.",
  "0 0 800 400", _body_cos(),
  "Week 25 hand calculation. Print the dot product in full for one pair, and the ranked or tabulated "
  "scores. Ties for the row maximum are all ringed.")


def _flow_box(x, y, w, h, fill, stroke, lines, sw=3, dash=None):
    o = [rect(x, y, w, h, 10, fill, stroke, sw, dash)]
    n = len(lines)
    for i, (s, size, col) in enumerate(lines):
        o.append(t(x + w / 2.0, y + h / 2.0 + (i - (n - 1) / 2.0) * 20, s, size, col, "middle", central=True))
    return o


def _body_rag():
    o = []
    xs = [20, 179, 338, 497, 656]
    for i in range(4):
        o.append(arrow(xs[i] + 124 + 3, 200, xs[i + 1] - 4, 200, INK, 3))
    o += _flow_box(xs[0], 150, 124, 100, HUMAN_F, HUMAN_S, [("question", 18, INK), ("you wrote", 12, INK), ("it first", 12, INK)])
    o += _flow_box(xs[1], 150, 124, 100, DATA_F, DATA_S, [("retrieve", 18, INK), ("15 chunks", 12, INK), ("top k = 2", 12, INK)])
    o += _flow_box(xs[2], 150, 124, 100, DATA_F, DATA_S, [("sources", 18, INK), ("numbered", 12, INK), ("[14] &#8230;", 12, INK)])
    o += _flow_box(xs[3], 150, 124, 100, PANEL, MODEL_S, [("answer", 18, INK), ("cites [14]", 12, INK)], 2, "6 4")
    o += _flow_box(xs[4], 150, 124, 100, OK_F, OK_S, [("verify", 18, INK), ("14 was served", 12, INK), ("pass", 12, INK)])
    for i, x in enumerate(xs):
        o.append(ring_num(x + 18, 150, i + 1))
    o.append(chip(xs[3] + 62 - 86, 262, 172, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))
    o.append(tick(xs[4] + 62, 270, 10, OK_S))
    o.append(t(400, 90, "Chunk, embed, retrieve, number the sources, demand the id back, check it", 18, INK, "middle"))
    o.append(t(400, 340, "The check proves the cited note was served. It does not prove the answer is right.", 14, MUT, "middle"))
    o.append(t(400, 364, "Worked task from Week 28: one extraction call, note 14, 15-note index.", 12, MUT, "middle"))
    return J(o)


M("motif-rag-flow", "Retrieval-augmented answer: retrieve, number, cite, verify",
  "Five numbered stages left to right: the question you wrote; retrieve the top 2 of 15 chunks; "
  "number the sources, the first being [14]; a scripted answer that cites [14], drawn dashed and labelled "
  "stand-in, not a model; and a verify step that passes because note 14 was served.",
  "0 0 800 400", _body_rag(),
  "Question = human; chunks = data; the scripted writer = dashed stand-in; the verifier = correct/wrong. "
  "Print the retrieved ids and k.")


def _body_recall():
    ks, lit, strg, n = D.RECALL_K, D.RECALL_LITERAL, D.RECALL_STRANGER, D.RECALL_N
    ym = lambda v: 400 - 28 * v
    o = [line(70, 100, 70, 400, INK, 2), line(70, 400, 460, 400, INK, 2)]
    for v in (0, 5, 10):
        o.append(line(70, ym(v), 460, ym(v), GRID, 1.5, cap=False))
        o.append(t(62, ym(v), str(v), 12, MUT, "end", central=True))
    o.append(trot(24, 250, "right note found (of 10 questions)", 12))
    for i, k in enumerate(ks):
        gx = 100 + i * 124
        o.append(sq(gx, ym(lit[i]), 48, 400 - ym(lit[i]), DATA_F, DATA_S, 3))
        o.append(sq(gx + 52, ym(strg[i]), 48, 400 - ym(strg[i]), HUMAN_F, HUMAN_S, 3))
        o.append(t(gx + 24, ym(lit[i]) - 8, "%d / %d" % (lit[i], n), 12, INK, "middle"))
        o.append(t(gx + 76, ym(strg[i]) - 8, "%d / %d" % (strg[i], n), 12, INK, "middle"))
        o.append(t(gx + 50, 420, "k = %d" % k, 12, MUT, "middle"))
    o.append(sq(120, 62, 18, 18, DATA_F, DATA_S, 3))
    o.append(t(146, 71, "my own words", 12, INK, central=True))
    o.append(sq(270, 62, 18, 18, HUMAN_F, HUMAN_S, 3))
    o.append(t(296, 71, "a stranger's words", 12, INK, central=True))
    o.append(t(265, 452, "Same ten facts, same index.", 12, MUT, "middle"))
    o.append(t(265, 470, "Questions in the notes' own words are an upper bound.", 12, MUT, "middle"))
    return J(o)


M("motif-recall-at-k", "Recall@k drops when a stranger writes the questions",
  "Grouped bars at k = 1, 3 and 5. Questions in the writer's own words: 10 of 10 at every k. The same ten "
  "facts in a stranger's words: 2 of 10, 5 of 10 and 6 of 10.",
  "0 0 500 500", _body_recall(),
  "Week 26. Always print hits over questions (k / n), never a bare percentage. Two bars per group differ "
  "by role colour AND by position and label.")


def _body_agent():
    o = [stand_in_frame(20, 64, 760, 140, label_y=50)]
    stages = [(40, "perceive"), (190, "decide"), (340, "act"), (490, "observe")]
    for i in range(3):
        o.append(arrow(stages[i][0] + 120 + 4, 130, stages[i + 1][0] - 4, 130, INK, 3))
    o.append(arrow(610 + 4, 130, 656, 130, INK, 3))
    o.append(path("M550 160 V188 H100 V162", "none", INK, 3))
    o.append(head(100, 160, -90, INK, 3))
    for i, (x, nm) in enumerate(stages):
        cur = nm == "act"
        o.append(rect(x, 100, 120, 60, 10, ACC_F if cur else PAPER, ACC_S if cur else INK, 4 if cur else 3))
        o.append(t(x + 60, 130, nm, 18, INK, "middle", central=True))
    o.append(rect(660, 100, 110, 60, 10, PAPER, INK, 3))
    o.append(t(715, 130, "stop", 18, INK, "middle", central=True))
    o.append(t(325, 200, "repeat until the model answers or a fence stops it", 12, MUT, "middle"))
    # trace strip: the real Week 28 five turns
    cum = 0
    for i, (it, tin, tout, cost, tool, res) in enumerate(D.TRACE):
        cum += tin
        x = 20 + i * 154
        cur = it == 4
        bad = res == "ERR"
        stroke = ACC_S if cur else (BAD_S if bad else GRID)
        fill = ACC_F if cur else (BAD_F if bad else PAPER)
        o.append(rect(x, 232, 144, 62, 8, fill, stroke, 3 if (cur or bad) else 2))
        o.append(t(x + 72, 252, "turn %d %s in %d" % (it, E_MID, tin), 12, INK, "middle", weight="600" if cur else None))
        o.append(t(x + 72, 274, "%s %s" % (tool, res), 12, INK, "middle", mono=True, weight="600" if cur else None))
        if bad:
            o.append(cross(x + 128, 244, 5))
    o.append(t(400, 320, "stop: end_turn %s 5 iterations %s spend $%.6f %s input tokens added up: %d" %
               (E_MID, E_MID, D.TRACE_SPEND, E_MID, cum), 12, MUT, "middle"))
    return J(o)


M("motif-agent-loop", "An agent is a loop: perceive, decide, act, observe, stop",
  "A cycle of four boxes, perceive, decide, act, observe, with a return arrow and a stop box. The loop is "
  "dashed and labelled stand-in, not a model. Beneath it, the five real turns of the Week 28 run: turn 3 "
  "write_file failed with an error, turn 4 write_file succeeded and is highlighted. Spend is $0.002705.",
  "0 0 800 340", _body_agent(),
  "Week 28/29. Current step = accent; error turn = wrong stroke with a cross. Print the step index and "
  "token counts. The scripted plan is a stand-in (STYLE 2.5).")


def _body_cost():
    ins = [r[1] for r in D.TRACE]
    ym = lambda v: 400 - 0.45 * v
    o = [line(70, 100, 70, 400, INK, 2), line(70, 400, 460, 400, INK, 2)]
    for v in (0, 200, 400, 600):
        o.append(line(70, ym(v), 460, ym(v), GRID, 1.5, cap=False))
        o.append(t(62, ym(v), str(v), 12, MUT, "end", central=True))
    o.append(trot(24, 250, "input tokens sent that turn", 12))
    for i, v in enumerate(ins):
        x = 92 + i * 74
        o.append(sq(x, ym(v), 56, 400 - ym(v), DATA_F, DATA_S, 2))
        o.append(t(x + 28, ym(v) - 8, str(v), 12, INK, "middle"))
        o.append(t(x + 28, 420, "turn %d" % (i + 1), 12, MUT, "middle"))
    o.append(chip(250, 52, 200, "all five: %s input tokens" % "{:,}".format(sum(ins)), ACC_S, ACC_F, 12, 28, mono=False))
    o.append(t(250, 450, "Every turn re-sends the history, so each bar is taller than the last.", 12, MUT, "middle"))
    o.append(t(250, 470, "1 + 2 + %s + 10 = 10 %s 11 %s 2 = %d" % (E_ELL, E_TIMES, E_DIV, D.TRI_SUM), 14, INK, "middle"))
    return J(o)


M("motif-cost-growth", "Tokens re-sent each turn make every turn dearer than the last",
  "Five bars of input tokens per turn from the Week 28 run: 247, 415, 448, 519 and 566, rising each turn. "
  "The five add up to 2,195 input tokens. The triangular sum 1 + 2 + ... + 10 equals 10 times 11 divided "
  "by 2, which is 55.",
  "0 0 500 500", _body_cost(),
  "Weeks 28-29. Print per-step and cumulative tokens and the triangular sum evaluated for one k. "
  "(The runs are of a scripted stand-in; say 'of the stand-in' in the caption.)")


def _body_fence():
    o = []
    o.append(rect(30, 40, 190, 70, 10, PANEL, MODEL_S, 2, "6 4"))
    o.append(t(125, 68, "tool call", 18, INK, "middle", central=True))
    o.append(t(125, 90, "outside the sandbox", 12, MUT, "middle", central=True))
    o.append(chip(34, 118, 182, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))
    o.append(arrow(224, 75, 378, 75, INK, 3))
    o.append(rect(386, 30, 14, 100, 4, INK, INK, 2))
    o.append(t(393, 150, "fence", 14, INK, "middle"))
    o.append(path("M408 75 H470", "none", BAD_S, 3, "6 4"))
    o.append(rect(480, 40, 290, 70, 10, BAD_F, BAD_S, 3))
    o.append(cross(512, 75, 10))
    o.append(t(540, 62, "blocked: PermissionError", 14, INK, "start", central=True))
    o.append(t(540, 88, "the model asked; the code said no", 12, INK, "start", central=True))
    o.append(rect(30, 178, 190, 50, 10, PANEL, MODEL_S, 2, "6 4"))
    o.append(t(125, 203, "tool call inside it", 14, INK, "middle", central=True))
    o.append(arrow(224, 203, 378, 203, INK, 3))
    o.append(path("M408 203 H470", "none", OK_S, 3))
    o.append(rect(480, 178, 290, 50, 10, OK_F, OK_S, 3))
    o.append(tick(512, 203, 10))
    o.append(t(540, 203, "allowed through, then acted on", 14, INK, "start", central=True))
    return J(o)


M("motif-fence", "A guardrail in code lets one call through and blocks the other",
  "Two tool calls from a scripted stand-in reach a fence. The call outside the sandbox is blocked with a "
  "PermissionError and a cross; the call inside it is allowed through with a tick.",
  "0 0 800 260", _body_fence(),
  "Week 28. Pass = correct + tick; block = wrong + cross; print the rule that fired. The fence is "
  "plain Python and works with the model unplugged.")


def _body_trace():
    o = [stand_in_frame(20, 40, 460, 580, label_y=22)]
    cum = 0
    obs = ["[note 14] (similarity 0.322) 2026-08-14 - Cost accounting", "0.36",
           "ValueError: directory 'reports' does not exist",
           "wrote 47 bytes to extraction-250.md",
           "One extraction call costs about $0.00144 [note 14]."]
    act = ["search_notes  ok", "calculate  ok", "write_file  ERR", "write_file  ok", "(answer)  stop"]
    for i, (it, tin, tout, cost, tool, res) in enumerate(D.TRACE):
        cum += tin
        y = 62 + i * 108
        cur = it == 4
        bad = res == "ERR"
        stroke = ACC_S if cur else (BAD_S if bad else GRID)
        fill = ACC_F if cur else (BAD_F if bad else PAPER)
        o.append(rect(34, y, 432, 96, 10, fill, stroke, 3 if (cur or bad) else 2))
        o.append(ring_num(60, y + 24, it))
        o.append(t(82, y + 29, "turn %d %s in %d, out %d %s so far %s in" % (it, E_MID, tin, tout, E_MID, "{:,}".format(cum)), 14, INK,
                   weight="600" if cur else None))
        o.append(t(50, y + 56, act[i], 12, INK, mono=True, weight="600" if cur else None))
        o.append(t(50, y + 80, obs[i], 12, INK, mono=True, weight="600" if cur else None))
        if bad:
            o.append(cross(444, y + 24, 6))
        elif res == "ok":
            o.append(tick(444, y + 24, 8))
    o.append(t(250, 612, "stop: end_turn %s 5 iterations %s spend $%.6f" % (E_MID, E_MID, D.TRACE_SPEND), 12, MUT, "middle"))
    return J(o)


M("motif-trace", "An agent trace, one row per turn, with the running token count",
  "Five rows, one per turn of the Week 28 run, inside a dashed stand-in frame. Each row shows tokens in and "
  "out and the input tokens so far (247, 662, 1,110, 1,629, 2,195), the tool called and what it returned. "
  "Turn 3, write_file, failed and is marked with a cross; turn 4 is highlighted as the current step.",
  "0 0 500 640", _body_trace(),
  "Section 1.9 exception: five lines of real trace text, in mono, with annotation only. Current row = "
  "accent + weight 600; error row = wrong + cross. Print every observation and the running token count.")


def _body_evaltable():
    cols = [(60, "start", "category"), (310, "middle", "n"), (440, "middle", "before"), (580, "middle", "after"), (700, "middle", "change")]
    o = []
    for x, a, s in cols:
        o.append(t(x, 52, s, 14, INK, a, weight="600"))
    o.append(line(40, 66, 760, 66, INK, 2))
    rows = [("all (average)", 30, 18, 19)] + [(c, n, b, a) for c, n, b, a in D.LORA_TABLE]
    for i, (c, n, b, a) in enumerate(rows):
        y = 78 + i * 72
        bad = (a / n - b / n) < 0
        avg = i == 0
        o.append(rect(40, y, 720, 60, 8, BAD_F if bad else (PANEL if avg else PAPER), BAD_S if bad else GRID, 3 if bad else 2))
        yc = y + 30
        o.append(t(60, yc, c, 18, INK, "start", central=True))
        o.append(t(310, yc, str(n), 14, INK, "middle", central=True))
        o.append(t(440, yc, "%d / %d = %.3f" % (b, n, b / n), 14, INK, "middle", central=True))
        o.append(t(580, yc, "%d / %d = %.3f" % (a, n, a / n), 14, INK, "middle", central=True))
        d = a / n - b / n
        o.append(t(700, yc, ("+%.3f" % d) if d >= 0 else (E_MINUS + "%.3f" % -d), 14, INK, "middle", central=True))
        if bad:
            o.append(cross(738, yc, 8))
    o.append(t(400, 316, "The average went up. One category went down: a sum can hide a subtraction.", 14, MUT, "middle"))
    o.append(t(400, 340, "Billing's drop is one ticket out of n = 5. Three other categories are not shown.", 12, MUT, "middle"))
    return J(o)


M("motif-eval-table", "The average rose while one category fell",
  "A table of before and after scores out of n. All: 18 of 30 (0.600) rises to 19 of 30 (0.633), +0.033. "
  "Technical: 2 of 7 (0.286) to 4 of 7 (0.571), +0.286. Billing: 2 of 5 (0.400) to 1 of 5 (0.200), "
  "minus 0.200, highlighted as the regression with a cross.",
  "0 0 800 400", _body_evaltable(),
  "Week 31 (base model vs LoRA). Print k / n for each category. The row that fell is wrong + cross icon "
  "(icon, not colour alone). Header cells may use weight 600 (STYLE 1.7).")


def _body_ablate():
    cols = [(60, "start", "variant"), (390, "middle", "best val loss"), (530, "middle", "at step"), (680, "middle", "final train / val")]
    o = [t(400, 34, "1,500 steps each, seed 1337", 14, MUT, "middle")]
    for x, a, s in cols:
        o.append(t(x, 70, s, 14, INK, a, weight="600"))
    o.append(line(40, 84, 760, 84, INK, 2))
    for i, (nm, best, st, ftr, fva) in enumerate(D.ABLATE):
        y = 96 + i * 70
        bad = best > 2.0
        o.append(rect(40, y, 720, 58, 8, BAD_F if bad else PAPER, BAD_S if bad else GRID, 3 if bad else 2))
        yc = y + 29
        o.append(t(60, yc, nm, 18, INK, "start", central=True))
        o.append(t(390, yc, "%.3f" % best, 14, INK, "middle", central=True))
        o.append(t(530, yc, str(st), 14, INK, "middle", central=True))
        o.append(t(680, yc, "%.3f / %.3f" % (ftr, fva), 14, INK, "middle", central=True))
        if bad:
            o.append(cross(738, yc, 8))
    o.append(t(400, 340, "Take the residual path out and nothing is learned. Taking the scale out did not hurt here.", 14, MUT, "middle"))
    return J(o)


M("motif-ablation-table", "Remove one component at a time and compare the loss",
  "A table of three variants after 1,500 steps. Baseline best validation loss 1.278 at step 750. No "
  "residual: 2.848 at step 850, highlighted as broken with a cross. No scale: 1.245 at step 600.",
  "0 0 800 400", _body_ablate(),
  "Weeks 15-19. Rows that broke are wrong + cross. Print each loss and the step count (STYLE 4: "
  "motif-head-ablation). The surprising row (no scale: not worse) is real and stays.")


def _body_chips():
    o = [t(400, 34, "A scripted backend is drawn dashed and chipped; a measurement is solid; a quotation is dashed grey", 14, MUT, "middle")]
    o.append(stand_in_frame(30, 74, 230, 120, label_y=64 + 0))
    o.append(t(145, 134, "scripted plan", 18, INK, "middle", central=True))
    o.append(t(145, 158, "replays typed steps", 12, MUT, "middle", central=True))
    o.append(rect(290, 74, 230, 120, 12, PAPER, INK, 3))
    o.append(t(405, 108, "measured", 12, MUT, "middle"))
    o.append(t(405, 140, "3,072,000 %s 14,549 = 211" % E_DIV, 14, INK, "middle", central=True))
    o.append(t(405, 164, "characters per knob", 12, INK, "middle", central=True))
    o.append(quoted_box(550, 74, 220, 120, "about 20 tokens per parameter", 12))
    o.append(t(660, 168, "compute-optimal rule, Module 4", 12, MUT, "middle", central=True))
    o.append(t(400, 232, "They never share a box. Characters are not tokens, so 211 and 20 are not compared.", 12, MUT, "middle"))
    return J(o)


M("motif-stand-in-and-quoted", "Stand-in, measured and quoted numbers each look different",
  "Three boxes side by side. A dashed purple frame with the chip stand-in, not a model around a scripted "
  "plan. A solid box with a measured value, 3,072,000 divided by 14,549 equals 211 characters per knob. "
  "A dashed grey box reading quoted: about 20 tokens per parameter, a compute-optimal rule of thumb.",
  "0 0 800 260", _body_chips(),
  "STYLE 2.5 and 2.6 together. Stand-in = dashed model stroke, panel fill, exact chip words. Quoted = "
  "muted text in a dashed grid box prefixed 'quoted:'. Week 21 numbers.")
