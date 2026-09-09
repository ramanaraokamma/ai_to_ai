#!/usr/bin/env python3
"""Figures for projects/worked-example-project.md and projects/capstone.md.

Same contract as _gen_assessments.py — see figures/STYLE.md.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_assessments import (  # noqa: E402
    DATA_S, DATA_F, MODEL_S, MODEL_F, HUMAN_S, HUMAN_F, OK_S, OK_F,
    BAD_S, BAD_F, ACC_S, ACC_F, INK, MUTED, GRID, PANEL, PAPER,
    SANS, MONO, txt, box, line, arrow, tick, cross, svg,
)


# ==================================================== WEP.1 the project map
def fig_wep_1():
    b = []
    b.append(txt(400, 40, "11 hours of project. The model was 40 minutes of it.",
                 24, INK, "middle"))

    stages = [
        ("1", "QUESTION", "1 h", "write it down,\nsigned and dated", HUMAN_S, HUMAN_F),
        ("2", "COLLECT", "3 h", "102 rows, typed\nby hand", DATA_S, DATA_F),
        ("3", "CLEAN", "2 h", "4 messes,\n4 logged reasons", DATA_S, DATA_F),
        ("4", "LOOK", "1.5 h", "describe(),\none scatter", DATA_S, DATA_F),
        ("5", "MODEL", "40 min", "three models,\none split", MODEL_S, MODEL_F),
        ("6", "TEST IT", "1.5 h", "k sweep,\nseed lottery", ACC_S, ACC_F),
        ("7", "WRITE UP", "1.5 h", "including what\nI got wrong", HUMAN_S, HUMAN_F),
    ]
    x0, w, gap = 32, 100, 6
    for i, (n, name, hrs, what, s, f) in enumerate(stages):
        bx = x0 + i * (w + gap)
        b.append(box(bx, 88, w, 148, f, s, 3, 10))
        b.append(f'<circle cx="{bx + w / 2}" cy="112" r="15" fill="{PAPER}" stroke="{s}" stroke-width="3"/>')
        b.append(txt(bx + w / 2, 112, n, 14, INK, "middle", central=True))
        b.append(txt(bx + w / 2, 146, name, 14, INK, "middle", weight="600"))
        b.append(txt(bx + w / 2, 166, hrs, 14, INK, "middle"))
        for j, ln in enumerate(what.split("\n")):
            b.append(txt(bx + w / 2, 194 + j * 17, ln, 12, MUTED, "middle"))
        if i < len(stages) - 1:
            b.append(arrow(bx + w + 1, 162, bx + w + gap - 1, 162, INK, 2))

    # the 40-minute bracket
    mx = x0 + 4 * (w + gap)
    b.append(f'<path d="M{mx} 254 V264 H{mx + w} V254" fill="none" stroke="{MODEL_S}" '
             f'stroke-width="2.5" stroke-linejoin="round"/>')
    b.append(txt(mx + w / 2, 288, "the bit everybody", 12, MODEL_S, "middle"))
    b.append(txt(mx + w / 2, 306, "thinks is the project", 12, MODEL_S, "middle"))

    # the 85% bracket
    b.append(f'<path d="M{x0} 254 V270 H{mx - 6} V254" fill="none" stroke="{HUMAN_S}" '
             f'stroke-width="2.5" stroke-linejoin="round"/>')
    b.append(f'<path d="M{mx + w + 6} 254 V270 H{x0 + 6 * (w + gap) + w} V254" fill="none" '
             f'stroke="{HUMAN_S}" stroke-width="2.5" stroke-linejoin="round"/>')
    b.append(txt(240, 292, "10 hours 20 minutes of this", 14, INK, "middle"))
    b.append(txt(672, 292, "and this", 14, INK, "middle"))

    b.append(txt(400, 344, "Every hour Nila spent on stages 1, 2 and 3 made stage 5 shorter.",
                 14, MUTED, "middle"))
    b.append(txt(400, 372, "Every hour she skipped there would have shown up in stage 7, where it hurts.",
                 12, MUTED, "middle"))
    svg("fig-wep-1-project-map.svg", "0 0 800 400",
        "11 hours of project. The model was 40 minutes of it.",
        "Seven numbered stages left to right with the hours each took: question 1 hour, collect 3 hours, clean 2 hours, look 1.5 hours, model 40 minutes, test it 1.5 hours, write up 1.5 hours. A bracket under the model stage is labelled the bit everybody thinks is the project. Brackets either side cover 10 hours 20 minutes of everything else.",
        b)


# ================================================== WEP.2 the four messes
def fig_wep_2():
    b = []
    b.append(txt(400, 38, "The four messes, and why the ORDER of the fixes matters",
                 24, INK, "middle"))
    b.append(txt(400, 62, "102 raw rows in. 100 clean rows out. Every change has a reason.",
                 14, MUTED, "middle"))

    messes = [
        ("1", "mood", "hype · Hype · chill ·  chill", "hype · chill",
         ".str.strip().str.title()", "4 spellings → 2. MUST be first"),
        ("2", "energy", "44   on a 1-5 scale", "4",
         "df.loc[df[\"energy\"] > 5]", "Typo, 1 row. I chose 4, not a mean"),
        ("3", "loudness", "two blank cells", "3   (the median)",
         "fillna(median), astype(int)", "Invents 2 values (really 4 and 5)"),
        ("4", "whole rows", "2 rows typed twice", "gone",
         "drop_duplicates()", "MUST be last — see note"),
    ]
    for i, (n, col, before, after, how, why) in enumerate(messes):
        ry = 88 + i * 68
        b.append(f'<circle cx="44" cy="{ry + 26}" r="15" fill="{ACC_F}" stroke="{ACC_S}" stroke-width="3"/>')
        b.append(txt(44, ry + 26, n, 14, INK, "middle", central=True))
        b.append(txt(70, ry + 18, col, 14, INK, weight="600"))
        # before
        b.append(box(146, ry + 4, 210, 44, BAD_F, BAD_S, 2, 8))
        b.append(txt(151, ry + 26, before, 12, INK, font=MONO, central=True))
        b.append(arrow(360, ry + 26, 386, ry + 26, INK, 2))
        # after
        b.append(box(392, ry + 4, 150, 44, OK_F, OK_S, 2, 8))
        b.append(txt(398, ry + 26, after, 12, INK, font=MONO, central=True))
        # how + why
        b.append(txt(556, ry + 20, how, 12, INK, font=MONO))
        b.append(txt(556, ry + 40, why, 12, MUTED))

    b.append(f'<rect x="32" y="366" width="736" height="0.1" rx="0" fill="none" stroke="none"/>')
    b.append(txt(400, 372, "Mess 4 last: \"Hype\" and \"hype\" are different strings, so duplicates are invisible until mess 1 is fixed.",
                 12, MUTED, "middle"))
    svg("fig-wep-2-four-messes.svg", "0 0 800 400",
        "The four messes, and why the ORDER of the fixes matters",
        "Four numbered repairs. One: the mood column had four spellings, hype, Hype, chill and space-chill, fixed to two with strip and title, and this must come first. Two: an energy value of 44 on a one-to-five scale, corrected to 4. Three: two blank loudness cells, filled with the median 3, which invents two values that were really 4 and 5. Four: two whole rows typed twice, removed with drop_duplicates, which must come last because Hype and hype are different strings.",
        b)


# ============================================ WEP.3 bpm drowns energy
def fig_wep_3():
    b = []
    b.append(txt(400, 40, "Why bpm drowned energy, in one sum", 24, INK, "middle"))
    b.append(txt(400, 64, "Distance adds up SQUARES. One column measured in hundreds wins every time.",
                 14, MUTED, "middle"))

    # two songs
    for i, (nm, bpm, en, bx) in enumerate([("song A", "158", "5", 60), ("song B", "92", "2", 250)]):
        b.append(box(bx, 90, 150, 90, DATA_F, DATA_S, 3, 10))
        b.append(txt(bx + 75, 112, nm, 14, INK, "middle"))
        b.append(txt(bx + 20, 140, "bpm", 12, MUTED))
        b.append(txt(bx + 130, 140, bpm, 18, INK, "end"))
        b.append(txt(bx + 20, 166, "energy", 12, MUTED))
        b.append(txt(bx + 130, 166, en, 18, INK, "end"))

    # the arithmetic
    b.append(box(60, 208, 344, 128, PANEL, GRID, 1.5, 10))
    rows = [
        ("bpm difference", "158−92 = 66", "66² = 4356", BAD_S),
        ("energy difference", "5 − 2 = 3", "3² = 9", OK_S),
        ("the distance sum", "4356 + 9", "= 4365", INK),
    ]
    for i, (lbl, calc, sq, col) in enumerate(rows):
        ry = 234 + i * 34
        b.append(txt(76, ry, lbl, 12, MUTED))
        b.append(txt(214, ry, calc, 12, INK, font=MONO))
        b.append(txt(388, ry, sq, 12, col, "end", font=MONO, weight="600" if i == 2 else None))

    # the share bar
    b.append(txt(596, 214, "who decided the answer?", 14, INK, "middle"))
    bar_x, bar_y, bar_w = 448, 232, 296
    share = 0.9979
    b.append(box(bar_x, bar_y, bar_w, 42, PAPER, INK, 2, 8))
    b.append(f'<rect x="{bar_x + 2}" y="{bar_y + 2}" width="{bar_w * share - 4:.1f}" height="38" rx="6" '
             f'fill="{BAD_F}" stroke="{BAD_S}" stroke-width="2" stroke-linejoin="round"/>')
    b.append(txt(bar_x + bar_w * share / 2, bar_y + 21, "bpm  99.79%", 14, INK, "middle", central=True))
    b.append(line(bar_x + bar_w * share, bar_y + 46, bar_x + bar_w - 8, 292, MUTED, 1.5))
    b.append(txt(bar_x + bar_w, 306, "energy  0.21%", 12, OK_S, "end"))
    b.append(txt(596, 336, "The 1-to-5 columns may as well not exist.", 12, MUTED, "middle"))

    b.append(txt(400, 378, "StandardScaler gives every column the same say. Fit it on the TRAINING rows only.",
                 14, MUTED, "middle"))
    svg("fig-wep-3-bpm-drowns-energy.svg", "0 0 800 400",
        "Why bpm drowned energy, in one sum",
        "Two song cards: song A at 158 bpm and energy 5, song B at 92 bpm and energy 2. The arithmetic panel shows the bpm difference of 66 squared is 4356, the energy difference of 3 squared is 9, and the distance sum is 4365. A bar on the right shows bpm accounting for 99.79 percent of that distance and energy 0.21 percent, captioned: the one-to-five columns may as well not exist.",
        b)


# ======================================== WEP.4 confusion matrix per class
def fig_wep_4():
    b = []
    b.append(txt(400, 38, "0.84 overall. But not for both kinds of song.", 24, INK, "middle"))
    b.append(txt(400, 62, "25 held-back songs. Row = the truth. Column = the guess.", 14, MUTED, "middle"))

    gx, gy, cw, ch = 190, 132, 104, 62
    b.append(txt(gx + cw, gy - 42, "PREDICTED", 14, MUTED, "middle"))
    for j, h in enumerate(["Chill", "Hype"]):
        b.append(txt(gx + j * cw + cw / 2, gy - 16, h, 14, INK, "middle"))
    b.append(f'<text x="{gx - 72}" y="{gy + ch}" font-family="{SANS}" font-size="14" fill="{MUTED}" '
             f'text-anchor="middle" transform="rotate(-90 {gx - 72} {gy + ch})">ACTUAL</text>')

    cells = [[("10", True), ("3", False)], [("1", False), ("11", True)]]
    labels = ["Chill", "Hype"]
    for i in range(2):
        b.append(txt(gx - 14, gy + i * ch + ch / 2, labels[i], 14, INK, "end", central=True))
        for j in range(2):
            v, diag = cells[i][j]
            f, s = (OK_F, OK_S) if diag else (BAD_F, BAD_S)
            b.append(box(gx + j * cw, gy + i * ch, cw, ch, f, s, 3, 0))
            b.append(txt(gx + j * cw + cw / 2, gy + i * ch + ch / 2, v, 24, INK, "middle", central=True))

    # per-class arithmetic
    b.append(box(430, 118, 338, 148, PANEL, GRID, 1.5, 10))
    b.append(txt(448, 142, "per-class accuracy — do the division", 12, MUTED))
    lines = [
        ("Chill", "10 ÷ 13 = 0.769 = 76.9%", BAD_S),
        ("Hype", "11 ÷ 12 = 0.917 = 91.7%", OK_S),
        ("overall", "21 ÷ 25 = 0.840 = 84.0%", INK),
    ]
    for i, (nm, calc, col) in enumerate(lines):
        ry = 172 + i * 30
        b.append(txt(448, ry, nm, 14, INK))
        b.append(txt(752, ry, calc, 12, col, "end", font=MONO,
                     weight="600" if i == 2 else None))
    b.append(line(448, 232, 752, 232, GRID, 1.5))
    b.append(txt(600, 254, "the gap: 14.8 PERCENTAGE POINTS", 12, ACC_S, "middle"))

    b.append(f'<rect x="190" y="284" width="578" height="52" rx="10" fill="{ACC_F}" '
             f'stroke="{ACC_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(479, 310, "3 chill songs were called hype. 1 hype song was called chill.",
                 14, INK, "middle", central=True))

    b.append(txt(400, 366, "One number hid two very different experiences. Always print the matrix.",
                 14, MUTED, "middle"))
    b.append(txt(400, 388, "And with 25 test rows, ONE song is worth 4 percentage points.",
                 12, MUTED, "middle"))
    svg("fig-wep-4-confusion-per-class.svg", "0 0 800 400",
        "0.84 overall. But not for both kinds of song.",
        "A two-by-two confusion matrix over 25 held-back songs, rows are the truth and columns are the guess. Chill row reads 10 correct and 3 wrong; Hype row reads 1 wrong and 11 correct. A panel does the divisions: Chill 10 over 13 is 76.9 percent, Hype 11 over 12 is 91.7 percent, overall 21 over 25 is 84.0 percent, a gap of 14.8 percentage points. A note adds that with 25 test rows one song is worth 4 percentage points.",
        b)


# ================================================== WEP.5 the seed lottery
def fig_wep_5():
    b = []
    b.append(txt(400, 38, "The same model, ten times, changing only the shuffle",
                 24, INK, "middle"))
    b.append(txt(400, 62, "Same 100 songs. Same k = 5. Same scaling. Only random_state changed.",
                 14, MUTED, "middle"))

    scores = [0.76, 0.88, 0.88, 0.80, 0.80, 0.96, 0.88, 0.84, 0.76, 0.68]
    px, py, pw, ph = 76, 96, 508, 160
    b.append(line(px, py + ph, px + pw, py + ph, INK, 2))
    b.append(line(px, py, px, py + ph, INK, 2))
    for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
        gy_ = py + ph - v * ph
        b.append(line(px + 2, gy_, px + pw - 2, gy_, GRID, 1.5))
        b.append(txt(px - 10, gy_, f"{v:.2f}", 12, MUTED, "end", central=True))
    bw = 38
    for i, v in enumerate(scores):
        bx = px + 14 + i * 48
        h = v * ph
        chosen = (i == 7)                 # random_state=42 would have been "the" one; 7 is the mid one
        f, s = (ACC_F, ACC_S) if chosen else (DATA_F, DATA_S)
        b.append(box(bx, py + ph - h, bw, h, f, s, 3, 4))
        b.append(txt(bx + bw / 2, py + ph - h - 8, f"{v:.2f}", 12, INK, "middle"))
        b.append(txt(bx + bw / 2, py + ph + 20, str(i), 12, MUTED, "middle"))
    b.append(txt(px + pw / 2, py + ph + 44, "random_state", 14, MUTED, "middle"))
    b.append(f'<text x="30" y="{py + ph / 2}" font-family="{SANS}" font-size="14" fill="{MUTED}" '
             f'text-anchor="middle" transform="rotate(-90 30 {py + ph / 2})">test accuracy</text>')

    b.append(box(604, 96, 164, 160, PANEL, GRID, 1.5, 10))
    stats = [("lowest", "0.68", BAD_S), ("highest", "0.96", OK_S),
             ("spread", "0.28", ACC_S), ("", "", None),
             ("that is", "28", INK), ("", "percentage points", MUTED)]
    for i, (k, v, col) in enumerate(stats):
        ry = 122 + i * 23
        if k:
            b.append(txt(620, ry, k, 12, MUTED))
        if v and col:
            b.append(txt(752, ry, v, 18 if v[0].isdigit() else 12, col, "end",
                         font=MONO if v[0].isdigit() else SANS))

    b.append(f'<rect x="76" y="316" width="692" height="46" rx="10" fill="{OK_F}" '
             f'stroke="{OK_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(422, 339, "So \"84%\" is one deal of the cards, not a property of the model.",
                 14, INK, "middle", central=True))
    b.append(txt(400, 386, "Report the number, the test-set size, AND the seed. Or report the spread.",
                 12, MUTED, "middle"))
    svg("fig-wep-5-seed-lottery.svg", "0 0 800 400",
        "The same model, ten times, changing only the shuffle",
        "Ten bars of test accuracy for random_state 0 to 9, all from the same 100 songs, same k of 5 and same scaling. The values are 0.76, 0.88, 0.88, 0.80, 0.80, 0.96, 0.88, 0.84, 0.76 and 0.68. A panel reports lowest 0.68, highest 0.96, spread 0.28, which is 28 percentage points. A green band concludes that 84 percent is one deal of the cards, not a property of the model.",
        b)


# ============================================== WEP.6 the scatter she drew
def fig_wep_6():
    HYPE = [(167,290),(93,184),(116,263),(114,293),(137,181),(166,290),(162,226),(134,245),
            (105,285),(106,171),(157,274),(143,258),(117,213),(150,231),(155,191),(134,255),
            (155,189),(120,299),(111,290),(84,182),(173,192),(136,285),(178,171),(108,252),
            (89,214),(113,203),(113,262),(104,247),(139,245),(175,253),(144,188),(123,179),
            (95,263),(107,281),(161,180),(96,281),(134,216),(114,219),(127,184),(173,201),
            (141,194),(173,252),(127,184),(179,291),(162,224),(112,257),(166,210),(137,235),
            (151,286),(141,229)]
    CHILL = [(77,277),(137,281),(80,229),(89,353),(150,220),(121,301),(126,220),(73,260),
             (129,288),(147,246),(117,301),(91,264),(126,249),(108,313),(78,232),(82,251),
             (150,314),(100,238),(79,322),(59,262),(60,293),(128,319),(99,298),(151,279),
             (112,257),(86,352),(122,358),(74,343),(154,342),(82,235),(153,338),(117,347),
             (106,328),(93,350),(72,308),(109,271),(66,333),(148,224),(152,216),(81,258),
             (144,341),(116,278),(85,226),(147,237),(134,340),(153,240),(106,255),(87,229),
             (65,328),(112,223)]
    b = []
    b.append(txt(400, 38, "The chart she should have drawn on day one", 24, INK, "middle"))
    b.append(txt(400, 62, "100 songs. Two features. The groups overlap, and that is the whole story.",
                 14, MUTED, "middle"))

    px, py, pw, ph = 92, 88, 470, 202
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{PANEL}" '
             f'stroke="{GRID}" stroke-width="1.5" stroke-linejoin="round"/>')
    b.append(line(px, py + ph, px + pw, py + ph, INK, 2))
    b.append(line(px, py, px, py + ph, INK, 2))

    xlo, xhi, ylo, yhi = 50, 190, 160, 370

    def SX(v):
        return px + 14 + (v - xlo) / (xhi - xlo) * (pw - 28)

    def SY(v):
        return py + ph - 12 - (v - ylo) / (yhi - ylo) * (ph - 26)

    for v in [60, 90, 120, 150, 180]:
        b.append(line(SX(v), py + ph, SX(v), py + ph + 6, MUTED, 1.5))
        b.append(txt(SX(v), py + ph + 22, str(v), 12, MUTED, "middle"))
    for v in [180, 240, 300, 360]:
        b.append(line(px - 6, SY(v), px, SY(v), MUTED, 1.5))
        b.append(txt(px - 10, SY(v), str(v), 12, MUTED, "end", central=True))
    b.append(txt(px + pw / 2, py + ph + 46, "beats per minute", 14, MUTED, "middle"))
    b.append(f'<text x="30" y="{py + ph / 2}" font-family="{SANS}" font-size="14" fill="{MUTED}" '
             f'text-anchor="middle" transform="rotate(-90 30 {py + ph / 2})">length in seconds</text>')

    # chill = open squares, hype = filled circles: shape AND colour, per STYLE.md
    for (bpm, sec) in CHILL:
        b.append(f'<rect x="{SX(bpm) - 4:.1f}" y="{SY(sec) - 4:.1f}" width="8" height="8" rx="1" '
                 f'fill="{PAPER}" stroke="{DATA_S}" stroke-width="2"/>')
    for (bpm, sec) in HYPE:
        b.append(f'<circle cx="{SX(bpm):.1f}" cy="{SY(sec):.1f}" r="4.5" fill="{BAD_F}" '
                 f'stroke="{BAD_S}" stroke-width="2"/>')

    # legend
    b.append(box(586, 96, 182, 92, PAPER, GRID, 1.5, 10))
    b.append(f'<circle cx="606" cy="124" r="5" fill="{BAD_F}" stroke="{BAD_S}" stroke-width="2"/>')
    b.append(txt(622, 129, "Hype  (50 songs)", 14, INK))
    b.append(f'<rect x="601" y="149" width="9" height="9" rx="1" fill="{PAPER}" stroke="{DATA_S}" stroke-width="2"/>')
    b.append(txt(622, 159, "Chill  (50 songs)", 14, INK))
    b.append(txt(602, 180, "shape AND colour, always", 12, MUTED))

    # the overlap callout
    b.append(box(586, 202, 182, 118, ACC_F, ACC_S, 3, 10))
    b.append(txt(677, 226, "what it told her", 12, MUTED, "middle"))
    for i, ln in enumerate(["No straight line", "separates these.",
                            "A model will get", "some wrong — and",
                            "84% may be near", "the ceiling."]):
        b.append(txt(677, 248 + i * 16, ln, 12, INK, "middle"))

    b.append(txt(400, 364, "Ten minutes with this chart would have saved her the surprise in stage 5.",
                 14, MUTED, "middle"))
    b.append(txt(400, 388, "Draw the picture before you fit anything. Every time.", 12, MUTED, "middle"))
    svg("fig-wep-6-scatter-overlap.svg", "0 0 800 400",
        "The chart she should have drawn on day one",
        "A scatter plot of 100 songs, beats per minute along the bottom from 50 to 190 and length in seconds up the side from 160 to 370. Fifty filled red circles are Hype songs and fifty open blue squares are Chill songs. The two groups overlap heavily through the middle of the chart. A callout reads: no straight line separates these, a model will get some wrong, and 84 percent may be near the ceiling.",
        b)


if __name__ == "__main__":
    print("writing worked-example figures:")
    fig_wep_1(); fig_wep_2(); fig_wep_3(); fig_wep_4(); fig_wep_5(); fig_wep_6()
    print("done.")
