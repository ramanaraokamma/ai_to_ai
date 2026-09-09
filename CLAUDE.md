# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A complete AI curriculum for **one learner who starts in 6th grade** and grows over 2–3 years, split
into 4 levels. It is a **content repository with one small Python program in it** — there is no
application, no test suite, and no dependencies to install beyond `cryptography`.

Two editions of the same material coexist, and it matters which one you are editing:

| Edition | Where | Shape |
|---|---|---|
| **Reference modules** (self-study) | `levels/level-N-*/module-0N-*.md` | 9 modules per level, one file each |
| **Taught course** (36 weekly classes) | `levels/level-N-*/36-week-course/` | 3 books × 36 weeks per level |

The 36-week course was **derived from** the modules and must stay consistent with them. Levels 1 and 2
have the taught edition; Levels 3 and 4 exist only as reference modules.

## Commands

```bash
# Build + serve the website (both levels). Binds 127.0.0.1 only — nothing is published.
./site-app/serve.sh                  # → http://localhost:8000/
./site-app/serve.sh 9000             # different port
./site-app/serve.sh --rebuild        # regenerate first, after editing course markdown

# Build only
python3 site-app/build.py --clean    # ~3 s for both levels

# Change the passcodes (defaults: student1234 / teacher1234)
AIA_STUDENT_PASS="..." AIA_TEACHER_PASS="..." python3 site-app/build.py --clean

# Level 2 figure audit — bounds, 12px type floor, banned SVG constructs, label collisions.
# STYLE.md requires this to print "--- 0 finding(s)".
cd levels/level-2-builder/36-week-course/figures/_generator && python3 _gen_audit.py
```

There is no lint or test command. Verification in this repo means: **execute the Python in the
markdown, validate the SVGs as XML, and crawl the links.** See "Verifying content" below.

## The website generator (`site-app/`)

`site-app/build.py` is a self-contained static site generator: markdown → HTML, with a
**passcode-gated two-tier encryption** scheme. `dist/` is generated output — never edit it; edit
`assets_src/app.css` and `assets_src/app.js`, or the `HOME_JS` string inside `build.py`.

Architecture worth knowing before changing it:

- **`ALL_LEVELS`** is the single source of truth for which levels exist, their URL key (`l1`, `l2`),
  accent colour and term names. Adding a level is one entry; levels whose `36-week-course/` folder is
  absent are skipped automatically and listed as "not built yet" on the root page.
- **Routes are level-prefixed** (`l2/chapter/week-07.html`). `build_route_map()` maps every source
  path → route across *all* levels first, so cross-level markdown links resolve. `make_resolver()`
  turns a markdown link into a correct relative URL, and emits `unavailable:` for anything outside
  the generated site — the build counts these and renders them inert rather than as broken links.
- **`parse_weeks()` locates the type column rather than trusting an index**, because Level 1's plan
  table has 6 columns and Level 2's has 7 (it adds "New syntax"). Keep that property if you touch it.
- **Encryption.** Both passcodes derive AES-256 keys via PBKDF2-HMAC-SHA256 (250k iterations) from
  one shared salt. Student-tier pages are encrypted under the student key, teacher-tier under the
  teacher key, and the student key is *also* stored wrapped under the teacher key — so one teacher
  unlock opens both tiers, but a student passcode cannot go the other way. Only the root
  `index.html` is plaintext; every other page ships as a ~20 KB shell with an empty content element.
  Browser side is WebCrypto in `assets_src/app.js`; keys live in `sessionStorage`.
- **The markdown renderer is deliberately not general-purpose.** It covers exactly the dialect this
  course uses. Two invariants exist because both were real bugs:
  - Inline patterns are compiled once and matched with an explicit `pos` — **never against
    `text[i:]`**, which copies the string tail per character and made a 99 KB Level 2 file hang.
  - The paragraph branch **always consumes at least one line**, so the main loop cannot stall on a
    content shape no branch handles. Unfenced ASCII diagrams starting with `|` are also captured
    as preformatted before that point.
- Progress-tracking `localStorage` keys are namespaced per level (`aia-done-l1`), because week 5 of
  Level 1 and week 5 of Level 2 are different weeks.

## Course content conventions

Every weekly file follows a fixed section order marked with emoji (🎯 objectives · 🪝 hook · 🧠
concept · 🔍 worked example · 💻 code · 🐞 debugging · ✍️ practice · ⚠️ mistakes · 🔑 takeaways ·
📓 vocabulary · ✅ answers). Match the surrounding files rather than inventing a variant — Level 1
and Level 2 each settled into a consistent dialect and mid-file drift is worse than either choice.

Hard rules that the content depends on:

- **Level 1 contains zero code.** Tools are unplugged activities, Google Teachable Machine, Scratch,
  Quick Draw and spreadsheets. Nothing to install.
- **Level 2 is Python 3 + numpy/pandas/matplotlib/scikit-learn only.** No seaborn, no torch (Level 3).
- **Level 2 has a syntax ladder** in `36-week-course/README.md`: max ~4 new Python constructs per
  week, and a construct must never appear before the week that introduces it. This is the level's
  main pacing control. Check the ladder before using `zip`, `enumerate`, comprehensions, f-strings etc.
- **No term is used before it is defined**, across the whole 4-level arc.
- **Never hand the student a teacher file.** Teacher guides contain every answer and also name the
  mistakes the student is expected to make.
- **Outputs in markdown must be real.** Code blocks are meant to have been executed and their actual
  stdout pasted. Invented or rounded output is the defect class that has bitten this repo most —
  e.g. `round(48.0996, 2)` documented as printing `48.1` when Python prints `48.10`.
- **Figures diagram the mental model, never screenshot the code.** Each level's
  `36-week-course/figures/STYLE.md` is the binding spec: palette by role, viewBox only (no
  `width`/`height`), `role="img"` + `<title>` + `<desc>`, 12px type floor, no external references,
  and colour is never the only carrier of meaning. Markdown alt text must match the SVG `<title>`
  word for word.

## Verifying content

When you edit course markdown, the checks that actually catch things:

```bash
# Every Python block still runs (Level 2). Use a cumulative per-file namespace and matplotlib Agg —
# later blocks legitimately depend on earlier ones, and some blocks are deliberately broken
# teaching examples, so triage failures rather than "fixing" them.
# Claimed outputs must be diffed against real stdout.

# Every SVG parses and obeys STYLE.md
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" <file.svg>

# Broken links: crawl dist/ AND the decrypted page bodies — most in-content links live inside
# ciphertext once built, so a plain HTML crawl misses ~2/3 of them.
```

## Known state and gaps

- `git` has one commit; roughly half the files are untracked and there is no `.gitignore`.
  `figures/__pycache__` regenerates when the Level 2 figure generators run.
- Level 2 audit residue: ~1,600 of 3,064 Python blocks have no adjacent output to diff against;
  ~200 output pairs remain non-matching by machine diff (triaged, ~35 hand-verified); 5 blocks use
  unseeded `random` and 17 wait on `input()`, so they cannot be output-verified.
- `site/index.html` (the old single-file 4-level map) and each level's
  `36-week-course/site/index.html` are standalone hand-authored pages that predate `site-app/` and
  are **not** generated by it. They can drift.
- Levels 3 and 4 have no 36-week course.
