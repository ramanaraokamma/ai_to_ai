"""Geometry + rule audit: bounds, effective font size, banned constructs, label collisions."""
import math
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
BANNED = re.compile(r'<image|href="http|@font-face|<filter|feGaussianBlur|feDropShadow|<foreignObject|<script|Gradient')


def parse_tf(s):
    """Return (sx, tx, ty) for the transforms we actually use."""
    sx, tx, ty, rot = 1.0, 0.0, 0.0, False
    for name, args in re.findall(r'(translate|scale|rotate)\(([^)]*)\)', s or ""):
        v = [float(a) for a in re.split(r'[ ,]+', args.strip()) if a]
        if name == "translate":
            tx += v[0]
            ty += v[1] if len(v) > 1 else 0.0
        elif name == "scale":
            sx *= v[0]
        else:
            rot = True
    return sx, tx, ty, rot


def path_points(d):
    pts, cx, cy = [], 0.0, 0.0
    for cmd, args in re.findall(r'([MLHVQACZmlhvqacz])([^MLHVQACZmlhvqacz]*)', d):
        v = [float(a) for a in re.findall(r'-?\d*\.?\d+', args)]
        u = cmd.upper()
        if u in "ML":
            for i in range(0, len(v) - 1, 2):
                cx, cy = v[i], v[i + 1]
                pts.append((cx, cy))
        elif u == "H":
            for a in v:
                cx = a
                pts.append((cx, cy))
        elif u == "V":
            for a in v:
                cy = a
                pts.append((cx, cy))
        elif u == "Q":
            for i in range(0, len(v) - 3, 4):
                pts.append((v[i], v[i + 1]))
                cx, cy = v[i + 2], v[i + 3]
                pts.append((cx, cy))
        elif u == "C":
            for i in range(0, len(v) - 5, 6):
                pts += [(v[i], v[i + 1]), (v[i + 2], v[i + 3])]
                cx, cy = v[i + 4], v[i + 5]
                pts.append((cx, cy))
        elif u == "A":
            for i in range(0, len(v) - 6, 7):
                cx, cy = v[i + 5], v[i + 6]
                pts.append((cx, cy))
    return pts


def walk(el, sx=1.0, tx=0.0, ty=0.0, rot=False, out=None, texts=None):
    out = [] if out is None else out
    texts = [] if texts is None else texts
    s2, dx, dy, r2 = parse_tf(el.get("transform"))
    sx, tx, ty, rot = sx * s2, tx + dx * sx, ty + dy * sx, rot or r2
    tag = el.tag.replace(NS, "")

    def pt(x, y):
        out.append((tx + x * sx, ty + y * sx))

    g = lambda k, d=0.0: float(el.get(k, d))
    if tag == "rect":
        pt(g("x"), g("y"))
        pt(g("x") + g("width"), g("y") + g("height"))
    elif tag == "circle":
        pt(g("cx") - g("r"), g("cy") - g("r"))
        pt(g("cx") + g("r"), g("cy") + g("r"))
    elif tag == "line":
        pt(g("x1"), g("y1"))
        pt(g("x2"), g("y2"))
    elif tag in ("polyline", "polygon"):
        v = [float(a) for a in re.findall(r'-?\d*\.?\d+', el.get("points", ""))]
        for i in range(0, len(v) - 1, 2):
            pt(v[i], v[i + 1])
    elif tag == "path":
        for x, y in path_points(el.get("d", "")):
            pt(x, y)
    elif tag == "text":
        fs = float(el.get("font-size", 14))
        mono = "mono" in (el.get("font-family") or "")
        n = len(re.sub(r'&[a-z]+;|&#\d+;', "X", el.text or ""))
        w = n * fs * (0.60 if mono else 0.58)
        x, y, a = g("x"), g("y"), el.get("text-anchor", "start")
        x0 = x if a == "start" else (x - w / 2 if a == "middle" else x - w)
        ry = rot or r2 or "rotate" in (el.get("transform") or "")
        if not ry:
            pt(x0, y - fs * 0.78)
            pt(x0 + w, y + fs * 0.24)
            texts.append((tx + x0 * sx, ty + y * sx, w * sx, fs * sx, el.text or ""))
        else:
            pt(x - fs, y - fs)
            pt(x + fs, y + fs)
            texts.append((None, None, 0, fs * sx, el.text or ""))
    for c in el:
        walk(c, sx, tx, ty, rot, out, texts)
    return out, texts


def audit(name, svg_text, pad, vb=None):
    bad = []
    if BANNED.search(svg_text):
        bad.append("banned construct")
    root = ET.fromstring(svg_text)
    vb = vb or root.get("viewBox")
    _, _, W, H = [float(v) for v in vb.split()]
    pts, texts = walk(root)
    if pts:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if min(xs) < pad - 0.6 or min(ys) < pad - 0.6 or max(xs) > W - pad + 0.6 or max(ys) > H - pad + 0.6:
            bad.append("bounds x %.1f..%.1f y %.1f..%.1f exceed %gx%g pad %g"
                       % (min(xs), max(xs), min(ys), max(ys), W, H, pad))
    for _, _, _, fs, s in texts:
        if fs < 11.99:
            bad.append("font %.1fpx under floor: %r" % (fs, s[:28]))
    rows = {}
    for x, y, w, fs, s in texts:
        if x is None:
            continue
        rows.setdefault(round(y, 1), []).append((x, x + w, s))
    for y, items in rows.items():
        items.sort()
        for (a0, a1, s1), (b0, b1, s2) in zip(items, items[1:]):
            if b0 < a1 - 1.5:
                bad.append("labels overlap at y=%s: %r / %r" % (y, s1[:18], s2[:18]))
    return bad


if __name__ == "__main__":
    from _gen_pat import PATTERNS, EXAMPLES
    from _gen_emit import pattern_svg
    from _gen_core import MOTIFS
    fails = 0
    for m in MOTIFS:
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img"><title>t</title>'
               '<desc>d</desc>%s</svg>' % (m["vb"], m["body"]))
        for b in audit(m["id"], svg, 0, m["vb"]):
            print("MOTIF  %-22s %s" % (m["id"], b))
            fails += 1
    for p in PATTERNS:
        for b in audit(p["id"], pattern_svg(p), 20):
            print("PAT    %-22s %s" % (p["id"], b))
            fails += 1
    for eid, et, es in EXAMPLES:
        for b in audit(eid, es, 20):
            print("EX     %-22s %s" % (eid, b))
            fails += 1
    print("--- %d finding(s)" % fails)
