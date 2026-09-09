#!/usr/bin/env python3
"""Generate the assessment/project figures for Level 2's 36-week course.

Follows figures/STYLE.md exactly: eight palette roles used by role, two system
font stacks, 3px primary strokes, round caps and joins, viewBox only, no white
background rect, 12px type floor, role="img" + <title> + <desc> on every file.
"""
import os
import xml.dom.minidom

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- palette
DATA_S, DATA_F = "#1F6FB2", "#D9EAF9"
MODEL_S, MODEL_F = "#6D28D9", "#DBCEF3"
HUMAN_S, HUMAN_F = "#845F00", "#E8C671"
OK_S, OK_F = "#1B7A4B", "#E2F7ED"
BAD_S, BAD_F = "#CC2B1D", "#F6AEA6"
ACC_S, ACC_F = "#C42B8C", "#F4D5E9"
INK = "#14202B"
MUTED = "#55636F"
GRID = "#C7CDD4"
PANEL = "#F5F8FA"
PAPER = "#FFFFFF"

SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


# ---------------------------------------------------------------- helpers
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def txt(x, y, s, size=12, fill=INK, anchor="start", font=SANS, weight=None,
        central=False):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight else ""
    c = ' dominant-baseline="central"' if central else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}"{a}{w}{c}>{esc(s)}</text>')


def box(x, y, w, h, fill=PAPER, stroke=INK, sw=3, rx=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round"/>')


def line(x1, y1, x2, y2, stroke=INK, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round"{d}/>')


def arrow(x1, y1, x2, y2, stroke=INK, sw=3):
    """A straight arrow from (x1,y1) to (x2,y2) with a chevron head."""
    import math
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (line(x1, y1, x2, y2, stroke, sw) +
            f'<polyline points="-13,-8 0,0 -13,8" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'transform="translate({x2} {y2}) rotate({ang:.2f})"/>')


def tick(cx, cy, r=17, stroke=OK_S, fill=OK_F):
    s = r / 34.0
    return (f'<g transform="translate({cx - r},{cy - r}) scale({s:.4f})">'
            f'<circle cx="34" cy="34" r="32" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
            f'<polyline points="18,36 29,48 52,22" fill="none" stroke="{stroke}" '
            f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>')


def cross(cx, cy, r=17, stroke=BAD_S, fill=BAD_F):
    s = r / 34.0
    return (f'<g transform="translate({cx - r},{cy - r}) scale({s:.4f})">'
            f'<circle cx="34" cy="34" r="32" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
            f'<line x1="22" y1="22" x2="46" y2="46" stroke="{stroke}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="46" y1="22" x2="22" y2="46" stroke="{stroke}" stroke-width="7" stroke-linecap="round"/></g>')


def svg(name, vb, title, desc, body):
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img">\n'
           f'  <title>{esc(title)}</title>\n'
           f'  <desc>{esc(desc)}</desc>\n'
           + "\n".join("  " + b for b in body) + "\n</svg>\n")
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(out)
    xml.dom.minidom.parseString(out)          # must parse
    banned = ["<image", 'href="http', "@font-face", "<filter", "feGaussianBlur",
              "feDropShadow", "<foreignObject", "<script", "Gradient"]
    for b in banned:
        assert b not in out, f"{name}: banned construct {b}"
    assert 'role="img"' in out and "<title>" in out and "<desc>" in out
    import re
    for m in re.finditer(r'font-size="([0-9.]+)"', out):
        assert float(m.group(1)) >= 12, f"{name}: font-size {m.group(1)} below floor"
    for m in re.finditer(r"scale\(([0-9.]+)", out):
        pass
    print(f"  {name}  ({len(out)} bytes)")


# ============================================================ T1.1 trace table
def fig_t1_1():
    b = []
    b.append(txt(400, 44, "A trace table: one row per pass, one column per box",
                 24, INK, "middle"))
    b.append(txt(400, 68, "When a value changes, cross out the old one. Never rub it out.",
                 14, MUTED, "middle"))

    # panel
    b.append(f'<rect x="20" y="88" width="760" height="272" rx="12" fill="{PANEL}" '
             f'stroke="{GRID}" stroke-width="1.5" stroke-linejoin="round"/>')

    # left: the code, as data values only (no syntax) - a stack of 3 pass labels
    b.append(txt(44, 124, "the loop, 3 passes", 14, INK))
    for i, (lbl, cy) in enumerate([("pass 1", 168), ("pass 2", 232), ("pass 3", 296)]):
        b.append(f'<circle cx="92" cy="{cy}" r="26" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
        b.append(txt(92, cy - 8, "step", 12, MUTED, "middle", central=True))
        b.append(txt(92, cy + 9, ["2", "5", "8"][i], 24, INK, "middle", central=True))
        b.append(txt(92, cy + 44, lbl, 12, MUTED, "middle"))

    # the table: two value columns
    tx = 200
    colw = 150
    b.append(txt(tx + colw / 2, 128, "total  before", 14, MUTED, "middle"))
    b.append(txt(tx + colw + colw / 2, 128, "total  after", 14, MUTED, "middle"))
    b.append(txt(tx + 2 * colw + 108, 128, "what got printed", 14, MUTED, "middle"))

    rows = [("0", "2", "2 2"), ("2", "7", "5 7"), ("7", "15", "8 15")]
    for i, (before, after, printed) in enumerate(rows):
        ry = 142 + i * 64
        # before cell
        b.append(box(tx, ry, colw - 12, 48, DATA_F, DATA_S, 2, 8))
        b.append(txt(tx + (colw - 12) / 2, ry + 24, before, 18, INK, "middle", central=True))
        if i > 0:  # struck through: the value it used to be
            b.append(line(tx + 12, ry + 24, tx + colw - 24, ry + 24, BAD_S, 2.5))
        # after cell
        b.append(box(tx + colw, ry, colw - 12, 48, ACC_F, ACC_S, 3, 8))
        b.append(txt(tx + colw + (colw - 12) / 2, ry + 24, after, 18, INK, "middle", central=True))
        # arrow between
        b.append(arrow(tx + colw - 16, ry + 24, tx + colw - 2, ry + 24, INK, 2))
        # printed
        b.append(box(tx + 2 * colw + 24, ry, 168, 48, PAPER, GRID, 1.5, 8))
        b.append(txt(tx + 2 * colw + 108, ry + 24, printed, 14, INK, "middle",
                     font=MONO, central=True))

    b.append(txt(400, 348, "The crossings-out ARE your working, and working earns marks.",
                 14, MUTED, "middle"))
    svg("fig-t1-1-trace-table.svg", "0 0 800 400",
        "A trace table: one column per variable, one row per line of code, with the value crossed out and rewritten each time it changes",
        "A worked trace table. Down the left, three numbered counters read 2, 5 and 8, labelled pass 1, pass 2 and pass 3. Two value columns show the accumulator before and after each pass: 0 becomes 2, then 2 becomes 7, then 7 becomes 15, with each old value struck through in red. A third column shows what each pass printed.",
        b)


# ======================================================= T1.2 traceback anatomy
def fig_t1_2():
    b = []
    b.append(txt(400, 42, "Every traceback has four parts. Read part 4 first.",
                 24, INK, "middle"))

    # the traceback panel (sanctioned exception: the artefact IS the lesson)
    b.append(f'<rect x="40" y="70" width="452" height="176" rx="10" fill="{PANEL}" '
             f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(line(40, 100, 492, 100, GRID, 1.5))
    b.append(txt(56, 90, "terminal", 12, MUTED))

    lines = [
        ("Traceback (most recent call last):", MUTED, False),
        ('  File "total.py", line 4, in <module>', INK, False),
        ('    print(f"The total is {totl}")', INK, False),
        ("NameError: name 'totl' is not defined", BAD_S, True),
    ]
    # highlight bar behind the last line, drawn first so nothing sits on top of text
    b.append(f'<rect x="48" y="{128 + 3 * 30 - 15}" width="436" height="24" rx="6" '
             f'fill="{BAD_F}" stroke="{BAD_S}" stroke-width="2" stroke-linejoin="round"/>')
    for i, (s, col, bold) in enumerate(lines):
        ly = 128 + i * 30
        b.append(txt(56, ly, s, 12, INK if bold else col, font=MONO,
                     weight="600" if bold else None))

    # numbered pins on the right
    pins = [
        (1, 128, "a header. Ignore it."),
        (2, 158, "WHICH FILE, WHICH LINE"),
        (3, 188, "your line, quoted back"),
        (4, 218, "THE KIND OF PROBLEM"),
    ]
    for n, py, label in pins:
        col_s, col_f = (ACC_S, ACC_F) if n in (2, 4) else (GRID, PAPER)
        b.append(arrow(500, py - 4, 528, py - 4, MUTED, 1.5))
        b.append(f'<circle cx="548" cy="{py - 4}" r="15" fill="{col_f}" stroke="{col_s}" stroke-width="3"/>')
        b.append(txt(548, py - 4, str(n), 14, INK, "middle", central=True))
        b.append(txt(570, py, label, 12, INK))

    # the three-step order
    b.append(f'<rect x="40" y="266" width="720" height="60" rx="10" fill="{OK_F}" '
             f'stroke="{OK_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(60, 292, "READ IN THIS ORDER", 12, MUTED))
    steps = [("4", "the last line", 236), ("2", "the line number", 430), ("3", "your code", 636)]
    for i, (n, label, sx) in enumerate(steps):
        b.append(f'<circle cx="{sx - 44}" cy="303" r="14" fill="{PAPER}" stroke="{OK_S}" stroke-width="3"/>')
        b.append(txt(sx - 44, 303, n, 14, INK, "middle", central=True))
        b.append(txt(sx - 22, 308, label, 18, INK))
        if i < 2:
            b.append(arrow(sx + 84, 303, sx + 128, 303, OK_S, 2.5))

    b.append(txt(400, 356, "The last line names the KIND of problem. Everything else tells you where.",
                 14, MUTED, "middle"))
    b.append(txt(400, 380, "Three steps, in that order, every single time.", 14, MUTED, "middle"))
    svg("fig-t1-2-traceback-anatomy.svg", "0 0 800 400",
        "The four parts of a Python traceback, with the last line marked as the one to read first",
        "A terminal panel shows a four-line traceback ending in a NameError, with the last line highlighted in red. Four numbered pins on the right label the parts: a header to ignore, the file and line number, your own quoted code, and the kind of problem. A green band underneath gives the reading order: last line first, then the line number, then your code.",
        b)


# =============================================== T2.1 list of dicts is a table
def fig_t2_1():
    b = []
    b.append(txt(400, 42, "A list of dictionaries IS a table", 24, INK, "middle"))
    b.append(txt(400, 66, "One dictionary is one row. The keys are the column names.",
                 14, MUTED, "middle"))

    # LEFT: four cards, each with three key->value pairs
    b.append(txt(30, 100, "what you typed: four dictionaries", 14, MUTED))
    for i, (nm, ag, sc) in enumerate([("Asha", "13", "80"), ("Ben", "11", "55"),
                                      ("Cara", "14", "92"), ("Dev", "12", "67")]):
        cy = 116 + i * 60
        b.append(box(30, cy, 300, 48, PAPER, GRID, 1.5, 8))
        for j, (k, v) in enumerate([("name", nm), ("age", ag), ("score", sc)]):
            kx = 42 + j * 98
            b.append(box(kx, cy + 8, 46, 32, ACC_F, ACC_S, 2, 6))
            b.append(txt(kx + 23, cy + 24, k, 12, INK, "middle", central=True))
            b.append(box(kx + 48, cy + 8, 42, 32, DATA_F, DATA_S, 2, 6))
            b.append(txt(kx + 69, cy + 24, v, 12, INK, "middle", central=True))
        b.append(txt(28, cy + 28, str(i), 12, MUTED, "middle"))

    # arrow across
    b.append(arrow(348, 240, 408, 240, INK, 3))
    b.append(txt(378, 226, "same thing", 12, MUTED, "middle"))

    # RIGHT: the same thing as a grid with a header row
    gx, gy = 430, 146
    cw, ch = 108, 44
    heads = ["name", "age", "score"]
    for j, h in enumerate(heads):
        b.append(box(gx + j * cw, gy - 44, cw, 44, ACC_F, ACC_S, 3, 0))
        b.append(txt(gx + j * cw + cw / 2, gy - 22, h, 14, INK, "middle",
                     weight="600", central=True))
    data = [("Asha", "13", "80"), ("Ben", "11", "55"),
            ("Cara", "14", "92"), ("Dev", "12", "67")]
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            b.append(box(gx + j * cw, gy + i * ch, cw, ch, PAPER, GRID, 1.5, 0))
            b.append(txt(gx + j * cw + cw / 2, gy + i * ch + ch / 2, v, 14, INK,
                         "middle", central=True))
        b.append(txt(gx - 12, gy + i * ch + ch / 2, str(i), 12, MUTED, "end", central=True))
    b.append(txt(gx + 1.5 * cw, gy - 58, "the keys become the header row", 12, MUTED, "middle"))
    b.append(txt(gx - 14, gy - 14, "index", 12, MUTED, "end"))

    b.append(txt(400, 376, "Stuck on a question? Draw this. A picture on your rough paper earns marks.",
                 14, MUTED, "middle"))
    svg("fig-t2-1-list-of-dicts-is-a-table.svg", "0 0 800 400",
        "A list of four dictionaries drawn as a table: four cards stacked, each with the same three keys, and the keys lined up so they form columns with a header row",
        "On the left, four stacked cards numbered 0 to 3. Each card holds three key-and-value pairs: name, age and score, with the keys in pink boxes and the values in blue boxes. An arrow labelled same thing points right to a grid with a pink header row reading name, age, score and four data rows holding Asha 13 80, Ben 11 55, Cara 14 92 and Dev 12 67, numbered 0 to 3 down the left.",
        b)


# ================================================== T2.2 shape mismatch
def fig_t2_2():
    b = []
    b.append(txt(400, 40, "shapes (4,) and (3,) cannot be paired up", 24, INK, "middle"))

    slot = 125
    x0 = 150
    # top row: 4 filled
    b.append(txt(x0 - 18, 96, "morning", 18, INK, "end"))
    b.append(txt(x0 - 18, 118, "shape (4,)", 12, MUTED, "end"))
    for i, v in enumerate([1200, 900, 1500, 1100]):
        b.append(box(x0 + i * slot, 78, slot - 14, 54, DATA_F, DATA_S, 3, 8))
        b.append(txt(x0 + i * slot + (slot - 14) / 2, 105, str(v), 18, INK, "middle", central=True))

    # bottom row: 3 filled + 1 empty
    b.append(txt(x0 - 18, 208, "evening", 18, INK, "end"))
    b.append(txt(x0 - 18, 230, "shape (3,)", 12, MUTED, "end"))
    for i, v in enumerate([800, 1000, 700]):
        b.append(box(x0 + i * slot, 190, slot - 14, 54, DATA_F, DATA_S, 3, 8))
        b.append(txt(x0 + i * slot + (slot - 14) / 2, 217, str(v), 18, INK, "middle", central=True))
    # the empty fourth slot
    b.append(f'<rect x="{x0 + 3 * slot}" y="190" width="{slot - 14}" height="54" rx="8" '
             f'fill="{PAPER}" stroke="{BAD_S}" stroke-width="3" stroke-dasharray="7 6" '
             f'stroke-linejoin="round"/>')
    b.append(txt(x0 + 3 * slot + (slot - 14) / 2, 217, "?", 24, BAD_S, "middle", central=True))

    # pairing lines: 3 good, 1 bad
    for i in range(3):
        cx = x0 + i * slot + (slot - 14) / 2
        b.append(line(cx, 136, cx, 186, OK_S, 2.5))
        b.append(tick(cx, 161, 13))
    cx = x0 + 3 * slot + (slot - 14) / 2
    b.append(line(cx, 136, cx, 186, BAD_S, 2.5, "6 5"))
    b.append(cross(cx, 161, 14))

    b.append(txt(cx + 30, 156, "no partner", 14, INK))
    b.append(txt(cx + 30, 176, "for slot 3", 14, INK))

    # verdict band
    b.append(f'<rect x="40" y="272" width="720" height="56" rx="10" fill="{BAD_F}" '
             f'stroke="{BAD_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(400, 300, "numpy refuses. It will NOT invent a zero for the empty slot.",
                 18, INK, "middle", central=True))
    b.append(txt(400, 356, "The bug is in the data on lines 3 and 4, not in the + on line 5.",
                 14, MUTED, "middle"))
    b.append(txt(400, 380, "Check it in one line before you add:  print(morning.shape, evening.shape)",
                 12, MUTED, "middle", font=MONO))
    svg("fig-t2-2-shape-mismatch.svg", "0 0 800 400",
        "Two rows of slots side by side: the top row has four filled slots, the bottom row has three filled slots and one empty slot with a cross over it, showing there is no partner for the fourth value",
        "The top row, labelled morning shape 4, has four blue slots holding 1200, 900, 1500 and 1100. The bottom row, labelled evening shape 3, has three blue slots holding 800, 1000 and 700, and a fourth dashed red slot holding a question mark. Green ticks join the first three pairs; a red cross marks the fourth, labelled no partner for slot 3. A red band reads: numpy refuses, it will not invent a zero for the empty slot.",
        b)


# ================================================== T3.1 axis 0 vs axis 1
def fig_t3_1():
    b = []
    b.append(txt(400, 40, "axis=0 walks DOWN. axis=1 walks ACROSS.", 24, INK, "middle"))

    grid = [[12, 40, 5], [8, 33, 2], [20, 51, 9]]
    cw, ch = 84, 52
    gx, gy = 214, 96

    # column headers
    for j, m in enumerate(["Jan", "Feb", "Mar"]):
        b.append(txt(gx + j * cw + cw / 2, gy - 12, m, 14, MUTED, "middle"))
    # row labels
    for i, c in enumerate(["City A", "City B", "City C"]):
        b.append(txt(gx - 14, gy + i * ch + ch / 2, c, 14, MUTED, "end", central=True))

    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            b.append(box(gx + j * cw, gy + i * ch, cw, ch, DATA_F, DATA_S, 2, 0))
            b.append(txt(gx + j * cw + cw / 2, gy + i * ch + ch / 2, str(v), 18,
                         INK, "middle", central=True))

    # axis=1 : across, to the right, one answer per row
    for i, total in enumerate([57, 43, 80]):
        ay = gy + i * ch + ch / 2
        b.append(arrow(gx + 3 * cw + 6, ay, gx + 3 * cw + 52, ay, ACC_S, 3))
        b.append(box(gx + 3 * cw + 62, gy + i * ch + 7, 74, ch - 14, ACC_F, ACC_S, 3, 8))
        b.append(txt(gx + 3 * cw + 99, ay, str(total), 18, INK, "middle", central=True))
    b.append(txt(gx + 3 * cw + 99, gy - 12, "axis=1", 14, ACC_S, "middle"))
    b.append(txt(gx + 3 * cw + 99, gy + 3 * ch + 24, "3 answers,", 12, MUTED, "middle"))
    b.append(txt(gx + 3 * cw + 99, gy + 3 * ch + 42, "one per ROW", 12, MUTED, "middle"))

    # axis=0 : down, underneath, one answer per column
    for j, mean in enumerate(["13.3", "41.3", "5.3"]):
        ax_ = gx + j * cw + cw / 2
        b.append(arrow(ax_, gy + 3 * ch + 6, ax_, gy + 3 * ch + 42, MODEL_S, 3))
        b.append(box(gx + j * cw + 6, gy + 3 * ch + 50, cw - 12, 42, MODEL_F, MODEL_S, 3, 8))
        b.append(txt(ax_, gy + 3 * ch + 71, mean, 18, INK, "middle", central=True))
    b.append(txt(gx - 14, gy + 3 * ch + 71, "axis=0", 14, MODEL_S, "end", central=True))
    b.append(txt(gx + 1.5 * cw, gy + 3 * ch + 112, "3 answers, one per COLUMN", 12, MUTED, "middle"))

    b.append(txt(400, 382, "Count the answers you expect BEFORE you run it. There is no error for the wrong axis.",
                 14, MUTED, "middle"))
    svg("fig-t3-1-axis-0-vs-axis-1.svg", "0 0 800 400",
        "A three-by-three grid of numbers with a downward arrow labelled axis equals 0 walking down each column producing three answers, and a rightward arrow labelled axis equals 1 walking across each row also producing three answers, with the two answer strips shown separately",
        "A three-by-three grid of rainfall numbers, rows labelled City A, B and C and columns labelled Jan, Feb, Mar. Pink arrows point right out of each row into three answer boxes reading 57, 43 and 80, labelled axis equals 1, three answers one per row. Purple arrows point down out of each column into three answer boxes reading 13.3, 41.3 and 5.3, labelled axis equals 0, three answers one per column.",
        b)


# ============================================ T3.2 truncated axis pair
def fig_t3_2():
    b = []
    b.append(txt(400, 38, "The same three numbers, twice", 24, INK, "middle"))
    b.append(txt(400, 60, "Nothing changed but where the y-axis starts.", 14, MUTED, "middle"))

    houses = ["Blue", "Green", "Red"]
    vals = [74.4, 72.9, 73.1]

    def panel(px, lo, hi, title, tcol, tfill, note):
        out = []
        pw, ph = 260, 200
        py = 106
        out.append(f'<rect x="{px - 16}" y="{py - 30}" width="{pw + 80}" height="{ph + 92}" rx="12" '
                   f'fill="{tfill}" stroke="{tcol}" stroke-width="3" stroke-linejoin="round"/>')
        out.append(txt(px + pw / 2 + 24, py - 8, title, 14, INK, "middle", weight="600"))
        # axes
        out.append(line(px + 46, py + 14, px + 46, py + ph, INK, 2))
        out.append(line(px + 46, py + ph, px + pw + 46, py + ph, INK, 2))
        # y ticks: lo, mid, hi
        for frac, lab in [(0.0, lo), (0.5, (lo + hi) / 2), (1.0, hi)]:
            ty = py + ph - frac * (ph - 14)
            out.append(line(px + 40, ty, px + 46, ty, MUTED, 1.5))
            lab_s = f"{lab:.0f}" if float(lab).is_integer() else f"{lab:.1f}"
            out.append(txt(px + 34, ty, lab_s, 12, MUTED, "end", central=True))
        # bars
        bw = 52
        for i, v in enumerate(vals):
            frac = max(0.0, (v - lo) / (hi - lo))
            h = frac * (ph - 14)
            bx = px + 66 + i * 72
            out.append(box(bx, py + ph - h, bw, max(h, 2), DATA_F, DATA_S, 3, 4))
            out.append(txt(bx + bw / 2, py + ph + 20, houses[i], 12, MUTED, "middle"))
            out.append(txt(bx + bw / 2, py + ph - h - 8, f"{v}", 12, INK, "middle"))
        out.append(txt(px + pw / 2 + 24, py + ph + 48, note, 12, MUTED, "middle"))
        return out

    b += panel(48, 72.5, 74.6, "THE LIE:  set_ylim(72.5, 74.6)", BAD_S, BAD_F,
               "Blue's bar is 4.75x Green's")
    b += panel(444, 0, 100, "THE FIX:  set_ylim(0, 100)", OK_S, OK_F,
               "Blue's bar is 1.02x Green's")

    b.append(txt(400, 384, "Real gap: 74.4 - 72.9 = 1.5 marks out of 100. Bars encode LENGTH, so bars need zero.",
                 12, MUTED, "middle"))
    svg("fig-t3-2-truncated-axis-pair.svg", "0 0 800 400",
        "Two bar charts side by side from the same three numbers: on the left the y-axis starts at seventy-two point five and the first bar towers over the others; on the right the y-axis starts at zero and the three bars are almost identical in height",
        "Left panel, framed in red and headed THE LIE with set y limits of 72.5 to 74.6: three bars for Blue, Green and Red at 74.4, 72.9 and 73.1, where Blue's bar is nearly five times taller than Green's. Right panel, framed in green and headed THE FIX with set y limits of 0 to 100: the same three values, and the three bars are now almost exactly the same height. A caption states the real gap is 1.5 marks out of 100.",
        b)


# ======================================== T4.1 the split and the two scores
def fig_t4_1():
    b = []
    b.append(txt(400, 40, "Cut the deck first. Score on the sealed pile.", 24, INK, "middle"))

    # the whole deck
    b.append(txt(104, 78, "150 rows", 14, MUTED, "middle"))
    for i in range(5):
        b.append(box(56 + i * 4, 92 - i * 4, 96, 104, DATA_F, DATA_S, 2, 8))
    b.append(txt(104, 140, "all your", 12, INK, "middle"))
    b.append(txt(104, 158, "data", 12, INK, "middle"))

    # the cut
    b.append(line(184, 74, 184, 200, ACC_S, 3, "8 6"))
    b.append(txt(184, 66, "one cut", 12, ACC_S, "middle"))
    b.append(txt(184, 216, "before the model", 12, MUTED, "middle"))
    b.append(txt(184, 234, "sees anything", 12, MUTED, "middle"))

    # train pile (big)
    b.append(arrow(200, 104, 244, 104, INK, 2.5))
    for i in range(4):
        b.append(box(252 + i * 4, 78 - i * 4, 128, 84, DATA_F, DATA_S, 2, 8))
    b.append(txt(316, 104, "TRAIN", 18, INK, "middle"))
    b.append(txt(316, 126, "120 rows  ·  80%", 12, MUTED, "middle"))
    b.append(txt(316, 178, "the model studies these", 12, MUTED, "middle"))

    # test pile (small, sealed)
    b.append(arrow(200, 180, 244, 180, INK, 2.5))
    b.append(box(252, 208, 128, 58, ACC_F, ACC_S, 3, 8))
    b.append(txt(316, 230, "TEST", 18, INK, "middle"))
    b.append(txt(316, 250, "30 rows  ·  20%", 12, MUTED, "middle"))
    b.append(txt(316, 288, "SEALED. Nobody looks.", 12, ACC_S, "middle"))

    # the two readouts
    b.append(arrow(396, 104, 448, 104, MUTED, 2))
    b.append(box(456, 76, 296, 56, PAPER, GRID, 1.5, 10))
    b.append(txt(472, 96, "score on the TRAINING rows", 12, MUTED))
    b.append(txt(472, 120, "0.9417", 24, INK, font=MONO))
    b.append(txt(600, 120, "a fact about the past", 14, MUTED))

    b.append(arrow(396, 232, 448, 232, MUTED, 2))
    b.append(box(456, 204, 296, 56, ACC_F, ACC_S, 3, 10))
    b.append(txt(472, 224, "score on the HELD-BACK rows", 12, MUTED))
    b.append(txt(472, 248, "0.7333", 24, INK, font=MONO))
    b.append(tick(724, 232, 16))

    b.append(f'<rect x="456" y="278" width="296" height="46" rx="10" fill="{OK_F}" '
             f'stroke="{OK_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(604, 301, "quote THIS one, and only this one", 14, INK, "middle", central=True))

    b.append(txt(400, 358, "Two numbers. One of them is a claim about the future. The other is a memory test.",
                 14, MUTED, "middle"))
    b.append(txt(400, 382, "The gap between them, 0.9417 - 0.7333 = 0.2083, is itself information.",
                 12, MUTED, "middle"))
    svg("fig-t4-1-split-and-two-scores.svg", "0 0 800 400",
        "A deck of cards being cut once into a large pile labelled train with 120 cards and a small sealed pile labelled test with 30 cards, with two score readouts beside them and only the test score circled as the one you may quote",
        "A stack of 150 rows on the left is cut once by a dashed pink line labelled one cut before the model sees anything. It becomes a large blue TRAIN pile of 120 rows, 80 percent, which the model studies, and a small pink TEST pile of 30 rows, 20 percent, marked sealed, nobody looks. Two readouts on the right: the training score 0.9417, labelled a fact about the past, and the held-back score 0.7333 with a green tick. A green band reads: quote this one, and only this one.",
        b)


# ============================================ T4.2 the overfitting cliff
def fig_t4_2():
    b = []
    b.append(txt(400, 38, "Training error falls forever. Test error has a bottom.",
                 24, INK, "middle"))

    depths = [1, 2, 3, 5, 8, 12, 15, 20]
    train = [54.47, 47.33, 43.68, 35.25, 17.50, 3.66, 0.46, 0.00]
    test = [56.51, 49.37, 48.10, 45.94, 48.72, 53.07, 53.06, 54.53]

    # plot box
    px, py, pw, ph = 92, 76, 500, 218
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{PANEL}" '
             f'stroke="{GRID}" stroke-width="1.5" stroke-linejoin="round"/>')
    b.append(line(px, py + ph, px + pw, py + ph, INK, 2))
    b.append(line(px, py, px, py + ph, INK, 2))

    ymax = 60.0

    def sx(d):
        return px + 24 + (depths.index(d) / (len(depths) - 1)) * (pw - 50)

    def sy(v):
        return py + ph - (v / ymax) * (ph - 18)

    # y gridlines
    for v in [0, 20, 40, 60]:
        gy_ = sy(v)
        b.append(line(px + 2, gy_, px + pw - 2, gy_, GRID, 1.5))
        b.append(txt(px - 10, gy_, str(v), 12, MUTED, "end", central=True))

    # x labels
    for d in depths:
        b.append(txt(sx(d), py + ph + 20, str(d), 12, MUTED, "middle"))
    b.append(txt(px + pw / 2, py + ph + 44, "max_depth of the tree", 14, MUTED, "middle"))
    b.append(f'<text x="30" y="{py + ph / 2}" font-family="{SANS}" font-size="14" '
             f'fill="{MUTED}" text-anchor="middle" '
             f'transform="rotate(-90 30 {py + ph / 2})">mean absolute error</text>')

    # the vertical marker at depth 5
    b.append(line(sx(5), py + 6, sx(5), py + ph - 2, ACC_S, 2.5, "8 6"))
    b.append(txt(sx(5) + 8, py + 20, "depth 5", 12, ACC_S))
    b.append(txt(sx(5) + 8, py + 38, "they part", 12, MUTED))
    b.append(txt(sx(5) + 8, py + 56, "company here", 12, MUTED))

    # curves
    for vals, col, fillc in [(train, MODEL_S, MODEL_F), (test, BAD_S, BAD_F)]:
        pts = " ".join(f"{sx(d):.1f},{sy(v):.1f}" for d, v in zip(depths, vals))
        b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
        for d, v in zip(depths, vals):
            b.append(f'<circle cx="{sx(d):.1f}" cy="{sy(v):.1f}" r="5" fill="{fillc}" '
                     f'stroke="{col}" stroke-width="2.5"/>')

    # end labels
    b.append(txt(sx(20) + 10, sy(0.0) + 4, "0.00", 12, MODEL_S))
    b.append(txt(sx(20) + 10, sy(54.53) + 4, "54.53", 12, BAD_S))
    b.append(txt(sx(1) - 4, sy(54.47) - 10, "54.47", 12, MODEL_S, "middle"))
    b.append(txt(sx(1) + 30, sy(56.51) - 10, "56.51", 12, BAD_S, "middle"))

    # legend
    b.append(box(612, 88, 168, 96, PAPER, GRID, 1.5, 10))
    b.append(line(626, 114, 656, 114, MODEL_S, 3))
    b.append(f'<circle cx="641" cy="114" r="5" fill="{MODEL_F}" stroke="{MODEL_S}" stroke-width="2.5"/>')
    b.append(txt(664, 119, "train MAE", 14, INK))
    b.append(txt(626, 140, "rows it studied", 12, MUTED))
    b.append(line(626, 160, 656, 160, BAD_S, 3))
    b.append(f'<circle cx="641" cy="160" r="5" fill="{BAD_F}" stroke="{BAD_S}" stroke-width="2.5"/>')
    b.append(txt(664, 165, "test MAE", 14, INK))
    b.append(txt(626, 178, "rows it never saw", 12, MUTED))

    # verdict
    b.append(f'<rect x="612" y="196" width="168" height="98" rx="10" fill="{BAD_F}" '
             f'stroke="{BAD_S}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(txt(696, 222, "a train MAE of", 12, INK, "middle"))
    b.append(txt(696, 248, "0.00", 24, INK, "middle", font=MONO))
    b.append(txt(696, 272, "is a WARNING,", 12, INK, "middle"))
    b.append(txt(696, 288, "not a result", 12, INK, "middle"))

    b.append(txt(400, 364, "Ship the model at the BOTTOM of the test curve: depth 5, MAE 45.94.",
                 14, MUTED, "middle"))
    b.append(txt(400, 386, "Depth 20 memorised 353 patients perfectly and is worse than one yes/no question.",
                 12, MUTED, "middle"))
    svg("fig-t4-2-overfitting-cliff.svg", "0 0 800 400",
        "Two lines plotted against tree depth: the training error falls smoothly all the way to zero while the test error falls to a minimum at depth five and then climbs back up, with a dashed vertical line at depth five marking where the two curves part company",
        "A line chart with max_depth from 1 to 20 along the bottom and mean absolute error up the side. A purple train line falls smoothly from 54.47 to 0.00. A red test line falls from 56.51 to a minimum of 45.94 at depth 5, then climbs back to 54.53 at depth 20. A dashed pink vertical line at depth 5 is labelled they part company here. A red panel reads: a train MAE of 0.00 is a warning, not a result.",
        b)


# ================================================ ASM.1 test timeline
def fig_asm_1():
    b = []
    b.append(txt(400, 40, "Four papers. Each one tests only its own nine weeks.",
                 24, INK, "middle"))

    terms = [
        ("TERM 1", "Say it in Python", "1", "9", DATA_S, DATA_F, "after W9"),
        ("TERM 2", "Your own toolbox", "10", "18", MODEL_S, MODEL_F, "after W18"),
        ("TERM 3", "Tables & pictures", "19", "27", HUMAN_S, HUMAN_F, "after W27"),
        ("TERM 4", "Models", "28", "36", OK_S, OK_F, "in W36, BEFORE the showcase"),
    ]
    x0, w, gap = 40, 170, 14
    for i, (name, sub, a, z, s, f, when) in enumerate(terms):
        bx = x0 + i * (w + gap)
        b.append(box(bx, 86, w, 96, f, s, 3, 12))
        b.append(txt(bx + w / 2, 112, name, 18, INK, "middle"))
        b.append(txt(bx + w / 2, 134, sub, 12, MUTED, "middle"))
        b.append(txt(bx + w / 2, 162, f"weeks {a}–{z}", 14, INK, "middle"))
        # arrow down to the paper
        b.append(arrow(bx + w / 2, 190, bx + w / 2, 226, s, 2.5))
        b.append(box(bx + 14, 232, w - 28, 74, PAPER, INK, 3, 10))
        b.append(txt(bx + w / 2, 254, "60 min", 14, INK, "middle"))
        b.append(txt(bx + w / 2, 274, "60 marks", 14, INK, "middle"))
        b.append(txt(bx + w / 2, 296, "NO computer", 12, BAD_S, "middle"))
        b.append(txt(bx + w / 2, 326, "give it", 12, MUTED, "middle"))
        b.append(txt(bx + w / 2, 344, when, 12, INK, "middle"))

    b.append(line(40, 74, 760, 74, GRID, 1.5))
    b.append(txt(400, 380, "Term 3 never asks about Week 6. A paper is a mirror, not a verdict.",
                 14, MUTED, "middle"))
    svg("fig-asm-1-test-timeline.svg", "0 0 800 400",
        "Four papers. Each one tests only its own nine weeks.",
        "Four coloured blocks across the page, one per term: Term 1 weeks 1 to 9, Term 2 weeks 10 to 18, Term 3 weeks 19 to 27 and Term 4 weeks 28 to 36. An arrow drops from each into a paper card reading 60 minutes, 60 marks, no computer, and when to give it: after week 9, after week 18, after week 27, and in week 36 before the showcase.",
        b)


# =========================================== ASM.2 partial credit ladder
def fig_asm_2():
    b = []
    b.append(txt(400, 40, "Marking code that nearly works", 24, INK, "middle"))
    b.append(txt(400, 64, "A program is not right or wrong. It is right in parts, and you mark the parts.",
                 14, MUTED, "middle"))

    rungs = [
        ("4 / 4", "It runs, it is correct, and it reports honestly", OK_S, OK_F, tick),
        ("3 / 4", "It runs and is correct, but the number has no label or no row count", OK_S, OK_F, tick),
        ("2 / 4", "One idea right, one missing: off-by-one, wrong axis, print for return", HUMAN_S, HUMAN_F, None),
        ("1 / 4", "Right shape on the page: correct keywords and indenting, wrong logic", HUMAN_S, HUMAN_F, None),
        ("0 / 4", "Blank, or English sentences where code was asked for", BAD_S, BAD_F, cross),
    ]
    for i, (score, what, s, f, mark) in enumerate(rungs):
        ry = 92 + i * 56
        b.append(box(40, ry, 96, 46, f, s, 3, 10))
        b.append(txt(88, ry + 23, score, 18, INK, "middle", central=True))
        b.append(box(148, ry, 612, 46, PAPER, GRID, 1.5, 10))
        b.append(txt(166, ry + 23, what, 14, INK, central=True))
        if mark:
            b.append(mark(736, ry + 23, 14))

    b.append(txt(400, 382, "A wrong answer with a correct trace table has shown you the thinking. Pay for it.",
                 14, MUTED, "middle"))
    svg("fig-asm-2-partial-credit-ladder.svg", "0 0 800 400",
        "Marking code that nearly works",
        "A five-rung ladder of marks out of four. Four out of four, green with a tick: it runs, it is correct and it reports honestly. Three out of four, green: correct but the number has no label or row count. Two out of four, amber: one idea right, one missing. One out of four, amber: the right shape on the page but wrong logic. Zero out of four, red with a cross: blank, or English where code was asked for.",
        b)


# ============================================ PR.1 five project categories
def fig_pr_1():
    b = []
    b.append(txt(400, 40, "Five kinds of project, and when you are ready for each",
                 24, INK, "middle"))

    cats = [
        ("Data\nDetective", "collect it,\nclean it,\nfind something", "after W24", DATA_S, DATA_F),
        ("Build a\nTool", "a program\nsomebody\nactually uses", "after W16", HUMAN_S, HUMAN_F),
        ("Teach a\nMachine", "X, y, split,\nfit, honest\nscore", "after W30", MODEL_S, MODEL_F),
        ("Test It\nHonestly", "break it,\nmeasure it,\nadmit it", "after W33", ACC_S, ACC_F),
        ("Creative\nCode", "make a thing\nthat did not\nexist", "after W12", OK_S, OK_F),
    ]
    x0, w, gap = 40, 140, 5
    for i, (name, what, when, s, f) in enumerate(cats):
        bx = x0 + i * (w + gap)
        b.append(box(bx, 82, w, 210, f, s, 3, 12))
        for j, ln in enumerate(name.split("\n")):
            b.append(txt(bx + w / 2, 112 + j * 24, ln, 18, INK, "middle"))
        b.append(line(bx + 20, 170, bx + w - 20, 170, s, 1.5))
        for j, ln in enumerate(what.split("\n")):
            b.append(txt(bx + w / 2, 196 + j * 20, ln, 12, INK, "middle"))
        b.append(box(bx + 16, 254, w - 32, 30, PAPER, s, 2, 8))
        b.append(txt(bx + w / 2, 269, when, 12, INK, "middle", central=True))

    # the week ruler underneath
    b.append(line(40, 322, 760, 322, GRID, 3))
    for wk, lab in [(1, "W1"), (12, "W12"), (16, "W16"), (24, "W24"), (30, "W30"), (33, "W33"), (36, "W36")]:
        rx = 40 + (wk - 1) / 35 * 720
        b.append(line(rx, 314, rx, 330, MUTED, 1.5))
        b.append(txt(rx, 348, lab, 12, MUTED, "middle"))
    b.append(txt(400, 382, "Pick one because you want to know the answer. Not because it sounds impressive.",
                 14, MUTED, "middle"))
    svg("fig-pr-1-five-categories.svg", "0 0 800 400",
        "Five kinds of project, and when you are ready for each",
        "Five coloured cards side by side. Data Detective, collect it clean it find something, after week 24. Build a Tool, a program somebody actually uses, after week 16. Teach a Machine, X y split fit honest score, after week 30. Test It Honestly, break it measure it admit it, after week 33. Creative Code, make a thing that did not exist, after week 12. A week ruler underneath runs from week 1 to week 36.",
        b)


# ============================================ PR.2 the three tests
def fig_pr_2():
    b = []
    b.append(txt(400, 40, "Three tests every project idea must pass", 24, INK, "middle"))
    b.append(txt(400, 64, "A project that fails one of these cannot be rescued by working harder later.",
                 14, MUTED, "middle"))

    tests = [
        ("1", "THE ANNOYANCE TEST",
         "Name a real moment last month",
         "when this bothered somebody.",
         "\"Dad puts the milk in the wrong bin\"",
         "\"It would be cool to predict stuff\""),
        ("2", "THE 100-ROW TEST",
         "Can you get 100 rows in about two",
         "hours, from where you are?",
         "100 songs from your own playlist",
         "100 classmates' exam marks"),
        ("3", "THE TARGET TEST",
         "Is there ONE column you want to",
         "predict from the others?",
         "minutes (a number) or late (a category)",
         "\"I just want to explore\""),
    ]
    for i, (n, title, q1, q2, good, bad) in enumerate(tests):
        bx = 32 + i * 250
        b.append(box(bx, 92, 236, 250, PANEL, INK, 3, 12))
        b.append(f'<circle cx="{bx + 34}" cy="124" r="18" fill="{ACC_F}" stroke="{ACC_S}" stroke-width="3"/>')
        b.append(txt(bx + 34, 124, n, 18, INK, "middle", central=True))
        b.append(txt(bx + 62, 130, title, 14, INK, weight="600"))
        b.append(txt(bx + 18, 168, q1, 12, INK))
        b.append(txt(bx + 18, 186, q2, 12, INK))
        # good
        b.append(box(bx + 14, 202, 208, 60, OK_F, OK_S, 2, 8))
        b.append(tick(bx + 36, 232, 13))
        b.append(txt(bx + 58, 226, good[:26], 12, INK))
        if len(good) > 26:
            b.append(txt(bx + 58, 244, good[26:], 12, INK))
        # bad
        b.append(box(bx + 14, 270, 208, 60, BAD_F, BAD_S, 2, 8))
        b.append(cross(bx + 36, 300, 13))
        b.append(txt(bx + 58, 294, bad[:26], 12, INK))
        if len(bad) > 26:
            b.append(txt(bx + 58, 312, bad[26:], 12, INK))

    b.append(txt(400, 374, "Fails one? Swap the idea NOW, while it costs you five minutes.",
                 14, MUTED, "middle"))
    svg("fig-pr-2-three-tests.svg", "0 0 800 400",
        "Three tests every project idea must pass",
        "Three cards. Card one, the annoyance test: can you name a real moment last month when this bothered somebody? Good example, Dad puts the milk in the wrong bin. Bad example, it would be cool to predict stuff. Card two, the hundred-row test: can you honestly get 100 rows in about two hours? Good, 100 songs from your own playlist. Bad, 100 classmates' exam marks. Card three, the target test: is there one column you would like to predict? Good, minutes or late. Bad, I just want to explore.",
        b)


if __name__ == "__main__":
    print("writing figures:")
    fig_t1_1(); fig_t1_2()
    fig_t2_1(); fig_t2_2()
    fig_t3_1(); fig_t3_2()
    fig_t4_1(); fig_t4_2()
    fig_asm_1(); fig_asm_2()
    fig_pr_1(); fig_pr_2()
    print("done.")
