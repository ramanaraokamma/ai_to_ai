"""
AI Academy — static site generator.

Renders every level that has a 36-week-course/ folder (currently Levels 1 to 4) into one
self-contained static site, with a level picker at the root and two access tiers.

  Public          — the root level picker only.
  Student passcode — chapters, workbooks, projects, glossary, reference modules, gallery.
  Teacher passcode — all of the above plus lesson scripts, orientation, term tests,
                     answer keys and the figure style guide.

Every content page is encrypted at build time with AES-256-GCM under its tier's key,
derived from the passcode with PBKDF2-HMAC-SHA256. The teacher key additionally wraps the
student key, so one teacher unlock opens both tiers. Without a passcode the bytes on disk
are unreadable — there is no plaintext to view-source.

Adding a level: drop an entry in ALL_LEVELS. Levels whose 36-week-course/ folder does not
exist yet are skipped automatically and listed as "not built yet" on the root page.

Stdlib only, except `cryptography` for AES-GCM at build time.

Usage:
    python3 site-app/build.py --clean
    ./site-app/serve.sh
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except ImportError:
    sys.exit("This build needs `cryptography`. Install it with:  pip install cryptography")

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "dist"

PBKDF2_ITERATIONS = 250_000


# ─────────────────────────────────────────────────────────────────────────────
# Levels
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Level:
    number: int
    key: str            # url segment, e.g. "l1"
    slug: str           # folder name, e.g. "level-1-explorer"
    name: str
    tagline: str
    grade: str
    blurb: str
    accent: str         # css colour role used as this level's accent
    terms: list         # (number, name, from_week, to_week, big_question)

    @property
    def dir(self) -> Path:
        return ROOT / "levels" / self.slug / "36-week-course"

    @property
    def level_dir(self) -> Path:
        return ROOT / "levels" / self.slug


ALL_LEVELS = [
    Level(
        number=1, key="l1", slug="level-1-explorer", name="Explorer",
        tagline="Machines can learn a rule from examples instead of being told the rule.",
        grade="Grade 6 · age ~11 · no code",
        blurb="Unplugged activities, Teachable Machine, Scratch and spreadsheets. "
              "Zero programming, zero installs.",
        accent="var(--data)",
        terms=[
            (1, "Spotting AI in the Wild", 1, 9,
             "What is AI really, and what is it made of?"),
            (2, "Teaching a Machine to Guess", 10, 18,
             "How do you turn the world into examples a machine can learn from?"),
            (3, "Trust, Proof, and Pixels", 19, 27,
             "How do you prove a model is any good — and what is it looking at?"),
            (4, "Words, Fairness, and Your Own AI", 28, 36,
             "How do machines handle language, who does AI let down, and can you build one "
             "and defend it honestly?"),
        ],
    ),
    Level(
        number=2, key="l2", slug="level-2-builder", name="Builder",
        tagline="If you can write code, you can turn a table of data into a model that predicts.",
        grade="Grades 7–8 · age ~12 · Python",
        blurb="Python from zero, then numpy, pandas, matplotlib and scikit-learn. "
              "First real models, honestly tested.",
        accent="var(--model)",
        terms=[
            (1, "Say It in Python", 1, 9,
             "How do you give a computer an instruction it cannot misunderstand — and read what "
             "it says back when you get it wrong?"),
            (2, "Build Your Own Toolbox", 10, 18,
             "How do you package your own tools, and hold a whole dataset inside your program?"),
            (3, "Real Tables, Honest Pictures", 19, 27,
             "How do you load a real, messy table, clean it honestly, and draw a picture that "
             "does not lie?"),
            (4, "Three Lines That Predict", 28, 36,
             "Can you train a model, prove the score is honest, and catch it memorising instead "
             "of learning?"),
        ],
    ),
    Level(
        number=3, key="l3", slug="level-3-engineer", name="Engineer",
        tagline="A model is one component of a measured, engineered, shippable pipeline.",
        grade="Grades 9–10 · age ~14 · PyTorch",
        blurb="Splits, leakage, metrics, gradient descent by hand, a neural network in numpy, "
              "then PyTorch and CNNs. Fully offline — no dataset downloads.",
        accent="var(--correct)",
        terms=[
            (1, "Build It Honestly", 1, 9,
             "How do you turn a messy table into a model somebody else can load and use — without "
             "lying to yourself about the score?"),
            (2, "Inside the Box", 10, 18,
             "What is the machine actually doing when it learns — and can I do it myself, with a pen "
             "and twenty-five lines of numpy?"),
            (3, "Real Networks, Real Framework", 19, 27,
             "Once you have built a brain by hand, how do you hand the boring part to PyTorch — and "
             "teach it to see?"),
            (4, "No Labels, Words, and Ship It", 28, 36,
             "What can you learn with no answer key, how do you turn words into numbers, and how do "
             "you hand the finished thing to a stranger?"),
        ],
    ),
    Level(
        number=4, key="l4", slug="level-4-innovator", name="Innovator",
        tagline="A language model is a system you can build, measure, attack and honestly describe.",
        grade="Grades 10–11 · age ~15–16 · PyTorch, fully offline",
        blurb="Train networks on purpose, build a small GPT, then tokenizers, scaling, retrieval, "
              "agents, evals and red-teaming — all on CPU with local stand-ins, no API and no downloads.",
        accent="var(--human)",
        terms=[
            (1, "Train It On Purpose", 1, 9,
             "Your loss curve is wrong. Which of ten knobs do you turn — and how do you know, before "
             "you turn it?"),
            (2, "Memory, Then Attention", 10, 18,
             "Why can a network not remember forty steps back — and what did people build instead of "
             "making it remember?"),
            (3, "How It Is Made, How It Is Asked", 19, 27,
             "Where does a language model's behaviour come from — and how do you test what you ask it, "
             "and what you retrieve for it, like an engineer?"),
            (4, "Agents, Evidence, and the System Card", 28, 36,
             "You have built the parts. Can you build a product out of them, prove it works, attack it "
             "yourself, and tell a stranger honestly where it breaks?"),
        ],
    ),
]


def _level_is_complete(lv: Level) -> tuple[bool, str]:
    """A level ships only when all three books are finished. A half-built level on the site is
    worse than an absent one — the gaps read as broken links, not as work in progress."""
    if not lv.dir.exists():
        return False, "no 36-week-course/ folder"
    if not (lv.dir / "README.md").exists():
        return False, "no README.md (the week table drives every page)"
    counts = {}
    for book in ("teacher-guide", "student-guide", "workbook"):
        counts[book] = sum(1 for w in range(1, 37)
                           if (lv.dir / book / f"week-{w:02d}.md").exists())
    missing = {b: 36 - n for b, n in counts.items() if n < 36}
    if missing:
        return False, "incomplete: " + ", ".join(f"{b} {n} week(s) short" for b, n in missing.items())
    return True, "complete"


# only build levels whose 36-week course is finished
LEVELS = []
for _lv in ALL_LEVELS:
    _ok, _why = _level_is_complete(_lv)
    if _ok:
        LEVELS.append(_lv)
    elif _lv.dir.exists():
        print(f"  skipping L{_lv.number} {_lv.name}: {_why}")



# ─────────────────────────────────────────────────────────────────────────────
# Markdown → HTML
# ─────────────────────────────────────────────────────────────────────────────

RAW_HTML_PREFIXES = ("<details", "</details", "<summary", "</summary", "<a id=", "</a>")

# A leading emoji cluster: emoji codepoints plus variation selectors and ZWJ joiners,
# so "⚠️" (emoji + VS16) and "🧑‍🏫" (ZWJ sequence) are captured whole.
EMOJI_RUN = re.compile(
    r"^((?:[\U0001F300-\U0001FAFF\u2190-\u2BFF\u2600-\u27BF\uFE0F\u200D\u20E3\u2B50]"
    r"|[\U0001F1E6-\U0001F1FF])+)\s*")


def split_icon(text: str) -> tuple[str, str]:
    """('🧠 The Concept') -> ('🧠', 'The Concept'). Returns ('', text) if no leading emoji."""
    m = EMOJI_RUN.match(text)
    return (m.group(1), text[m.end():]) if m else ("", text)


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_-]+", "-", text) or "section"


class Inline:
    """Inline markdown: code, bold, italic, links, images. Escapes everything else."""

    # Compiled once, and matched with an explicit `pos` — never against text[i:],
    # which would copy the tail of the string at every character and make rendering
    # a 60 KB file quadratic.
    RE_CODE = re.compile(r"(`+)(.+?)\1", re.S)
    RE_IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
    RE_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")

    def __init__(self, link_resolver):
        self.resolve = link_resolver

    def render(self, text: str) -> str:
        out, i, n = [], 0, len(text)
        while i < n:
            ch = text[i]

            # `code`  (highest precedence — no markup inside)
            if ch == "`":
                m = self.RE_CODE.match(text, i)
                if m:
                    out.append(f"<code>{html.escape(m.group(2))}</code>")
                    i = m.end()
                    continue

            # ![alt](src)
            if ch == "!" and text.startswith("![", i):
                m = self.RE_IMG.match(text, i)
                if m:
                    alt, src = html.escape(m.group(1)), self.resolve(m.group(2))
                    out.append(
                        f'<img src="{html.escape(src)}" alt="{alt}" loading="lazy" decoding="async">'
                    )
                    i = m.end()
                    continue

            # [text](href)
            if ch == "[":
                m = self.RE_LINK.match(text, i)
                if m:
                    label, href = self.render(m.group(1)), self.resolve(m.group(2))
                    ext = ' target="_blank" rel="noopener"' if href.startswith(("http://", "https://")) else ""
                    out.append(f'<a href="{html.escape(href)}"{ext}>{label}</a>')
                    i = m.end()
                    continue

            # ***bold italic*** / **bold** / *italic*
            if ch == "*":
                for marker, tag in (("***", "strong><em"), ("**", "strong"), ("*", "em")):
                    if text.startswith(marker, i):
                        close = text.find(marker, i + len(marker))
                        if close != -1:
                            inner = self.render(text[i + len(marker):close])
                            if tag == "strong><em":
                                out.append(f"<strong><em>{inner}</em></strong>")
                            else:
                                out.append(f"<{tag}>{inner}</{tag}>")
                            i = close + len(marker)
                            break
                else:
                    out.append("*")
                    i += 1
                continue

            out.append(html.escape(ch))
            i += 1
        return "".join(out)


@dataclass
class Heading:
    level: int
    text: str
    anchor: str


class MarkdownRenderer:
    def __init__(self, link_resolver):
        self.inline = Inline(link_resolver)
        self.headings: list[Heading] = []
        self.plain: list[str] = []

    def render(self, src: str) -> str:
        lines = src.replace("\r\n", "\n").split("\n")
        out: list[str] = []
        i, n = 0, len(lines)

        while i < n:
            line = lines[i]
            stripped = line.strip()

            # blank
            if not stripped:
                i += 1
                continue

            # fenced code
            if stripped.startswith("```"):
                lang = stripped[3:].strip()
                i += 1
                buf = []
                while i < n and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                i += 1  # closing fence
                cls = f' class="lang-{html.escape(lang)}"' if lang else ""
                body = html.escape("\n".join(buf))
                out.append(f'<pre{cls}><code>{body}</code></pre>')
                continue

            # raw HTML we deliberately allow through
            if stripped.startswith(RAW_HTML_PREFIXES):
                out.append(stripped)
                self.plain.append(re.sub(r"<[^>]+>", " ", stripped))
                i += 1
                continue

            # horizontal rule
            if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", stripped):
                out.append("<hr>")
                i += 1
                continue

            # heading
            m = re.match(r"(#{1,6})\s+(.*)$", stripped)
            if m:
                level = len(m.group(1))
                raw = m.group(2).rstrip("#").strip()
                anchor = slugify(raw)
                base, k = anchor, 2
                existing = {h.anchor for h in self.headings}
                while anchor in existing:
                    anchor = f"{base}-{k}"
                    k += 1
                self.headings.append(Heading(level, re.sub(r"[*`]", "", raw), anchor))
                self.plain.append(raw)
                icon, rest = split_icon(raw)
                if icon:
                    body = (f'<span class="sec-ic" aria-hidden="true">{icon}</span>'
                            f'<span class="sec-tx">{self.inline.render(rest)}</span>')
                    attrs = f' class="sec" data-ic="{html.escape(icon)}"'
                else:
                    body, attrs = self.inline.render(raw), ""
                out.append(f'<h{level} id="{anchor}"{attrs}>{body}'
                            f'<a class="anchor" href="#{anchor}" aria-label="Link to this section">#</a></h{level}>')
                i += 1
                continue

            # table
            if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
                i, tbl = self._table(lines, i)
                out.append(tbl)
                continue

            # A run of lines starting with "|" that is NOT a table is almost always an
            # unfenced ASCII diagram (pointer/annotation art). Render it preformatted so
            # the alignment survives — and so it can never fall through to the paragraph
            # branch, which would refuse to consume it and spin forever.
            if stripped.startswith("|"):
                buf = []
                while i < n and lines[i].strip():
                    buf.append(lines[i])
                    i += 1
                self.plain.append(" ".join(x.strip() for x in buf))
                out.append(f'<pre class="ascii"><code>{html.escape(chr(10).join(buf))}</code></pre>')
                continue

            # blockquote
            if stripped.startswith(">"):
                buf = []
                while i < n and lines[i].strip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                inner = MarkdownRenderer(self.inline.resolve)
                body = inner.render("\n".join(buf))
                self.plain.extend(inner.plain)
                first = next((ln.strip() for ln in buf if ln.strip()), "")
                icon, _ = split_icon(re.sub(r"^[*_#>\s]+", "", first))
                if icon:
                    out.append(f'<blockquote class="callout" data-ic="{html.escape(icon)}">{body}</blockquote>')
                else:
                    out.append(f"<blockquote>{body}</blockquote>")
                continue

            # list
            if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
                i, lst = self._list(lines, i)
                out.append(lst)
                continue

            # paragraph — always consumes at least one line, so the loop can never stall
            # even if some future content shape isn't handled by a branch above.
            buf = []
            while i < n and lines[i].strip() and (not buf or not self._starts_block(lines, i)):
                buf.append(lines[i].strip())
                i += 1
            text = " ".join(buf)
            self.plain.append(text)
            # a lone italic line right after an image is a figure caption
            cap = re.fullmatch(r"\*([^*].*?)\*", text)
            if cap and out and out[-1].startswith("<p><img"):
                out[-1] = out[-1][:-4] + f'<span class="caption">{self.inline.render(cap.group(1))}</span></p>'
            else:
                rendered = self.inline.render(text)
                cls = ' class="figure"' if rendered.startswith("<img") else ""
                out.append(f"<p{cls}>{rendered}</p>")

        return "\n".join(out)

    def _starts_block(self, lines, i) -> bool:
        s = lines[i].strip()
        return (
            s.startswith(("```", ">", "|"))
            or s.startswith(RAW_HTML_PREFIXES)
            or bool(re.match(r"#{1,6}\s", s))
            or bool(re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s))
            or bool(re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]))
        )

    def _table(self, lines, i):
        def cells(row):
            row = row.strip()
            row = row[1:] if row.startswith("|") else row
            row = row[:-1] if row.endswith("|") else row
            return [c.strip() for c in re.split(r"(?<!\\)\|", row)]

        header = cells(lines[i])
        aligns = []
        for spec in cells(lines[i + 1]):
            left, right = spec.startswith(":"), spec.endswith(":")
            aligns.append("center" if left and right else "right" if right else "left" if left else "")
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(cells(lines[i]))
            i += 1

        def cell(tag, text, idx):
            a = aligns[idx] if idx < len(aligns) else ""
            style = f' style="text-align:{a}"' if a else ""
            return f"<{tag}{style}>{self.inline.render(text.replace(chr(92) + '|', '|'))}</{tag}>"

        thead = "".join(cell("th", c, k) for k, c in enumerate(header))
        body = []
        for r in rows:
            self.plain.append(" ".join(r))
            body.append("<tr>" + "".join(cell("td", c, k) for k, c in enumerate(r)) + "</tr>")
        self.plain.append(" ".join(header))
        return i, (f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead>'
                   f'<tbody>{"".join(body)}</tbody></table></div>')

    def _list(self, lines, i):
        def info(line):
            m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
            if not m:
                return None
            return len(m.group(1).replace("\t", "    ")), m.group(2), m.group(3)

        base = info(lines[i])[0]
        ordered = info(lines[i])[1][0].isdigit()
        items: list[list[str]] = []
        while i < len(lines):
            meta = info(lines[i])
            if meta and meta[0] <= base + 1:
                if meta[0] < base:
                    break
                items.append([meta[2]])
                i += 1
            elif items and lines[i].strip() and (info(lines[i]) or
                    len(lines[i]) - len(lines[i].lstrip()) > base):
                items[-1].append(lines[i])
                i += 1
            else:
                break

        html_items = []
        for chunk in items:
            first, rest = chunk[0], chunk[1:]
            self.plain.append(first)
            body = self.inline.render(first)
            if rest:
                dedent = "\n".join(
                    ln[min((len(l) - len(l.lstrip()) for l in rest if l.strip()), default=0):]
                    for ln in rest
                )
                sub = MarkdownRenderer(self.inline.resolve)
                body += sub.render(dedent)
                self.plain.extend(sub.plain)
            html_items.append(f"<li>{body}</li>")
        tag = "ol" if ordered else "ul"
        return i, f"<{tag}>{''.join(html_items)}</{tag}>"


# ─────────────────────────────────────────────────────────────────────────────
# Content model
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Doc:
    src: Path
    route: str          # e.g. "l1/chapter/week-01.html"
    mode: str           # "student" | "teacher"
    kind: str           # chapter | workbook | lesson | test | project | page
    week: int | None
    title: str = ""
    nav_label: str = ""
    headings: list[Heading] = field(default_factory=list)
    body: str = ""
    text: str = ""
    level: str = ""     # level key, e.g. "l1"


def first_h1(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.startswith("# "):
            return re.sub(r"[*`]", "", line[2:]).strip()
    return path.stem


def discover(lv: Level) -> list[Doc]:
    docs: list[Doc] = []
    C = lv.dir
    R = lv.level_dir

    def add(src, sub, mode, kind, week, nav_label=None):
        if not src.exists():
            print(f"  ! missing, skipped: {src.relative_to(ROOT)}")
            return
        t = first_h1(src)
        docs.append(Doc(src, f"{lv.key}/{sub}", mode, kind, week, t, nav_label or t, level=lv.key))

    for wk in range(1, 37):
        nn = f"{wk:02d}"
        add(C / "student-guide" / f"week-{nn}.md", f"chapter/week-{nn}.html", "student", "chapter", wk)
        add(C / "workbook" / f"week-{nn}.md", f"workbook/week-{nn}.html", "student", "workbook", wk)
        add(C / "teacher-guide" / f"week-{nn}.md", f"lesson/week-{nn}.html", "teacher", "lesson", wk)

    add(C / "teacher-guide" / "00-orientation.md", "lesson/orientation.html", "teacher", "lesson", None,
        "Teacher Orientation — read this first")
    for t in range(1, 5):
        add(C / "assessments" / f"term-{t}-test.md", f"tests/term-{t}.html", "teacher", "test", None,
            f"Term {t} Test")
    add(C / "assessments" / "README.md", "tests/marking.html", "teacher", "test", None,
        "Marking & Remediation")
    add(C / "figures" / "STYLE.md", "lesson/style-guide.html", "teacher", "lesson", None, "Figure Style Guide")

    add(C / "projects" / "project-ideas.md", "projects/ideas.html", "student", "project", None, "50 Project Ideas")
    add(C / "projects" / "worked-example-project.md", "projects/worked-example.html", "student", "project", None,
        "A Finished Project, Marked")
    add(C / "projects" / "capstone.md", "projects/capstone.html", "student", "project", None, "The Capstone")
    add(C / "HOW-TO-USE.md", "how-to-use.html", "student", "page", None, "How To Use This Course")
    add(C / "README.md", "plan.html", "student", "page", None, "The 36-Week Plan")

    # level reference material that the weekly files link to
    add(R / "glossary.md", "glossary.html", "student", "page", None, "Glossary — every word, defined")
    add(R / "README.md", "level-overview.html", "student", "page", None, f"About Level {lv.number}")
    add(R / "capstone.md", "projects/capstone-brief.html", "student", "project", None,
        "Capstone — original brief")
    add(R / "assessment.md", "tests/exit-exam.html", "teacher", "test", None,
        f"Level {lv.number} Exit Exam")
    for mod in sorted(R.glob("module-0*.md")):
        num = re.match(r"module-(\d+)", mod.stem).group(1)
        add(mod, f"modules/module-{num}.html", "student", "page", None,
            f"Module {int(num)} — {first_h1(mod).split('—', 1)[-1].strip()}")
    return docs


# Directory links in the markdown map to a representative page.
DIR_ALIASES = {
    "student-guide": "chapter/week-01.html",
    "workbook": "workbook/week-01.html",
    "teacher-guide": "lesson/orientation.html",
    "assessments": "tests/marking.html",
    "projects": "projects/ideas.html",
    "figures": "gallery.html",
}


def build_route_map(all_docs: list[Doc]) -> dict[Path, str]:
    """Source path -> site route, across every level, so cross-level links resolve."""
    m = {d.src.resolve(): d.route for d in all_docs}
    for lv in LEVELS:
        for svg in (lv.dir / "figures").glob("*.svg"):
            m[svg.resolve()] = f"assets/figures/{lv.key}/{svg.name}"
    return m


def clean_url(path: str) -> str:
    """Internal routes keep `.html` on disk; links drop it.

    `foo/bar.html` -> `foo/bar`, and `.../index.html` -> `.../` so the level home is a
    directory URL. Cloudflare Workers resolves both against the real files automatically;
    `serve.sh` installs a matching fallback so local serving behaves the same way.
    """
    frag = ""
    if "#" in path:
        path, frag = path.split("#", 1)
        frag = "#" + frag
    if path.endswith("index.html"):
        path = path[: -len("index.html")]
    elif path.endswith(".html"):
        path = path[: -len(".html")]
    return (path or "./") + frag


def make_resolver(doc: Doc, routes: dict[Path, str]):
    here = Path(doc.route).parent
    lv_key = doc.level

    def rel(target_route: str) -> str:
        return os.path.relpath(target_route, here.as_posix() if here.as_posix() != "." else ".")

    def resolve(link: str) -> str:
        if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
            return link
        frag = ""
        if "#" in link:
            link, frag = link.split("#", 1)
            frag = "#" + frag
        if not link:
            return frag
        target = (doc.src.parent / link).resolve()
        if target in routes:
            return clean_url(rel(routes[target])) + frag
        if target.is_dir():
            for cand in ("README.md", "index.md"):
                if (target / cand).resolve() in routes:
                    return clean_url(rel(routes[(target / cand).resolve()])) + frag
            if target.name in DIR_ALIASES:
                return clean_url(rel(f"{lv_key}/{DIR_ALIASES[target.name]}")) + frag
            # a link to a whole level folder, e.g. ../level-2-builder/
            for lv in LEVELS:
                if target == lv.level_dir.resolve() or target == lv.dir.resolve():
                    return clean_url(rel(f"{lv.key}/index.html")) + frag
        # outside the generated site — flagged by the build and rendered inert
        return "unavailable:" + link + frag

    return resolve


# ─────────────────────────────────────────────────────────────────────────────
# Encryption
# ─────────────────────────────────────────────────────────────────────────────

def derive_key(passphrase: str, salt: bytes) -> bytes:
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                      iterations=PBKDF2_ITERATIONS).derive(passphrase.encode())


def encrypt_bytes(key: bytes, plaintext: bytes) -> dict:
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext, None)
    return {"iv": base64.b64encode(nonce).decode(), "ct": base64.b64encode(ct).decode()}


def encrypt(key: bytes, plaintext: str) -> dict:
    return encrypt_bytes(key, plaintext.encode("utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# Page shell
# ─────────────────────────────────────────────────────────────────────────────

def shell(*, doc: Doc, depth: int, nav_json: str, body: str, encrypted: bool,
          lv: Level | None = None) -> str:
    up = "../" * depth
    week_badge = f'<span class="badge wk">Week {doc.week}</span>' if doc.week else ""
    kind_label = {"chapter": "Student Chapter", "workbook": "Workbook", "lesson": "Lesson Script",
                  "test": "Assessment", "project": "Project", "page": "Course Info"}[doc.kind]
    toc = "".join(
        f'<a class="toc-l{h.level}" href="#{h.anchor}">{html.escape(h.text)}</a>'
        for h in doc.headings if 2 <= h.level <= 3
    )

    lvl_chip = ""
    if lv:
        opts = "".join(
            f'<a href="{up}{x.key}/" class="lvl-opt'
            f'{" on" if x.key == lv.key else ""}">L{x.number} · {html.escape(x.name)}</a>'
            for x in LEVELS)
        lvl_chip = (f'<div class="lvl-switch" role="group" aria-label="Level">'
                    f'<span class="lvl-cur">L{lv.number}</span>'
                    f'<div class="lvl-menu">{opts}</div></div>')

    if encrypted:
        tier_note = ("This is <strong>teacher material</strong> — a lesson script, an answer key or a "
                     "test. Only the teacher passcode opens it."
                     if doc.mode == "teacher" else
                     "Enter your passcode to read this page. Either the student or the teacher "
                     "passcode will open it.")
        content = (
            f'<div id="locked" class="locked"><div class="lock-card">'
            f'<div class="lock-ico" aria-hidden="true">🔒</div>'
            f'<h2>{"Teacher material" if doc.mode == "teacher" else "Locked"}</h2>'
            f'<p>{tier_note} It stays unlocked for the rest of this browser session.</p>'
            f'<form id="unlock-form"><label class="sr-only" for="pass">Passcode</label>'
            f'<input id="pass" type="password" autocomplete="current-password" '
            f'placeholder="Passcode" required></input>'
            f'<button type="submit">Unlock</button></form>'
            f'<p id="lock-msg" class="lock-msg" role="status"></p>'
            f'<p class="lock-foot"><a href="{up}{doc.level}/">← Back to '
            f'Level {lv.number if lv else ""} home</a> · '
            f'<a href="{up}">All levels</a></p>'
            f'</div></div>'
            f'<article id="content" class="doc" hidden data-tier="{doc.mode}" '
            f'data-enc="{up}assets/enc/{doc.route.replace("/", "__")}.json"></article>')
    else:
        content = f'<article id="content" class="doc">{body}</article>'

    # Level 4 uses scripted stand-ins for language models (the course labels each one in place);
    # the site repeats the label so no page can be read as showing a real model.
    stand_in_note = ('<p class="stand-in-note">Level 4 runs offline on this machine. Where a lesson uses a '
                     'scripted stand-in for a language model, it is labelled \u201cstand-in, not a model\u201d.</p>'
                     if doc.level == "l4" and week_badge else "")

    return f"""<!DOCTYPE html>
<html lang="en" data-mode="{doc.mode}" data-level="{doc.level}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(doc.title)} · AI Academy</title>
<link rel="stylesheet" href="{up}assets/app.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('aia-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
</head>
<body data-depth="{depth}">
<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <a class="brand" href="{up}"><span class="logo">AI</span> Academy</a>
  {lvl_chip}
  <div class="modes" role="group" aria-label="Navigation mode">
    <a href="{up}{doc.level}/#student" class="mode-btn" data-mode-btn="student">🎒 Student</a>
    <a href="{up}{doc.level}/#teacher" class="mode-btn" data-mode-btn="teacher">🧑‍🏫 Teacher <span class="lk" aria-hidden="true">🔒</span></a>
  </div>
  <div class="top-right">
    <span id="who" class="who-chip" hidden></span>
    <button id="signout" class="icon-btn" aria-label="Sign out" title="Sign out" hidden>⎋</button>
    <button id="theme" class="icon-btn" aria-label="Toggle dark mode" title="Toggle dark mode">◐</button>
    <button id="nav-toggle" class="icon-btn only-mobile" aria-label="Toggle navigation" aria-expanded="false">☰</button>
  </div>
</header>
<div class="layout">
  <nav id="side" class="side" aria-label="Course navigation">
    <input id="nav-search" class="nav-search" type="search" placeholder="Search this level…" aria-label="Search this level">
    <div id="nav-tree"></div>
  </nav>
  <main class="main">
    <div class="crumbs">{week_badge}<span class="badge kind">{kind_label}</span></div>
    {stand_in_note}
    {content}
    <nav class="pager" id="pager" aria-label="Previous and next"></nav>
  </main>
  <aside class="toc" aria-label="On this page">{'<h2>On this page</h2>' + toc if toc else ''}</aside>
</div>
<script>window.AIA_NAV={nav_json};window.AIA_ROUTE="{doc.route}";window.AIA_UP="{up}";</script>
<script src="{up}assets/app.js"></script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Week metadata (from the course plan table)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Week:
    number: int
    term: int
    title: str
    big_idea: str
    type: str
    homework: str
    syntax: str = ""     # Level 2+ only: the new Python constructs this week


TYPE_ICON = {"teach": ("📘", "t"), "lab": ("🔬", "l"), "project": ("🛠️", "p"),
             "review": ("🔁", "r"), "capstone": ("🎪", "c"), "assessment": ("🏁", "a")}


def parse_weeks(lv: Level) -> list[Week]:
    """
    Reads the '36 weeks' table out of the level's README.

    Level 1 columns: | Week | Term | Title | Big idea | Type | Homework |
    Level 2 columns: | Week | Term | Title | Big idea | New syntax | Type | Homework |

    The type cell is the discriminator — it always reduces to one of the TYPE_ICON keys,
    so we locate it rather than trusting a fixed column index.
    """
    weeks: list[Week] = []
    for line in (lv.dir / "README.md").read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^\|\s*(\d{1,2})\s*\|\s*(\d)\s*\|(.+)$", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(3).split("|")]
        if len(cells) < 4:
            continue

        type_at = None
        for i, c in enumerate(cells):
            if re.sub(r"[^a-z]", "", c.lower()) in TYPE_ICON:
                type_at = i
                break
        if type_at is None or type_at < 2:
            continue

        clean = lambda s: re.sub(r"[*`]", "", s).strip()
        title, idea = clean(cells[0]), clean(cells[1])
        syntax = clean(cells[2]) if type_at >= 3 else ""
        typ = re.sub(r"[^a-z]", "", cells[type_at].lower())
        hw = clean(cells[type_at + 1]) if len(cells) > type_at + 1 else ""

        weeks.append(Week(int(m.group(1)), int(m.group(2)), title, idea, typ, hw, syntax))

    if len(weeks) != 36:
        print(f"  ! {lv.key}: parsed {len(weeks)} weeks from the plan table, expected 36")
    return weeks


def build_nav_payload(lv: Level, weeks: list[Week], docs: list[Doc]) -> str:
    by_week: dict[int, dict[str, str]] = {}
    for d in docs:
        if d.week:
            by_week.setdefault(d.week, {})[d.kind] = d.route
    return json.dumps({
        "level": {"key": lv.key, "number": lv.number, "name": lv.name, "grade": lv.grade},
        "levels": [{"key": x.key, "number": x.number, "name": x.name,
                    "route": f"{x.key}/index.html"} for x in LEVELS],
        "terms": [{"number": n, "name": nm, "from": a, "to": b, "question": q}
                  for n, nm, a, b, q in lv.terms],
        "weeks": [{"week": w.number, "term": w.term, "title": w.title, "type": w.type,
                   "idea": w.big_idea, "syntax": w.syntax, "docs": by_week.get(w.number, {})}
                  for w in weeks],
        "flat": [{"route": d.route, "label": d.nav_label, "kind": d.kind, "mode": d.mode}
                 for d in docs if d.week is None],
    }, ensure_ascii=False, separators=(",", ":"))


def home_page(lv: Level, weeks: list[Week], docs: list[Doc], nav_json: str, counts: dict) -> str:
    """The per-level home page, written to <key>/index.html."""
    by_week: dict[int, dict[str, str]] = {}
    for d in docs:
        if d.week:
            by_week.setdefault(d.week, {})[d.kind] = d.route

    # routes are site-absolute ("l1/chapter/…"); this page sits inside l1/, so drop the prefix
    def here(route: str) -> str:
        r = route[len(lv.key) + 1:] if route.startswith(lv.key + "/") else "../" + route
        return clean_url(r)

    terms_html = []
    for idx, (num, name, lo, hi, question) in enumerate(lv.terms):
        cards = []
        for w in [x for x in weeks if lo <= x.number <= hi]:
            icon, cls = TYPE_ICON.get(w.type, ("📘", "t"))
            r = by_week.get(w.number, {})
            links = []
            if "chapter" in r:
                links.append(f'<a class="lockable" data-need="student" href="{here(r["chapter"])}">📗 Chapter</a>')
            if "workbook" in r:
                links.append(f'<a class="lockable" data-need="student" href="{here(r["workbook"])}">✏️ Workbook</a>')
            if "lesson" in r:
                links.append(f'<a class="lockable tch" data-need="teacher" href="{here(r["lesson"])}">🧑‍🏫 Lesson script</a>')
            syntax_chips = ""
            if w.syntax:
                bits = [b.strip() for b in re.split(r"·|,", w.syntax) if b.strip()][:5]
                syntax_chips = ('<div class="syn">' + "".join(
                    f'<code class="syn-chip">{html.escape(b.strip("`"))}</code>' for b in bits)
                    + '</div>')
            cards.append(
                f'<article class="wk-card" data-week="{w.number}" '
                f'data-search="{html.escape((str(w.number) + " " + w.title + " " + w.big_idea + " " + w.type + " " + w.syntax).lower())}">'
                f'<div class="row1"><span class="num">WEEK {w.number:02d}</span>'
                f'<span class="type-{cls}" title="{w.type}">{icon} {w.type}</span>'
                f'<label class="done"><input type="checkbox" data-done="{w.number}"> done</label></div>'
                f'<h3>{html.escape(w.title)}</h3>'
                f'<p class="idea">{html.escape(w.big_idea)}</p>'
                f'{syntax_chips}'
                f'<div class="links">{"".join(links)}</div>'
                f'</article>')
        terms_html.append(
            f'<section class="term" data-term="{num}">'
            f'<div class="term-head"><h2>Term {num} · {html.escape(name)}</h2>'
            f'<span class="rng">Weeks {lo}–{hi}</span>'
            f'<p class="q">{html.escape(question)}</p>'
            f'<div class="term-bar"><i data-term-bar="{num}" style="background:{lv.accent}"></i></div></div>'
            f'<div class="weeks">{"".join(cards)}</div></section>')

    extras = [d for d in docs if d.week is None]
    extra_links = "".join(
        f'<a class="lockable" href="{here(d.route)}" data-need="{d.mode}">{html.escape(d.nav_label)}</a>'
        for d in extras)

    other = [x for x in LEVELS if x.key != lv.key]
    other_links = " · ".join(
        f'<a href="../{x.key}/">Level {x.number} {html.escape(x.name)}</a>' for x in other)
    lvl_opts = "".join(
        f'<a href="../{x.key}/" class="lvl-opt{" on" if x.key == lv.key else ""}">'
        f'L{x.number} · {html.escape(x.name)}</a>' for x in LEVELS)

    first_chapter = here(by_week.get(1, {}).get("chapter", "chapter/week-01.html"))
    orientation = next((here(d.route) for d in docs
                        if d.route.endswith("lesson/orientation.html")), "lesson/orientation.html")

    return f"""<!DOCTYPE html>
<html lang="en" data-level="{lv.key}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Academy · Level {lv.number} {html.escape(lv.name)} — 36 weeks</title>
<link rel="stylesheet" href="../assets/app.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('aia-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
</head>
<body data-depth="1" class="home">
<a class="skip" href="#year">Skip to the year plan</a>
<header class="top">
  <a class="brand" href="../"><span class="logo">AI</span> Academy</a>
  <div class="lvl-switch" role="group" aria-label="Level">
    <span class="lvl-cur">L{lv.number}</span>
    <div class="lvl-menu">{lvl_opts}</div>
  </div>
  <div class="modes" role="group" aria-label="Navigation mode">
    <a href="#student" class="mode-btn" data-mode-btn="student">🎒 Student</a>
    <a href="#teacher" class="mode-btn" data-mode-btn="teacher">🧑‍🏫 Teacher <span class="lk" aria-hidden="true">🔒</span></a>
  </div>
  <div class="top-right">
    <span id="who" class="who-chip" hidden></span>
    <button id="signout" class="icon-btn" aria-label="Sign out" title="Sign out" hidden>⎋</button>
    <button id="theme" class="icon-btn" aria-label="Toggle dark mode" title="Toggle dark mode">◐</button>
  </div>
</header>

<section class="hero">
  <p class="eyebrow" style="color:{lv.accent}">Level {lv.number} · {html.escape(lv.grade)}</p>
  <h1>{html.escape(lv.name)}</h1>
  <p class="sub">{html.escape(lv.tagline)}<br>{html.escape(lv.blurb)}</p>

  <div id="gate" class="gate">
    <div class="gate-body">
      <div class="gate-ico" aria-hidden="true">🔐</div>
      <div class="gate-text">
        <h2>Enter your passcode to open the course</h2>
        <p>This page is the only one you can read without one. Chapters, workbooks and lesson
           scripts are encrypted until you unlock them.</p>
      </div>
      <form id="gate-form" autocomplete="off">
        <label class="sr-only" for="gate-pass">Passcode</label>
        <input id="gate-pass" type="password" placeholder="Passcode" autocomplete="current-password" required>
        <button type="submit">Unlock</button>
      </form>
      <p id="gate-msg" class="lock-msg" role="status"></p>
      <table class="gate-keys">
        <tr><td>🎒 <strong>Student</strong></td><td>chapters · workbooks · projects · glossary</td></tr>
        <tr><td>🧑‍🏫 <strong>Teacher</strong></td><td>all of the above <em>plus</em> lesson scripts, answer keys, term tests</td></tr>
      </table>
    </div>
  </div>

  <div class="pick" id="pick" hidden>
    <a class="pick-card lockable" href="{first_chapter}" data-need="student">
      <div class="ico">🎒</div>
      <h2>Start Week 1 — your chapter</h2>
      <p>Read the chapter, then do the workbook. Mark it yourself from the answer key.</p>
      <span class="who">Chapters · Workbooks · Projects</span>
    </a>
    <a class="pick-card lockable" href="{orientation}" data-need="teacher">
      <div class="ico">🧑‍🏫</div>
      <h2>Teacher orientation</h2>
      <p>Read this once, before Week 1. It teaches you the whole subject in plain language.</p>
      <span class="who">Lesson scripts · Answer keys · Tests</span>
    </a>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">36</div><div class="l">weekly classes</div></div>
    <div class="stat"><div class="n">4</div><div class="l">terms</div></div>
    <div class="stat"><div class="n">{counts['figures']}</div><div class="l">drawings</div></div>
    <div class="stat"><div class="n">{counts['pages']}</div><div class="l">pages</div></div>
    <div class="stat"><div class="n" id="pct">0%</div><div class="l">you've completed</div></div>
  </div>

  <div class="hero-tools">
    <input id="home-search" class="nav-search" type="search" style="max-width:26rem;margin-top:1.6rem"
           placeholder="Search the 36 weeks…" aria-label="Search the 36 weeks">
    <p id="home-count" class="l" style="color:var(--muted);font-size:.85rem">Showing all 36 weeks</p>
  </div>
  <nav class="links extras" style="display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem">{extra_links}</nav>
  {f'<p class="other-lvl">Other levels: {other_links}</p>' if other else ''}
</section>

<main class="year" id="year">
{"".join(terms_html)}
</main>

<script>window.AIA_NAV={nav_json};window.AIA_ROUTE="{lv.key}/index.html";window.AIA_UP="../";</script>
<script src="../assets/app.js"></script>
<script src="../assets/home.js"></script>
</body>
</html>
"""


def root_page(level_stats: dict) -> str:
    """The site front door: pick a level. Public, no passcode."""
    cards = []
    for lv in LEVELS:
        s = level_stats[lv.key]
        cards.append(
            f'<a class="lvl-card" href="{lv.key}/" style="--lvl:{lv.accent}">'
            f'<div class="lvl-num">Level {lv.number}</div>'
            f'<h2>{html.escape(lv.name)}</h2>'
            f'<p class="lvl-grade">{html.escape(lv.grade)}</p>'
            f'<p class="lvl-tag">{html.escape(lv.tagline)}</p>'
            f'<p class="lvl-blurb">{html.escape(lv.blurb)}</p>'
            f'<div class="lvl-stats"><span>36 weeks</span><span>{s["pages"]} pages</span>'
            f'<span>{s["figures"]} drawings</span></div>'
            f'<span class="lvl-go">Open Level {lv.number} →</span></a>')

    coming = []
    for lv in ALL_LEVELS:
        if lv.key not in {x.key for x in LEVELS}:
            coming.append(f'<li>Level {lv.number} · {html.escape(lv.name)} — {html.escape(lv.grade)}</li>')
    for n, nm, g in [(3, "Engineer", "Grades 9–10 · PyTorch, CNNs, NLP"),
                     (4, "Innovator", "Grades 11–12 · Transformers, LLMs, RAG, agents")]:
        if n > max(lv.number for lv in ALL_LEVELS):
            coming.append(f'<li>Level {n} · {nm} — {g}</li>')

    total_pages = sum(s["pages"] for s in level_stats.values())
    total_figs = sum(s["figures"] for s in level_stats.values())

    coming_html = ""
    if coming:
        coming_html = (
            '<section class="coming"><h2>Not built yet</h2>'
            f'<ul>{"".join(coming)}</ul>'
            '<p>These levels exist as self-study reference modules in the repository, but have '
            'not been expanded into 36 weekly classes.</p></section>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Academy — from 6th grade to building real AI</title>
<link rel="stylesheet" href="assets/app.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('aia-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
</head>
<body data-depth="0" class="root">
<header class="top">
  <a class="brand" href="./"><span class="logo">AI</span> Academy</a>

  <div class="top-right">
    <span id="who" class="who-chip" hidden></span>
    <button id="signout" class="icon-btn" aria-label="Sign out" title="Sign out" hidden>⎋</button>
    <button id="theme" class="icon-btn" aria-label="Toggle dark mode" title="Toggle dark mode">◐</button>
  </div>
</header>

<section class="hero root-hero">
  <h1>AI Academy</h1>
  <p class="sub">One learner. Four levels. Start in 6th grade with zero code — finish able to build
     real AI systems. Each level is a full school year: 36 weekly classes, three books a week, and a
     teacher guide written for someone who has never taught this before.</p>
  <div class="stats">
    <div class="stat"><div class="n">{len(LEVELS)}</div><div class="l">levels ready</div></div>
    <div class="stat"><div class="n">{len(LEVELS) * 36}</div><div class="l">weekly classes</div></div>
    <div class="stat"><div class="n">{total_pages}</div><div class="l">pages</div></div>
    <div class="stat"><div class="n">{total_figs}</div><div class="l">drawings</div></div>
  </div>
</section>

<main class="lvl-grid-wrap">
  <div class="lvl-grid">{"".join(cards)}</div>
  {coming_html}
</main>

<script src="assets/app.js"></script>
<script>
(function(){{
  var r=null; try{{r=sessionStorage.getItem('aia-role')}}catch(e){{}}
  var w=document.getElementById('who'), o=document.getElementById('signout');
  if(r&&w){{w.hidden=false;w.textContent=r==='teacher'?'Teacher':'Student';}}
  if(r&&o){{o.hidden=false;o.addEventListener('click',function(){{
    try{{sessionStorage.clear()}}catch(e){{}} location.reload();
  }});}}
}})();
</script>
</body>
</html>
"""


HOME_JS = r"""
/* AI Academy — home page: passcode gate, role gating, search, progress. */
(function () {
  'use strict';
  var Auth = window.AIA_auth;
  var LVL = (window.AIA_NAV.level && window.AIA_NAV.level.key) || 'l1';
  var LS = { mode: 'aia-mode', done: 'aia-done-' + LVL };
  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function mode() {
    var h = (location.hash || '').replace('#', '');
    if (h === 'teacher' || h === 'student') set(LS.mode, h);
    var m = get(LS.mode, 'student');
    if (m === 'teacher' && Auth.role() !== 'teacher') m = 'student';
    return m;
  }

  var gate = document.getElementById('gate');
  var pick = document.getElementById('pick');
  var gateForm = document.getElementById('gate-form');
  var gateMsg = document.getElementById('gate-msg');
  var gatePass = document.getElementById('gate-pass');

  /* Everything with .lockable is inert until the right passcode is in. */
  function applyGate() {
    var role = Auth.role();
    var m = mode();

    if (gate) gate.hidden = !!role;
    if (pick) pick.hidden = !role;

    document.querySelectorAll('.lockable').forEach(function (el) {
      var need = el.getAttribute('data-need') || 'student';
      var allowed = Auth.can(need);
      // teacher-only links are also hidden from a student entirely
      var hide = need === 'teacher' && role !== 'teacher';
      el.classList.toggle('hidden', hide && !!role);
      el.classList.toggle('is-locked', !allowed);
      if (allowed) {
        el.removeAttribute('aria-disabled');
        el.removeAttribute('tabindex');
      } else {
        el.setAttribute('aria-disabled', 'true');
        el.setAttribute('tabindex', '-1');
      }
    });

    document.body.classList.toggle('locked-out', !role);
    document.querySelectorAll('[data-mode-btn]').forEach(function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-mode-btn') === m ? 'true' : 'false');
    });
  }

  /* Clicking a locked link bounces you to the passcode box instead of 404-ing. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('.lockable');
    if (!a || a.getAttribute('aria-disabled') !== 'true') return;
    e.preventDefault();
    if (!Auth.role()) {
      gate.scrollIntoView({ block: 'center' });
      gatePass.focus();
      gateMsg.className = 'lock-msg';
      gateMsg.textContent = 'Enter a passcode first.';
    } else {
      gateMsg.className = 'lock-msg err';
      gateMsg.textContent = 'That page needs the teacher passcode.';
      gate.hidden = false;
      gate.scrollIntoView({ block: 'center' });
      gatePass.focus();
    }
  });

  if (gateForm) {
    gateForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = gateForm.querySelector('button');
      btn.disabled = true;
      gateMsg.className = 'lock-msg';
      gateMsg.textContent = 'Checking…';
      Auth.unlock(gatePass.value)
        .then(function (role) {
          gateMsg.className = 'lock-msg ok';
          gateMsg.textContent = 'Welcome — signed in as ' + role + '.';
          set(LS.mode, role);
          gatePass.value = '';
          applyGate();
          if (window.AIA_refreshChrome) window.AIA_refreshChrome();
        })
        .catch(function () {
          gateMsg.className = 'lock-msg err';
          gateMsg.textContent = 'That passcode does not match. Try again.';
          gatePass.select();
        })
        .then(function () { btn.disabled = false; });
    });
  }

  /* progress */
  function doneSet() { try { return new Set(JSON.parse(get(LS.done, '[]'))); } catch (e) { return new Set(); } }
  function paintProgress() {
    var s = doneSet();
    document.querySelectorAll('[data-done]').forEach(function (cb) {
      cb.checked = s.has(Number(cb.getAttribute('data-done')));
    });
    (window.AIA_NAV.terms || []).forEach(function (t) {
      var tot = t.to - t.from + 1, n = 0;
      for (var w = t.from; w <= t.to; w++) if (s.has(w)) n++;
      var bar = document.querySelector('[data-term-bar="' + t.number + '"]');
      if (bar) bar.style.width = (n / tot * 100) + '%';
    });
    var pct = document.getElementById('pct');
    if (pct) pct.textContent = Math.round(s.size / 36 * 100) + '%';
  }
  document.addEventListener('change', function (e) {
    var cb = e.target.closest('[data-done]');
    if (!cb) return;
    var s = doneSet(), n = Number(cb.getAttribute('data-done'));
    cb.checked ? s.add(n) : s.delete(n);
    set(LS.done, JSON.stringify(Array.from(s)));
    paintProgress();
  });

  /* search */
  var box = document.getElementById('home-search');
  var count = document.getElementById('home-count');
  if (box) {
    box.addEventListener('input', function () {
      var q = box.value.trim().toLowerCase(), shown = 0;
      document.querySelectorAll('.wk-card').forEach(function (c) {
        var hit = !q || (c.getAttribute('data-search') || '').indexOf(q) !== -1;
        c.classList.toggle('hidden', !hit);
        if (hit) shown++;
      });
      document.querySelectorAll('.term').forEach(function (t) {
        t.classList.toggle('hidden', !t.querySelector('.wk-card:not(.hidden)'));
      });
      count.textContent = q ? shown + ' of 36 weeks match “' + box.value.trim() + '”' : 'Showing all 36 weeks';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && e.target === document.body) { e.preventDefault(); box.focus(); }
    });
  }

  window.addEventListener('hashchange', applyGate);
  applyGate();
  paintProgress();
  if (!Auth.role() && gatePass) gatePass.focus();
})();
"""


def gallery_page(lv: Level, nav_json: str, names: list[str]) -> tuple[str, str]:
    """Returns (page_shell_html, inner_body_html). The body is encrypted like any other page."""
    def week_of(name):
        m = re.match(r"fig-w(\d+)", name)
        return int(m.group(1)) if m else None

    groups: dict[str, list[str]] = {}
    for n in names:
        wk = week_of(n)
        groups.setdefault(f"Week {wk:02d}" if wk else "Shared", []).append(n)

    blocks = []
    for label in sorted(groups, key=lambda s: (s == "Shared", s)):
        items = "".join(
            f'<figure data-search="{html.escape(n.lower())}">'
            f'<img src="../assets/figures/{lv.key}/{html.escape(n)}" alt="{html.escape(n)}" '
            f'loading="lazy" decoding="async">'
            f'<figcaption>{html.escape(n)}</figcaption></figure>'
            for n in sorted(groups[label]))
        blocks.append(f'<section class="gal-group" data-search="{html.escape(label.lower())}">'
                      f'<h2>{label} <span class="rng">{len(groups[label])} figures</span></h2>'
                      f'<div class="gal">{items}</div></section>')

    doc = Doc(lv.dir / "README.md", f"{lv.key}/gallery.html", "student", "page", None,
              f"Figure Gallery — Level {lv.number}", "Figure Gallery", level=lv.key)
    body = (f'<h1 id="figure-gallery">Figure Gallery — Level {lv.number} {html.escape(lv.name)}</h1>'
            f'<p>Every drawing in this level — {len(names)} hand-authored SVGs. '
            f'They scale to any size and print cleanly. Search by filename or week.</p>'
            f'<input id="gal-search" class="nav-search" type="search" placeholder="Filter figures…" '
            f'aria-label="Filter figures">'
            f'<style>.gal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:1rem}}'
            f'.gal figure{{margin:0;padding:.8rem;background:var(--bg);border:1px solid var(--line);'
            f'border-radius:12px;text-align:center}}.gal img{{max-height:16rem}}'
            f'.gal figcaption{{margin-top:.5rem;font-size:.72rem;color:var(--muted);'
            f'font-family:var(--mono);word-break:break-all}}'
            f'.gal-group h2 .rng{{font-size:.75rem;color:var(--muted);font-weight:500}}</style>'
            + "".join(blocks) +
            '<script>(function(){var b=document.getElementById("gal-search");if(!b)return;'
            'b.addEventListener("input",function(){var q=b.value.trim().toLowerCase();'
            'document.querySelectorAll(".gal figure").forEach(function(f){'
            'f.classList.toggle("hidden",!!q&&f.getAttribute("data-search").indexOf(q)===-1)});'
            'document.querySelectorAll(".gal-group").forEach(function(g){'
            'g.classList.toggle("hidden",!g.querySelector("figure:not(.hidden)"))})})})();</script>')
    doc.headings = [Heading(1, "Figure Gallery", "figure-gallery")]
    return shell(doc=doc, depth=1, nav_json=nav_json, body=body, encrypted=True, lv=lv), body


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Build the AI Academy site.")
    ap.add_argument("--student-pass", default=os.environ.get("AIA_STUDENT_PASS", "student1234"),
                    help="Student passcode (or set AIA_STUDENT_PASS)")
    ap.add_argument("--teacher-pass", default=os.environ.get("AIA_TEACHER_PASS", "teacher1234"),
                    help="Teacher passcode (or set AIA_TEACHER_PASS)")
    ap.add_argument("--clean", action="store_true", help="Remove dist/ before building")
    args = ap.parse_args()

    if args.student_pass == args.teacher_pass:
        sys.exit("The student and teacher passcodes must be different.")

    if not LEVELS:
        sys.exit("No level has a 36-week-course/ folder yet — nothing to build.")

    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "enc").mkdir(parents=True, exist_ok=True)

    print("AI Academy — building site")
    print(f"  levels : {', '.join(f'L{lv.number} {lv.name}' for lv in LEVELS)}")
    print(f"  output : {OUT.relative_to(ROOT)}")

    # Two keys from one salt, shared across all levels. Student content is encrypted under
    # the student key; teacher content under the teacher key. The student key is ALSO stored
    # wrapped under the teacher key, so the teacher passcode opens everything in one unlock.
    salt = os.urandom(16)
    key_student = derive_key(args.student_pass, salt)
    key_teacher = derive_key(args.teacher_pass, salt)
    verifier_plain = "ai-academy-ok"

    # shared assets
    src_assets = Path(__file__).resolve().parent / "assets_src"
    for name in ("app.css", "app.js"):
        shutil.copy2(src_assets / name, OUT / "assets" / name)
    (OUT / "assets" / "home.js").write_text(HOME_JS, encoding="utf-8")

    # discover everything first, so cross-level links resolve
    per_level: dict[str, list[Doc]] = {}
    all_docs: list[Doc] = []
    for lv in LEVELS:
        d = discover(lv)
        per_level[lv.key] = d
        all_docs.extend(d)
    routes = build_route_map(all_docs)

    n_student = n_teacher = 0
    dead_links: list[str] = []
    level_stats: dict[str, dict] = {}

    for lv in LEVELS:
        docs = per_level[lv.key]
        weeks = parse_weeks(lv)
        nav_json = build_nav_payload(lv, weeks, docs)

        # figures, namespaced per level
        fig_dir = OUT / "assets" / "figures" / lv.key
        fig_dir.mkdir(parents=True, exist_ok=True)
        figs: list[str] = []
        for svg in sorted((lv.dir / "figures").glob("*.svg")):
            shutil.copy2(svg, fig_dir / svg.name)
            if not svg.name.startswith("_"):
                figs.append(svg.name)

        for doc in docs:
            renderer = MarkdownRenderer(make_resolver(doc, routes))
            body = renderer.render(doc.src.read_text(encoding="utf-8"))
            doc.headings = renderer.headings
            for m in re.finditer(r'href="unavailable:([^"]+)"', body):
                dead_links.append(f"{doc.src.relative_to(ROOT)} -> {m.group(1)}")
            body = re.sub(r'href="unavailable:[^"]*"',
                          'href="#" class="dead" title="Not part of this site"', body)

            depth = doc.route.count("/")
            page = shell(doc=doc, depth=depth, nav_json=nav_json, body=body,
                         encrypted=True, lv=lv)
            dest = OUT / doc.route
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(page, encoding="utf-8")

            key = key_teacher if doc.mode == "teacher" else key_student
            (OUT / "assets" / "enc" / f'{doc.route.replace("/", "__")}.json').write_text(
                json.dumps(encrypt(key, body), separators=(",", ":")), encoding="utf-8")
            if doc.mode == "teacher":
                n_teacher += 1
            else:
                n_student += 1

        gal_page, gal_body = gallery_page(lv, nav_json, figs)
        (OUT / lv.key / "gallery.html").write_text(gal_page, encoding="utf-8")
        (OUT / "assets" / "enc" / f"{lv.key}__gallery.html.json").write_text(
            json.dumps(encrypt(key_student, gal_body), separators=(",", ":")), encoding="utf-8")

        stats = {"weeks": len(weeks), "figures": len(figs), "pages": len(docs) + 1}
        level_stats[lv.key] = stats
        (OUT / lv.key / "index.html").write_text(
            home_page(lv, weeks, docs, nav_json, stats), encoding="utf-8")
        print(f"  L{lv.number} {lv.name:9} {len(weeks)} weeks · {len(docs)} pages · {len(figs)} figures")

    (OUT / "assets" / "enc" / "_meta.json").write_text(json.dumps({
        "salt": base64.b64encode(salt).decode(),
        "iterations": PBKDF2_ITERATIONS,
        "plain": verifier_plain,
        "verifyStudent": encrypt(key_student, verifier_plain),
        "verifyTeacher": encrypt(key_teacher, verifier_plain),
        # student key, wrapped under the teacher key
        "wrappedStudentKey": encrypt_bytes(key_teacher, key_student),
    }, separators=(",", ":")), encoding="utf-8")

    (OUT / "index.html").write_text(root_page(level_stats), encoding="utf-8")

    print(f"  pages  : {n_student} student-tier + {n_teacher} teacher-tier, all encrypted")
    print(f"           1 public page (index.html, the level picker) + {len(LEVELS)} level homes"
          f" + {len(LEVELS)} galleries")
    print(f"  crypto : AES-256-GCM, PBKDF2-SHA256 x{PBKDF2_ITERATIONS:,}, two keys + key wrapping")
    if dead_links:
        print(f"  ! {len(dead_links)} link(s) point outside the generated site:")
        for d in sorted(set(dead_links))[:12]:
            print(f"      {d}")
    print(f"\n  student passcode : {args.student_pass!r}")
    print(f"  teacher passcode : {args.teacher_pass!r}")
    print(f"  serve            : ./site-app/serve.sh")
    print("  then open        : http://localhost:8000/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

