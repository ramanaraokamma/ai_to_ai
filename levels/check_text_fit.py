#!/usr/bin/env python3
"""check_text_fit.py — does every <text> in a figure fit where it is drawn?

The figure audits (`_gen_audit.py`) check bounds and label collisions from character-count estimates.
This tool measures each <text> with real glyph metrics (PIL + macOS Helvetica / Menlo) and flags:

  OVERFLOW-VIEWBOX   text extends past the viewBox
  OVERFLOW-BOX       text starts inside a box (rect) but spills past its edge
  OVERLAP            two text boxes overlap noticeably
  ROTATED            a rotated text (only checked against the viewBox)

Widths are multiplied by SAFETY (default 1.05) because the page uses the reader's system-ui font, which is
a little wider than Helvetica. Transforms (translate / scale / rotate) are applied. Nothing is rendered.

Usage:  python3 levels/check_text_fit.py [--safety 1.08] [--summary] [PATH ...]
        PATH may be an .svg, a directory, or omitted (all four levels' figures).
Exit status 1 if any finding.
"""
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import ImageFont

NS = "{http://www.w3.org/2000/svg}"
ROOT = Path(__file__).resolve().parent
SAFETY = 1.05
TOL = 3.0

# Reviewed false positives: (figure file name, kind) -> why the text is fine as drawn
ALLOW = {
    ("fig-w29-3-false-stamp.svg", "OVERLAP"): "the rotated FALSE stamp is deliberately drawn over the words",
    ("fig-w20-4-item-plain-number-versus-whole-history.svg", "OVERFLOW-BOX"): "text sits on the front card; checker measured the back card",
    ("fig-w19-9-blank-axis-to-label.svg", "OVERFLOW-BOX"): "circular badge centred on the cell edge, like A, B, D",
}
_fonts = {}
BAD_TRANSFORMS = []
INHERITED = ("font-size", "font-family", "font-weight", "text-anchor", "dominant-baseline")


def font(bold, mono, size):
    key = (bold, mono, size)
    if key not in _fonts:
        if mono:
            path, idx = "/System/Library/Fonts/Menlo.ttc", 1 if bold else 0
        else:
            path, idx = "/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0
        _fonts[key] = ImageFont.truetype(path, max(1, int(round(size * 8))), index=idx)  # 8x for sub-pixel accuracy
    return _fonts[key]


def text_width(s, size, bold, mono):
    return font(bold, mono, size).getlength(s) / 8.0


# ---- affine transforms: (a,b,c,d,e,f)
I = (1, 0, 0, 1, 0, 0)


def mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)


def parse_transform(s):
    m = I
    for name, args in re.findall(r"(\w+)\(([^)]*)\)", s or ""):
        v = [float(x) for x in re.split(r"[\s,]+", args.strip()) if x]
        if (name == "rotate" and len(v) not in (1, 3)) or (name == "translate" and len(v) not in (1, 2)) \
                or (name == "scale" and len(v) not in (1, 2)):
            BAD_TRANSFORMS.append(f"{name}({args})")
            continue
        if name == "translate":
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            r = math.radians(v[0])
            c, s_ = math.cos(r), math.sin(r)
            t = (c, s_, -s_, c, 0, 0)
            if len(v) == 3:
                t = mul(mul((1, 0, 0, 1, v[1], v[2]), t), (1, 0, 0, 1, -v[1], -v[2]))
        else:
            continue
        m = mul(m, t)
    return m


def apply(m, x, y):
    return m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]


def bbox_of(m, x0, y0, x1, y1):
    pts = [apply(m, x, y) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def num(el, k, default=0.0):
    try:
        return float(el.get(k, default))
    except ValueError:
        return default


def collect(root):
    """Return (rects, texts) in root coordinates."""
    rects, texts = [], []

    def walk(el, m, inh):
        for ch in el:
            tag = ch.tag.replace(NS, "")
            cm = mul(m, parse_transform(ch.get("transform")))
            ci = dict(inh)
            for k in INHERITED:
                if ch.get(k) is not None:
                    ci[k] = ch.get(k)
            if tag == "rect":
                x, y, w, h = num(ch, "x"), num(ch, "y"), num(ch, "width"), num(ch, "height")
                sw = num(ch, "stroke-width", 0) if ch.get("stroke", "none") != "none" else 0
                rects.append(bbox_of(cm, x - sw / 2, y - sw / 2, x + w + sw / 2, y + h + sw / 2))
            elif tag == "text":
                texts.append(measure(ch, cm, ci))
            elif tag in ("g", "svg", "a"):
                walk(ch, cm, ci)

    walk(root, I, {})
    return rects, [t for t in texts if t]


def measure(el, m, inh):
    def attr(k, d=""):
        return el.get(k) if el.get(k) is not None else inh.get(k, d)

    s = "".join(el.itertext()).strip()
    s = re.sub(r"\s+", " ", s)
    if not s:
        return None
    try:
        size = float(attr("font-size", 16))
    except ValueError:
        size = 16.0
    ff = attr("font-family")
    mono = "mono" in ff.lower() or "menlo" in ff.lower()
    bold = attr("font-weight") in ("600", "700", "bold", "800", "900")
    w = text_width(s, size, bold, mono) * SAFETY
    x, y = num(el, "x"), num(el, "y")
    anchor = attr("text-anchor", "start")
    x0 = x - w if anchor == "end" else x - w / 2 if anchor == "middle" else x
    if attr("dominant-baseline") in ("central", "middle"):
        top, bot = y - size * 0.5, y + size * 0.5
    else:
        top, bot = y - size * 0.78, y + size * 0.22
    rot = abs(m[1]) > 1e-6 or abs(m[2]) > 1e-6
    return dict(s=s, size=size, anchor=(x, y), box=bbox_of(m, x0, top, x0 + w, bot),
                anchor_root=apply(m, x, y), rot=rot)


def check(path):
    out = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [("PARSE", str(e))]
    vb = [float(v) for v in root.get("viewBox", "0 0 0 0").replace(",", " ").split()]
    if len(vb) != 4:
        return [("PARSE", "no viewBox")]
    X0, Y0, W, H = vb
    del BAD_TRANSFORMS[:]
    rects, texts = collect(root)
    for b in sorted(set(BAD_TRANSFORMS)):
        out.append(("BAD-TRANSFORM", f"{b} is invalid, so browsers ignore it"))
    area_vb = W * H
    for t in texts:
        bx0, by0, bx1, by1 = t["box"]
        label = f'"{t["s"][:50]}" ({t["size"]:g}px)'
        if bx0 < X0 - TOL or by0 < Y0 - TOL or bx1 > X0 + W + TOL or by1 > Y0 + H + TOL:
            out.append(("OVERFLOW-VIEWBOX", f"{label} spans x {bx0:.0f}..{bx1:.0f}, y {by0:.0f}..{by1:.0f} in {W:g}x{H:g}"))
            continue
        if t["rot"]:
            continue
        ax, ay = t["anchor_root"]
        # the smallest rect that contains the anchor point (a box this text belongs to)
        best = None
        for r in rects:
            rx0, ry0, rx1, ry1 = r
            a = (rx1 - rx0) * (ry1 - ry0)
            if a >= 0.85 * area_vb or a <= 0:
                continue
            tw = bx1 - bx0
            if (rx1 - rx0) >= 40 and (ry1 - ry0) >= 16 and rx0 <= ax <= rx1 \
                    and ry0 - 2 <= by0 and by1 <= ry1 + 2 and tw <= 1.6 * (rx1 - rx0):
                if best is None or a < best[0]:
                    best = (a, r)
        if best:
            rx0, ry0, rx1, ry1 = best[1]
            if bx0 < rx0 - TOL or bx1 > rx1 + TOL:
                side = "left" if bx0 < rx0 - TOL else "right"
                over = (rx0 - bx0) if side == "left" else (bx1 - rx1)
                out.append(("OVERFLOW-BOX", f"{label} spills {over:.0f}px past the {side} edge of its box "
                                            f"(text {bx0:.0f}..{bx1:.0f}, box {rx0:.0f}..{rx1:.0f})"))
    # text-text overlap
    for i in range(len(texts)):
        a = texts[i]
        for j in range(i + 1, len(texts)):
            b = texts[j]
            ax0, ay0, ax1, ay1 = a["box"]
            bx0, by0, bx1, by1 = b["box"]
            ox, oy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
            if ox > 3 and oy > min(a["size"], b["size"]) * 0.45 and a["s"] != b["s"]:
                out.append(("OVERLAP", f'"{a["s"][:30]}" with "{b["s"][:30]}" ({ox:.0f}x{oy:.0f}px)'))
    return out


def figures(args):
    if not args:
        args = [str(ROOT)]
    files = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            files += sorted(f for f in p.rglob("fig-*.svg") if "_generator" not in f.parts)
        else:
            files.append(p)
    return files


def main(argv):
    global SAFETY
    summary = False
    while argv and argv[0].startswith("--"):
        if argv[0] == "--safety":
            SAFETY, argv = float(argv[1]), argv[2:]
        elif argv[0] == "--summary":
            summary, argv = True, argv[1:]
        else:
            print(__doc__)
            return 2
    total, bad = 0, 0
    kinds = {}
    for f in figures(argv):
        found = [(k, m) for k, m in check(f) if (Path(f).name, k) not in ALLOW]
        total += 1
        if found:
            bad += 1
            for k, m in found:
                kinds[k] = kinds.get(k, 0) + 1
            if not summary:
                print(f)
                for k, m in found:
                    print(f"   {k}: {m}")
    print(f"--- {total} figure(s), {bad} with findings, {sum(kinds.values())} finding(s) {kinds}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
