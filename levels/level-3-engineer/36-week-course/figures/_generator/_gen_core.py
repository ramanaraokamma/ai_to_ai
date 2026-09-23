"""Core palette, helpers and the motif registry for Level 3 (Engineer) figures.

Everything above the HELPERS line is inherited VERBATIM from Level 2, which
inherited it from Level 1. Do not change a value here: three years of figures
depend on these exact numbers.
"""

FS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
FM = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

DATA_S, DATA_F = "#1F6FB2", "#D9EAF9"
MODEL_S, MODEL_F = "#6D28D9", "#DBCEF3"
HUMAN_S, HUMAN_F = "#845F00", "#E8C671"
OK_S, OK_F = "#1B7A4B", "#E2F7ED"
BAD_S, BAD_F = "#CC2B1D", "#F6AEA6"
ACC_S, ACC_F = "#C42B8C", "#F4D5E9"
INK, PAPER, MUT, GRID, PANEL = "#14202B", "#FFFFFF", "#55636F", "#C7CDD4", "#F5F8FA"

# ------------------------------------------------------------------ HELPERS


def t(x, y, s, size=14, fill=MUT, anchor=None, mono=False, central=False,
      weight=None, extra=""):
    ff = FM if mono else FS
    a = ' text-anchor="%s"' % anchor if anchor else ""
    c = ' dominant-baseline="central"' if central else ""
    w = ' font-weight="%s"' % weight if weight else ""
    e = (" " + extra) if extra else ""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s"%s%s%s%s>%s</text>'
            % (x, y, ff, size, fill, a, c, w, e, s))


def trot(x, y, s, size=12, fill=MUT, anchor=None):
    """Text rotated -90 degrees about its own anchor point."""
    return t(x, y, s, size, fill, anchor, extra='transform="rotate(-90 %s %s)"' % (x, y))


def head(x, y, angle=0, color=INK, w=3):
    return ('<polyline points="-13,-8 0,0 -13,8" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" transform="translate(%s %s) rotate(%s)"/>'
            % (color, w, x, y, angle))


def arrow(x1, y1, x2, y2, color=INK, w=3, dash=None):
    import math
    ang = round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 1)
    ang = int(ang) if ang == int(ang) else ang
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>\n  %s'
            % (x1, y1, x2, y2, color, w, d, head(x2, y2, ang, color, w)))


def rect(x, y, w, h, rx, fill, stroke, sw=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s" stroke-linejoin="round"/>' % (x, y, w, h, rx, fill, stroke, sw))


def sq(x, y, w, h, fill, stroke, sw=2):
    """A grid cell: square corners, because cells butt up against each other."""
    return ('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, fill, stroke, sw))


def line(x1, y1, x2, y2, color=INK, w=2, dash=None, cap=True):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    c = ' stroke-linecap="round"' if cap else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
            % (x1, y1, x2, y2, color, w, d, c))


def circ(cx, cy, r, fill, stroke, sw=3):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (cx, cy, r, fill, stroke, sw))


def poly(points, fill="none", stroke=INK, sw=3):
    return ('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round"/>' % (points, fill, stroke, sw))


def path(d, fill="none", stroke=INK, sw=3, dash=None):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s '
            'stroke-linecap="round" stroke-linejoin="round"/>' % (d, fill, stroke, sw, ds))


def dot(cx, cy, r=5, fill=DATA_S):
    """A data point: filled mark with a paper halo so overlaps stay readable."""
    return circ(cx, cy, r, fill, PAPER, 1.5)


def tri(cx, cy, r=6, fill=OK_S):
    """A data point of the second class: a TRIANGLE, never just another colour."""
    return ('<path d="M%s %s L%s %s L%s %s Z" fill="%s" stroke="%s" stroke-width="1.5" '
            'stroke-linejoin="round"/>' % (cx, cy - r, cx + r, cy + r * 0.9,
                                           cx - r, cy + r * 0.9, fill, PAPER))


def chip(x, y, w, txt, stroke=DATA_S, fill=PAPER, size=12, h=26):
    """A mono shape annotation pinned to a block: 'shape (3, 4)'."""
    return "%s\n  %s" % (rect(x, y, w, h, 6, fill, stroke, 2),
                         t(x + w / 2.0, y + h / 2.0, txt, size, INK, "middle",
                           mono=True, central=True))


def bracket(x1, x2, y, depth=8, color=MUT, down=False):
    """A span bracket above (default) or below a run of cells."""
    if down:
        return path("M%s %s V%s H%s V%s" % (x1, y, y + depth, x2, y), "none", color, 1.5)
    return path("M%s %s V%s H%s V%s" % (x1, y, y - depth, x2, y), "none", color, 1.5)


def badge_check(x, y, s=0.28):
    return ('<g transform="translate(%s,%s) scale(%s)">\n  %s\n  %s\n  </g>'
            % (x, y, s, circ(50, 50, 34, OK_F, OK_S, 3),
               poly("34,52 45,64 68,38", "none", OK_S, 6)))


def badge_cross(x, y, s=0.28):
    return ('<g transform="translate(%s,%s) scale(%s)">\n  %s\n  <g stroke="%s" stroke-width="6" '
            'stroke-linecap="round">\n    %s\n    %s\n  </g>\n  </g>'
            % (x, y, s, circ(50, 50, 34, BAD_F, BAD_S, 3), BAD_S,
               line(38, 38, 62, 62, BAD_S, 6), line(62, 38, 38, 62, BAD_S, 6)))


def centroid(cx, cy, r=8):
    """A k-means centroid: a ringed cross-hair. A SHAPE, so it survives greyscale."""
    return "\n  ".join([circ(cx, cy, r, PAPER, ACC_S, 3),
                        line(cx - r + 1, cy, cx + r - 1, cy, ACC_S, 2),
                        line(cx, cy - r + 1, cx, cy + r - 1, ACC_S, 2)])


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
