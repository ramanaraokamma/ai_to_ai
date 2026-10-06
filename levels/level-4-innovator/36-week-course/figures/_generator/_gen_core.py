"""Core palette, drawing helpers and the motif registry for Level 4 (Innovator) figures.

Palette, fonts, stroke widths and canvas rules are the Level 1-3 values, unchanged
(STYLE.md section 1). Everything here is Level 4's own code, written fresh: the helpers
add what Level 4 needs (series markers, pale bands, three-tint heatmap cells, the
stand-in frame and the quoted box).

Dependency order:  _gen_core -> _gen_data -> _gen_motifs -> _gen_pat -> _gen_map -> _gen_emit
"""
import math

FS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
FM = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

DATA_S, DATA_F = "#1F6FB2", "#D9EAF9"
MODEL_S, MODEL_F = "#6D28D9", "#DBCEF3"
HUMAN_S, HUMAN_F = "#845F00", "#E8C671"
OK_S, OK_F = "#1B7A4B", "#E2F7ED"
BAD_S, BAD_F = "#CC2B1D", "#F6AEA6"
ACC_S, ACC_F = "#C42B8C", "#F4D5E9"
INK, PAPER, MUT, GRID, PANEL = "#14202B", "#FFFFFF", "#55636F", "#C7CDD4", "#F5F8FA"

STAND_IN = "stand-in, not a model"

# ------------------------------------------------------------------ HELPERS


def f2(v):
    """Compact number for coordinates."""
    s = "%.1f" % v
    return s[:-2] if s.endswith(".0") else s


def t(x, y, s, size=14, fill=MUT, anchor=None, mono=False, central=False,
      weight=None, extra=""):
    ff = FM if mono else FS
    a = ' text-anchor="%s"' % anchor if anchor else ""
    c = ' dominant-baseline="central"' if central else ""
    w = ' font-weight="%s"' % weight if weight else ""
    e = (" " + extra) if extra else ""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s"%s%s%s%s>%s</text>'
            % (f2(x) if not isinstance(x, str) else x, f2(y) if not isinstance(y, str) else y,
               ff, size, fill, a, c, w, e, s))


def trot(x, y, s, size=12, fill=MUT, anchor="middle"):
    """Axis title rotated -90 degrees about its own anchor point."""
    return t(x, y, s, size, fill, anchor, extra='transform="rotate(-90 %s %s)"' % (f2(x), f2(y)))


def head(x, y, angle=0, color=INK, w=3):
    return ('<polyline points="-13,-8 0,0 -13,8" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" transform="translate(%s %s) rotate(%s)"/>'
            % (color, w, f2(x), f2(y), angle))


def arrow(x1, y1, x2, y2, color=INK, w=3, dash=None):
    ang = round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 1)
    ang = int(ang) if ang == int(ang) else ang
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>\n  %s'
            % (f2(x1), f2(y1), f2(x2), f2(y2), color, w, d, head(x2, y2, ang, color, w)))


def rect(x, y, w, h, rx, fill, stroke, sw=3, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s" stroke-linejoin="round"%s/>'
            % (f2(x), f2(y), f2(w), f2(h), rx, fill, stroke, sw, d))


def sq(x, y, w, h, fill, stroke, sw=2):
    """A grid cell: square corners, because cells butt up against each other."""
    return ('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (f2(x), f2(y), f2(w), f2(h), fill, stroke, sw))


def line(x1, y1, x2, y2, color=INK, w=2, dash=None, cap=True):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    c = ' stroke-linecap="round"' if cap else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
            % (f2(x1), f2(y1), f2(x2), f2(y2), color, w, d, c))


def circ(cx, cy, r, fill, stroke, sw=3):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (f2(cx), f2(cy), r, fill, stroke, sw))


def poly(points, fill="none", stroke=INK, sw=3, dash=None):
    """Open or filled polyline. points: string 'x,y x,y' or list of (x, y)."""
    if not isinstance(points, str):
        points = " ".join("%s,%s" % (f2(x), f2(y)) for x, y in points)
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round"%s/>' % (points, fill, stroke, sw, d))


def polygon(points, fill="none", stroke=GRID, sw=1.5):
    s = " ".join("%s,%s" % (f2(x), f2(y)) for x, y in points)
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"/>' % (s, fill, stroke, sw))


def path(d, fill="none", stroke=INK, sw=3, dash=None):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s '
            'stroke-linecap="round" stroke-linejoin="round"/>' % (d, fill, stroke, sw, ds))


def mark(kind, cx, cy, r=6, stroke=DATA_S, fill=PAPER, sw=2):
    """Series end marker. circle / square / triangle / diamond: a SHAPE, never colour alone."""
    if kind == "circle":
        return circ(cx, cy, r, fill, stroke, sw)
    if kind == "square":
        return rect(cx - r, cy - r, 2 * r, 2 * r, 2, fill, stroke, sw)
    if kind == "triangle":
        return polygon([(cx, cy - r - 1), (cx + r + 1, cy + r), (cx - r - 1, cy + r)], fill, stroke, sw)
    return polygon([(cx, cy - r - 2), (cx + r + 2, cy), (cx, cy + r + 2), (cx - r - 2, cy)], fill, stroke, sw)


def chip(x, y, w, txt, stroke=DATA_S, fill=PAPER, size=12, h=26, mono=True, color=INK, dash=None):
    """A small labelled chip: a shape annotation '(3, 2)' (mono) or a words chip (mono=False)."""
    return "%s\n  %s" % (rect(x, y, w, h, 6, fill, stroke, 2, dash),
                         t(x + w / 2.0, y + h / 2.0, txt, size, color, "middle", mono=mono, central=True))


def shape_chip(x, y, txt, stroke=DATA_S):
    """Mono shape annotation, width sized to its text."""
    w = max(34, int(len(txt.replace("&#8722;", "-")) * 12 * 0.6) + 14)
    return chip(x, y, w, txt, stroke)


def ring_num(cx, cy, n, stroke=ACC_S, fill=ACC_F):
    """Ringed number: matches two parts of a figure by number, not by leader line (2.8)."""
    return circ(cx, cy, 11, fill, stroke, 2) + "\n  " + t(cx, cy, str(n), 12, INK, "middle", central=True, weight=None)


def bracket(x1, x2, y, depth=8, color=MUT, down=False):
    d = depth if down else -depth
    return path("M%s %s V%s H%s V%s" % (f2(x1), f2(y), f2(y + d), f2(x2), f2(y)), "none", color, 1.5)


def badge_check(x, y, s=0.28):
    return ('<g transform="translate(%s,%s) scale(%s)">\n  %s\n  %s\n  </g>'
            % (f2(x), f2(y), s, circ(50, 50, 34, OK_F, OK_S, 3),
               poly("34,52 45,64 68,38", "none", OK_S, 6)))


def badge_cross(x, y, s=0.28):
    return ('<g transform="translate(%s,%s) scale(%s)">\n  %s\n  <g stroke="%s" stroke-width="6" '
            'stroke-linecap="round">\n    %s\n    %s\n  </g>\n  </g>'
            % (f2(x), f2(y), s, circ(50, 50, 34, BAD_F, BAD_S, 3), BAD_S,
               line(38, 38, 62, 62, BAD_S, 6), line(62, 38, 38, 62, BAD_S, 6)))


def tick(cx, cy, r=9, color=OK_S):
    """Text-free tick, drawn at its real size (no scale)."""
    return poly([(cx - r * 0.7, cy), (cx - r * 0.2, cy + r * 0.55), (cx + r * 0.8, cy - r * 0.6)], "none", color, 3)


def cross(cx, cy, r=7, color=BAD_S):
    return (poly([(cx - r, cy - r), (cx + r, cy + r)], "none", color, 3) + "\n  " +
            poly([(cx - r, cy + r), (cx + r, cy - r)], "none", color, 3))


def stand_in_frame(x, y, w, h, label_x=None, label_y=None):
    """Dashed model-stroke outline on a panel fill plus the exact chip words (2.5)."""
    cx = (x + w / 2.0) if label_x is None else label_x
    ty = (y - 13) if label_y is None else label_y
    cw = 172
    return "%s\n  %s" % (rect(x, y, w, h, 12, PANEL, MODEL_S, 2, "6 4"),
                         chip(cx - cw / 2.0, ty - 13, cw, STAND_IN, MODEL_S, PANEL, 12, 26, mono=False))


def quoted_box(x, y, w, h, txt, size=12):
    """A quoted-not-measured number: muted text, dashed grid outline, 'quoted:' prefix (2.6)."""
    return "%s\n  %s" % (rect(x, y, w, h, 8, PAPER, GRID, 2, "6 4"),
                         t(x + w / 2.0, y + h / 2.0, "quoted: " + txt, size, MUT, "middle", central=True))


def cell_tint(v, row_max, cut=0.10):
    """Three discrete tints (2.9): accent = largest in the row, data = at least cut, panel = below."""
    if abs(v - row_max) < 1e-9:
        return ACC_F, ACC_S, 3
    if v >= cut:
        return DATA_F, GRID, 2
    return PANEL, GRID, 2


def terminal(x, y, w, lines, size=12, lh=18, hi=None, pad=10):
    """A dark-on-panel terminal panel (<=5 lines; section 1.9). hi = index of the highlighted line."""
    h = pad * 2 + lh * len(lines)
    out = [rect(x, y, w, h, 8, PANEL, INK, 2)]
    for i, s in enumerate(lines):
        yy = y + pad + lh * (i + 0.5)
        if hi is not None and i == hi:
            out.append(rect(x + 4, yy - lh / 2.0 + 1, w - 8, lh - 2, 4, ACC_F, ACC_S, 2))
        out.append(t(x + 10, yy, s, size, INK, mono=True, central=True,
                     weight="600" if hi == i else None))
    return "\n  ".join(out)


# ------------------------------------------------------------------ REGISTRY
MOTIFS = []


def M(mid, title, desc, vb, body, note):
    MOTIFS.append(dict(id=mid, title=title, desc=desc, vb=vb,
                       body=body.strip("\n"), note=note))


def J(*parts):
    """Join body fragments, indenting each to two spaces."""
    out = []
    for p in parts:
        if isinstance(p, (list, tuple)):
            out.extend("  " + q for q in p)
        else:
            out.append("  " + p)
    return "\n".join(out)


def svg_doc(vb, title, desc, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img">\n'
            '  <title>%s</title>\n  <desc>%s</desc>\n%s\n</svg>' % (vb, title, desc, body))
