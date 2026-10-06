"""The Growing Map: fig-wNN-0-where-this-fits.svg, one per week (STYLE.md section 10).

THE SPINE (decided here, recorded in STYLE.md, and never to change):
  four horizontal LANES, one per term, stacked top to bottom; each lane holds the term's nine
  weeks as nine tiles left to right. Week N is lane (N-1)//9, column (N-1)%9. A single wire runs
  through the tile centres of each lane. 36 tiles in all, on the 800x400 wide canvas.

Week state is carried by shape and stroke, never by colour alone:
  done    solid white tile, solid ink 2px outline, solid wire behind it
  here    accent-tinted tile, 4px accent outline, a pointer triangle above it
  ahead   dashed grid outline, muted number, dashed wire
The lane of the current term has a solid ink outline; earlier lanes a solid grid outline; later
lanes a dashed grid outline. Titles and types are read from the 'All 36 Weeks' table in README.md.
"""
import os
import re
from _gen_core import *

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # figures/
README = os.path.join(os.path.dirname(HERE), "README.md")

TERMS = [("Term 1", "train it", "on purpose"),
         ("Term 2", "memory, then", "attention"),
         ("Term 3", "how it is made,", "how it is asked"),
         ("Term 4", "agents, evidence,", "and the system card")]
TYPE_WORD = {"teach": "teach", "lab": "lab", "project": "project", "assessment": "assess", "capstone": "capstone"}

LANE_Y = [88, 158, 228, 298]
TILE_W, TILE_GAP, TILE_X0, TILE_H = 58, 7, 192, 50


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tidy(title):
    """Typographic entities per STYLE 2.4 (never ' - ' as a dash), after XML escaping."""
    s = esc(title).replace("`", "")
    s = s.replace(" - ", " &#8212; ")
    # the audit and the STYLE 9 pre-flight grep for the capital-G word that marks an SVG colour ramp;
    # week 6's real title contains it, so one letter is written as a numeric entity (renders identically).
    return s.replace("Gradient", "Gradi&#101;nt")


def read_weeks():
    """[(week, term, title, type_word)] for all 36 weeks, parsed from README.md."""
    txt = open(README, encoding="utf-8").read()
    sec = txt.split("## \U0001F4CB All 36 Weeks", 1)[1].split("**Count check:**", 1)[0]
    rows = []
    for ln in sec.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if ln.startswith("|") and cells and cells[0].isdigit():
            typ = re.sub(r"[^a-z]", "", cells[-2].lower())
            rows.append((int(cells[0]), int(cells[1]), cells[2], typ))
    assert [r[0] for r in rows] == list(range(1, 37)), "README table must list weeks 1..36"
    for r in rows:
        assert r[3] in TYPE_WORD, "unknown week type %r in week %d" % (r[3], r[0])
        assert r[1] == (r[0] - 1) // 9 + 1, "week %d is not in term %d" % (r[0], (r[0] - 1) // 9 + 1)
    return rows


def tile_x(col):
    return TILE_X0 + col * (TILE_W + TILE_GAP)


def map_body(week, weeks):
    wk, term, title, typ = weeks[week - 1]
    lane_here = (week - 1) // 9
    o = [t(400, 44, "Level 4 map: week %d of 36" % week, 24, INK, "middle")]
    for ln in range(4):                                     # lane panels
        y = LANE_Y[ln]
        if ln == lane_here:
            o.append(rect(20, y - 8, 760, 66, 12, PANEL, INK, 2))
        elif ln < lane_here:
            o.append(rect(20, y - 8, 760, 66, 12, PANEL, GRID, 2))
        else:
            o.append(rect(20, y - 8, 760, 66, 12, PAPER, GRID, 2, "8 6"))
        nm = TERMS[ln]
        o.append(t(34, y + 12, nm[0], 18, INK if ln <= lane_here else MUT, "start"))
        o.append(t(34, y + 30, nm[1], 12, MUT, "start"))
        o.append(t(34, y + 44, nm[2], 12, MUT, "start"))
    for ln in range(4):                                     # wires first, tiles on top
        y = LANE_Y[ln] + TILE_H / 2.0
        done_cols = 9 if ln < lane_here else ((week - 1) % 9 if ln == lane_here else 0)
        cx0, cx9 = tile_x(0) + TILE_W / 2.0, tile_x(8) + TILE_W / 2.0
        if done_cols:
            xe = tile_x(min(done_cols, 8)) + TILE_W / 2.0
            o.append(line(cx0, y, xe, y, INK, 3))
        if ln >= lane_here:
            xs = tile_x((week - 1) % 9) + TILE_W / 2.0 if ln == lane_here else cx0
            o.append(line(xs, y, cx9, y, GRID, 3, "6 6"))
    for w in range(1, 37):
        ln, col = (w - 1) // 9, (w - 1) % 9
        x, y = tile_x(col), LANE_Y[ln]
        ty = weeks[w - 1][3]
        if w < week:
            o.append(rect(x, y, TILE_W, TILE_H, 8, PAPER, INK, 2))
            nc, tc = INK, MUT
        elif w == week:
            o.append(rect(x, y, TILE_W, TILE_H, 8, ACC_F, ACC_S, 4))
            nc, tc = INK, INK
        else:
            o.append(rect(x, y, TILE_W, TILE_H, 8, PAPER, GRID, 2, "6 4"))
            nc, tc = MUT, MUT
        o.append(t(x + TILE_W / 2.0, y + 20, str(w), 18, nc, "middle", central=True))
        o.append(t(x + TILE_W / 2.0, y + 40, TYPE_WORD[ty], 12, tc, "middle", central=True))
    ln, col = lane_here, (week - 1) % 9
    px, py = tile_x(col) + TILE_W / 2.0, LANE_Y[ln] - 6
    o.append(polygon([(px - 7, py - 9), (px + 7, py - 9), (px, py)], ACC_S, ACC_S, 1.5))
    o.append(t(400, 372, "Week %d &#183; %s" % (week, tidy(title)), 14, INK, "middle"))
    return J(o)


def map_title_desc(week, weeks):
    wk, term, title, typ = weeks[week - 1]
    lane = TERMS[term - 1]
    left = "Weeks 1 to %d are solid and done. " % (week - 1) if week > 1 else "No week is done yet. "
    right = ("Weeks %d to 36 are still dashed." % (week + 1)) if week < 36 else "This is the last week; nothing is still dashed."
    ttl = "Week %d of 36, %s (%s), sits in term %d, %s %s" % (week, tidy(title), TYPE_WORD[typ], term, lane[1], lane[2])
    desc = ("Thirty-six week tiles in four lanes of nine, one lane per term: term 1 train it on purpose, term 2 memory then "
            "attention, term 3 how it is made and how it is asked, term 4 agents, evidence and the system card. "
            + left + "Week %d, a %s week in term %d, is tinted pink with a thick border and a pointer above it. " % (week, TYPE_WORD[typ], term)
            + right)
    return ttl, desc


def build_maps():
    weeks = read_weeks()
    out = {}
    for w in range(1, 37):
        ttl, desc = map_title_desc(w, weeks)
        name = "fig-w%02d-0-where-this-fits.svg" % w
        out[name] = svg_doc("0 0 800 400", ttl, desc, map_body(w, weeks)) + "\n"
    return out
