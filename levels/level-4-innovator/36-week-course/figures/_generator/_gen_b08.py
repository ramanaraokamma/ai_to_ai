"""Block 8 figures: weeks 22, 23, 24 (two concept figures each).

Every number printed is copied from the same week's student-guide output blocks (seeded runs)
or is a hand sum printed beside it (STYLE.md 2.1). Writes fig-w22-1 ... fig-w24-2 into ../figures.
Called from _gen_build.py via emit_b08(). Deterministic: no randomness at run time.
"""
import os
from _gen_core import *

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # figures/
MINUS = "&#8722;"


def title_t(x, s):
    return t(x, 44, s, 24, INK, "middle")


def doc(vb, title, desc, parts):
    return svg_doc(vb, title, desc, "\n".join("  " + p for p in parts))


def fnum(v, nd=4):
    s = ("%." + str(nd) + "f") % abs(v)
    return (MINUS + s) if v < 0 else s


# ------------------------------------------------------------------ W22-1: SFT loss mask
def w22_1():
    toks = [3, 7, 2, 9, 11, 4, 4, 1, 6]
    surprise = [4.574, 1.972, 2.968, 4.729, 4.111, 4.044, 3.102, 4.907]
    x0, pitch, bw = 60, 76, 70
    P = [title_t(400, "SFT scores only the answer: 4 of 8 guesses count")]
    # bracket labels over the token row
    P.append(t(x0 + 2 * pitch + bw / 2.0, 72, "prompt (5 tokens)", 14, HUMAN_S, "middle"))
    P.append(t(x0 + 6.5 * pitch + bw / 2.0, 72, "answer (4 tokens)", 14, DATA_S, "middle"))
    for k, tk in enumerate(toks):
        x = x0 + k * pitch
        if k < 5:
            P.append(rect(x, 84, bw, 44, 8, HUMAN_F, HUMAN_S, 2))
        else:
            P.append(rect(x, 84, bw, 44, 8, DATA_F, DATA_S, 3))
        P.append(t(x + bw / 2.0, 106, str(tk), 18, INK, "middle", mono=True, central=True))
    P.append(t(x0, 148, "the guess made at each place is for the NEXT token; number = surprise, &#8722;ln(chance)", 12, MUT))
    for i in range(9):
        x = x0 + i * pitch
        if i == 8:
            P.append(rect(x, 158, bw, 70, 8, PAPER, GRID, 2, "6 4"))
            P.append(t(x + bw / 2.0, 186, "no guess:", 12, MUT, "middle"))
            P.append(t(x + bw / 2.0, 202, "nothing next", 12, MUT, "middle"))
            continue
        tgt = toks[i + 1]
        if i < 4:
            P.append(rect(x, 158, bw, 70, 8, PANEL, GRID, 2, "6 4"))
            col = MUT
        else:
            P.append(rect(x, 158, bw, 70, 8, ACC_F, ACC_S, 3))
            col = INK
        P.append(t(x + bw / 2.0, 180, "&#8594; %d" % tgt, 14, col, "middle", mono=True, central=True))
        P.append(t(x + bw / 2.0, 206, "%.3f" % surprise[i], 14, col, "middle", mono=True, central=True))
        if i < 4:
            P.append(t(x + bw / 2.0, 248, MINUS + "100", 14, MUT, "middle", mono=True))
        else:
            P.append(tick(x + bw / 2.0, 244, 8, OK_S))
    P.append(t(x0 + 1.5 * pitch + bw / 2.0, 268, "skipped: the answer is inside the prompt", 12, MUT, "middle"))
    P.append(t(x0 + 5.5 * pitch + bw / 2.0, 268, "counted: scored as SFT", 12, INK, "middle"))
    P.append(shape_chip(x0, 282, "(8, 12)", DATA_S))
    P.append(t(x0 + 66, 296, "model scores: one row of 12 per guess (random numbers, not a model)", 12, MUT))
    P.append(rect(60, 314, 330, 34, 8, PANEL, GRID, 2))
    P.append(t(225, 331, "mean of all 8 guesses = 3.8008", 14, INK, "middle", central=True))
    P.append(rect(410, 314, 330, 34, 8, ACC_F, ACC_S, 3))
    P.append(t(575, 331, "mean of the 4 that count = 4.0407", 14, INK, "middle", central=True))
    P.append(t(400, 372, "Different guesses averaged, so different numbers; with random scores neither says SFT worked.", 14, MUT, "middle"))
    return doc("0 0 800 400", "SFT scores only the answer guesses and blanks the prompt guesses",
               "Nine tokens, five of them prompt and four answer, sit in a row. Under them eight guesses, each made at one place for the next "
               "token. The first four guesses (surprises 4.574, 1.972, 2.968, 4.729) are dashed and marked minus 100 because their right "
               "answers are still inside the prompt. The last four (4.111, 4.044, 3.102, 4.907) count. The mean of all eight is 3.8008 and "
               "the mean of the four that count is 4.0407. Scores are random numbers of shape (8, 12), not a model.", P)


# ------------------------------------------------------------------ W22-2: KL by hand
def w22_2():
    q = [0.25, 0.25, 0.25, 0.25]
    p = [0.50, 0.25, 0.125, 0.125]
    lr = [0.6931, 0.0, -0.6931, -0.6931]
    pr = [0.3466, 0.0, -0.0866, -0.0866]
    cent = [195, 315, 435, 555]
    P = [title_t(400, "KL: how far p moved from q, weighted by p")]
    base, sc = 175, 140
    P.append(line(150, base, 600, base, GRID, 1.5))
    for c, name, qv, pv in zip(cent, "ABCD", q, p):
        P.append(t(c, 78, name, 18, INK, "middle"))
        hq, hp = qv * sc, pv * sc
        P.append(rect(c - 40, base - hq, 36, hq, 2, PANEL, DATA_S, 2, "4 3"))
        P.append(rect(c + 4, base - hp, 36, hp, 2, DATA_F, DATA_S, 3))
        P.append(t(c - 22, base - hq - 6, "%g" % qv, 12, MUT, "middle"))
        P.append(t(c + 22, base - hp - 6, "%g" % pv, 12, INK, "middle"))
    P.append(rect(24, 120, 14, 14, 2, PANEL, DATA_S, 2, "4 3"))
    P.append(t(44, 132, "q: reference", 12, INK))
    P.append(rect(24, 142, 14, 14, 2, DATA_F, DATA_S, 3))
    P.append(t(44, 154, "p1: policy", 12, INK))
    P.append(t(24, 216, "ln(p1/q)", 14, INK))
    P.append(t(24, 266, "p1 &#215; ln(p1/q)", 14, INK))
    for c, v, pv in zip(cent, lr, pr):
        up = "&#9650; " if v > 0 else ("&#9660; " if v < 0 else "")
        P.append(rect(c - 46, 196, 92, 34, 8, PAPER, DATA_S, 2))
        P.append(t(c, 213, (up + ("+" if v > 0 else "") + fnum(v)) if v else "0.0000", 14, INK, "middle", central=True))
        P.append(rect(c - 46, 246, 92, 34, 8, PAPER, DATA_S, 2))
        P.append(t(c, 263, ("+" if pv > 0 else "") + fnum(pv) if pv else "0", 14, INK, "middle", central=True))
    P.append(arrow(604, 263, 628, 263, INK, 2))
    P.append(rect(632, 236, 148, 54, 10, ACC_F, ACC_S, 3))
    P.append(t(706, 256, "sum", 14, INK, "middle", central=True))
    P.append(t(706, 276, "KL = 0.1733", 18, INK, "middle", central=True))
    P.append(t(400, 312, "0.3466 &#8722; 0.0866 &#8722; 0.0866 = 0.1733   (hand sum, matches kl.py)", 14, INK, "middle"))
    P.append(t(400, 338, "p2 = 0.70, 0.10, 0.10, 0.10 moves further: KL(p2 || q) = 0.4458, but KL(q || p2) = 0.4298", 14, INK, "middle"))
    P.append(t(400, 364, "Zero only when p = q. Never negative. Not symmetric, so always say which table comes first.", 14, MUT, "middle"))
    return doc("0 0 800 400", "KL divergence is the log-ratio of each outcome, weighted by the new table's own chances, then added",
               "Four outcomes A to D. The reference q gives each 0.25. The policy p1 gives 0.50, 0.25, 0.125, 0.125. The log-ratios ln(p1/q) are "
               "plus 0.6931, 0.0000, minus 0.6931, minus 0.6931. Weighted by p1 they become plus 0.3466, 0, minus 0.0866, minus 0.0866, which add to KL 0.1733. "
               "A second policy p2 gives KL(p2 to q) 0.4458 while KL(q to p2) is 0.4298, so KL is not symmetric.", P)


# ------------------------------------------------------------------ W23-1: the harness
def w23_1():
    stages = [("frozen", "set", HUMAN_F, HUMAN_S, [("8 cases", False), ("32 boxes", False)]),
              ("versioned", "prompt", HUMAN_F, HUMAN_S, [("v1 v2 v3", False), ("one change", False)]),
              ("call", None, PANEL, MODEL_S, [("FakeClient", True), ("seeded", False)]),
              ("parse", None, DATA_F, DATA_S, [("parse-fail 0", False), ("of 8 replies", False)]),
              ("score", None, DATA_F, DATA_S, [("16 22 30", False), ("of 32 boxes", False)]),
              ("report", None, DATA_F, DATA_S, [("regression", False), ("list", False)])]
    bw, gap, x0, y0, h = 104, 24, 28, 110, 120
    P = [title_t(400, "The harness is a test suite with a prompt in it")]
    cx = [x0 + i * (bw + gap) + bw / 2.0 for i in range(6)]
    for i in range(5):
        P.append(arrow(cx[i] + bw / 2.0 + 2, y0 + h / 2.0, cx[i + 1] - bw / 2.0 - 2, y0 + h / 2.0, INK, 2))
    for i, (l1, l2, fl, st, notes) in enumerate(stages):
        x = cx[i] - bw / 2.0
        dash = "6 4" if i == 2 else None
        P.append(rect(x, y0, bw, h, 10, fl, st, 3 if i != 2 else 2, dash))
        if l2:
            P.append(t(cx[i], y0 + 28, l1, 18, INK, "middle", central=True))
            P.append(t(cx[i], y0 + 50, l2, 18, INK, "middle", central=True))
        else:
            P.append(t(cx[i], y0 + 38, l1, 18, INK, "middle", central=True))
        for j, (s, mono) in enumerate(notes):
            P.append(t(cx[i], y0 + 80 + 20 * j, s, 14 if not mono else 12, INK if j == 0 else MUT, "middle", mono=mono, central=True))
    P.append(chip(cx[2] - 86, 76, 172, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))
    # loop back: report -> versioned prompt
    P.append(path("M%s %s V258 H%s V240" % (f2(cx[5]), y0 + h + 2, f2(cx[1])), "none", INK, 2))
    P.append(head(cx[1], 236, -90, INK, 2))
    P.append(t((cx[1] + cx[5]) / 2.0, 282, "change ONE thing, run the same frozen set again", 14, INK, "middle"))
    P.append(rect(110, 302, 580, 34, 8, PANEL, INK, 2))
    P.append(t(400, 319, "guard around the call: limit $0.0040; the run stopped at call 19 with $0.0042 spent", 14, INK, "middle", central=True))
    P.append(t(400, 366, "All scores are of the stand-in, not a model. Floor to beat: 43.8% (14 of 32).", 14, MUT, "middle"))
    return doc("0 0 800 400", "A prompt is tested like code: frozen cases, a versioned prompt, a call, a parse, a score and a report, inside a spending guard",
               "Six boxes in a row joined by arrows: frozen set (8 cases, 32 boxes), versioned prompt (v1, v2, v3), call (a dashed box labelled stand-in, "
               "not a model), parse (parse-fail 0), score (16, 22 and 30 of 32 boxes), report (a regression list). An arrow runs from report back to the "
               "versioned prompt: change one thing and run again. A guard bar under the row says the run stopped at call 19 with 0.0042 dollars spent against a "
               "limit of 0.0040. The floor is 43.8 percent, 14 of 32 boxes.", P)


# ------------------------------------------------------------------ W23-2: scores against the floor
def w23_2():
    X0, SC = 190, 5.0
    bars = [("floor", "(constant answer)", 43.8, "14 / 32", True),
            ("v1 zero-shot", None, 50.0, "16 / 32", False),
            ("v2 rules", None, 68.8, "22 / 32", False),
            ("v3 few-shot", None, 93.8, "30 / 32", False)]
    P = [title_t(400, "Prompt versions against the floor (stand-in)")]
    for v in (0, 25, 50, 75, 100):
        x = X0 + v * SC
        P.append(line(x, 60, x, 340, GRID, 1.5, "2 4"))
        P.append(t(x, 358, str(v), 12, MUT, "middle"))
    for i, (nm, sub, v, cnt, floor) in enumerate(bars):
        y = 64 + 34 * i
        w = v * SC
        if floor:
            P.append(rect(X0, y, w, 28, 6, PANEL, GRID, 2, "6 4"))
            P.append(t(180, y + 11, nm, 14, INK, "end", central=True))
            P.append(t(180, y + 25, sub, 12, MUT, "end", central=True))
        else:
            P.append(rect(X0, y, w, 28, 6, DATA_F, DATA_S, 3))
            P.append(t(180, y + 14, nm, 14, INK, "end", central=True))
        P.append(t(X0 + w - 8, y + 14, "%.1f%% &#183; %s boxes" % (v, cnt), 14, INK, "end", central=True))
    P.append(t(24, 226, "same prompts, six model seeds: each mark is one seed", 14, INK))
    fx = X0 + 43.8 * SC
    P.append(line(fx, 252, fx, 340, GRID, 2, "6 4"))
    P.append(t(fx + 6, 262, "floor 43.8", 12, MUT))
    seeds = [("v1 zero-shot", [50.0, 43.8, 46.9, 59.4, 40.6, 31.2], "circle", 276),
             ("v2 rules", [68.8, 87.5, 71.9, 68.8, 81.2, 75.0], "square", 302),
             ("v3 few-shot", [93.8], "triangle", 328)]
    for nm, vals, kind, y in seeds:
        P.append(t(180, y, nm, 12, INK, "end", central=True))
        P.append(line(X0, y, X0 + 100 * SC, y, GRID, 1.5))
        for v in sorted(set(vals)):
            P.append(mark(kind, X0 + v * SC, y, 6, DATA_S, DATA_F, 2))
        if len(vals) == 1:
            P.append(t(X0 + 93.8 * SC - 14, y, "all six seeds = 93.8", 12, INK, "end", central=True))
        else:
            P.append(t(X0 + 100 * SC + 6, y, "%.1f&#8211;%.1f" % (min(vals), max(vals)), 12, MUT, central=True))
    P.append(t(X0 + 50 * SC, 376, "field score, % of 32 boxes (higher is better)", 12, MUT, "middle"))
    return doc("0 0 800 400", "A prompt must clear the floor, and one seed is one draw",
               "Horizontal bars of field score out of 32 boxes: the constant-answer floor 43.8 percent (14 of 32), v1 zero-shot 50.0 percent (16 of 32), "
               "v2 rules 68.8 percent (22 of 32), v3 few-shot 93.8 percent (30 of 32). Below, six model seeds per prompt: v1 ranges from 31.2 to 59.4 and "
               "falls below the floor on two seeds (40.6 and 31.2), v2 ranges 68.8 to 87.5, v3 scores 93.8 on all six. All scores are of the stand-in, not of a model.", P)


# ------------------------------------------------------------------ W24-1: in-context accuracy vs ceiling
def w24_1():
    model = [0.176, 0.312, 0.480, 0.638, 0.666, 0.828, 0.998]
    ceil = [0.167, 0.333, 0.500, 0.667, 0.833, 1.000, 1.000]
    X0, XS, Y0, YS = 78, 58, 400, 310
    xs = [X0 + XS * n for n in range(7)]
    P = [title_t(250, "Examples vs the ceiling")]
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        y = Y0 - v * YS
        P.append(line(X0, y, X0 + 6 * XS, y, GRID, 1.5, None if v == 0 else "2 4"))
        P.append(t(X0 - 8, y, "%.2f" % v, 12, MUT, "end", central=True))
    for n in range(7):
        P.append(t(xs[n], 418, str(n), 12, MUT, "middle"))
    P.append(t(X0 + 3 * XS, 438, "worked examples in the prompt, n", 12, MUT, "middle"))
    P.append(trot(32, 245, "accuracy on 500 test prompts"))
    P.append(poly([(xs[n], Y0 - ceil[n] * YS) for n in range(7)], "none", MUT, 2, "6 4"))
    P.append(poly([(xs[n], Y0 - model[n] * YS) for n in range(7)], "none", DATA_S, 3))
    for n in range(7):
        P.append(mark("diamond", xs[n], Y0 - ceil[n] * YS, 5, MUT, PAPER, 2))
    for n in range(7):
        P.append(mark("circle", xs[n], Y0 - model[n] * YS, 6, DATA_S, DATA_F, 3))
    for n in range(6):
        P.append(t(xs[n] + 6, Y0 - model[n] * YS + 22 if n else Y0 - model[n] * YS + 22, "%.3f" % model[n], 12, INK))
    P.append(t(xs[6] - 8, Y0 - model[6] * YS + 24, "0.998", 12, INK, "end"))
    P.append(t(xs[5], 78, "ceiling (dashed)", 12, MUT, "middle"))
    P.append(t(xs[1] + 8, Y0 - model[1] * YS - 66 + 0, "model (solid)", 12, DATA_S))
    P.append(ring_num(xs[4] + 6, Y0 - model[4] * YS + 6 - 30, 4))
    P.append(rect(226, 268, 236, 84, 10, PANEL, ACC_S, 2))
    P.append(ring_num(246, 288, 4))
    P.append(t(264, 292, "n = 4: model 0.666,", 12, INK))
    P.append(t(264, 310, "ceiling 0.833. Key shown:", 12, INK))
    P.append(t(264, 328, "copied right only 0.788.", 12, INK))
    P.append(t(264, 346, "Seed 0; ceiling is (n + 1) &#247; 6.", 12, MUT))
    P.append(t(250, 456, "Nothing can beat the dashed line. At n = 0", 14, MUT, "middle"))
    P.append(t(250, 472, "the model gets 0.176: a coin toss on a new code.", 14, MUT, "middle"))
    return doc("0 0 500 500", "A model can only use the examples as far as the task allows: accuracy tracks the ceiling and falls short at n = 4 and 5",
               "Accuracy on 500 test prompts against the number of worked examples n from 0 to 6, seed 0. The dashed ceiling (n plus 1) over 6 reads 0.167, 0.333, "
               "0.500, 0.667, 0.833, 1.000, 1.000. The model reads 0.176, 0.312, 0.480, 0.638, 0.666, 0.828, 0.998: within 0.03 of the ceiling for n 0 to 3, below it "
               "at n 4 and 5 where copying a shown key is right only 0.788 and 0.854 of the time.", P)


# ------------------------------------------------------------------ W24-2: the mask fixes shape, not content
def w24_2():
    panels = [("names seen in training", 40, [("parses as JSON", 90, 100), ("every field right", 79, 95)]),
              ("new names, never seen", 420, [("parses as JSON", 85, 100), ("every field right", 25, 26)])]
    base, sc, bw = 300, 2.0, 52
    P = [title_t(400, "The mask fixes the shape, not the content")]
    for name, px, groups in panels:
        P.append(rect(px - 8, 62, 356, 296, 12, PAPER, GRID, 1.5, "6 4"))
        P.append(t(px + 170, 82, name, 18, INK, "middle"))
        P.append(line(px + 10, base, px + 330, base, INK, 2))
        for gi, (gl, free, mask) in enumerate(groups):
            gx = px + 20 + gi * 160
            P.append(rect(gx, base - free * sc, bw, free * sc, 2, DATA_F, DATA_S, 3))
            P.append(t(gx + bw / 2.0, base - free * sc - 6, str(free), 14, INK, "middle"))
            P.append(rect(gx + bw + 8, base - mask * sc, bw, mask * sc, 2, OK_F, OK_S, 3))
            P.append(t(gx + bw + 8 + bw / 2.0, base - mask * sc - 6, str(mask), 14, INK, "middle"))
            P.append(t(gx + bw / 2.0, 318, "free", 12, MUT, "middle"))
            P.append(t(gx + bw + 8 + bw / 2.0, 318, "mask", 12, MUT, "middle"))
            P.append(t(gx + bw + 4, 340, gl, 14, INK, "middle"))
    P.append(chip(602 - 50, 196, 100, "25 &#8594; 26: +1", ACC_S, ACC_F, 12, 26, mono=False))
    P.append(t(400, 374, "Out of 100 prompts per bar, seed 0: parses go to 100 / 100, but unseen names stay wrong.", 14, MUT, "middle"))
    return doc("0 0 800 400", "A grammar mask guarantees valid JSON but cannot make the content right",
               "Two panels of paired bars, each out of 100 prompts. Names seen in training: parses as JSON 90 free and 100 masked; every field right 79 free and 95 masked. "
               "New names never seen: parses 85 free and 100 masked; every field right 25 free and 26 masked, a gain of one.", P)


FIGS = {"fig-w22-1-sft-loss-mask.svg": w22_1,
        "fig-w22-2-kl-by-hand.svg": w22_2,
        "fig-w23-1-prompt-harness.svg": w23_1,
        "fig-w23-2-prompts-vs-floor.svg": w23_2,
        "fig-w24-1-in-context-vs-ceiling.svg": w24_1,
        "fig-w24-2-mask-shape-not-content.svg": w24_2}


def emit_b08():
    for name, fn in FIGS.items():
        open(os.path.join(HERE, name), "w").write(fn() + "\n")
    return len(FIGS)
