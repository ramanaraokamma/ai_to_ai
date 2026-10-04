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

The 36-week course was **derived from** the modules and must stay consistent with them.
**Levels 1, 2 and 3 have the taught edition; Level 4 exists only as reference modules.**

Top-level orientation docs live at the repo root, not under `levels/`: `README.md`,
`START_HERE.md`, `CURRICULUM_MAP.md`, `RESOURCES.md`, and `teacher-guide/`. `site-app/README.md`
documents the generator.

Scale, so you know what you are touching: 412 markdown files, ~518,000 lines, 1,140 SVGs. Each
taught level is 120 files / 36 weeks / ~96k–182k lines. Do not attempt whole-level edits inline —
see "Building a level" below.

## Commands

```bash
# Build + serve the website (all complete levels). Binds 127.0.0.1 only — nothing is published.
# serve.sh runs serve.py, which resolves extensionless URLs the way Cloudflare Workers does —
# plain `python3 -m http.server` will 404 on every generated link.
./site-app/serve.sh                  # → http://localhost:8000/
./site-app/serve.sh 9000             # different port
./site-app/serve.sh --rebuild        # regenerate first, after editing course markdown

# Build only  (~3 s for three levels)
python3 site-app/build.py --clean

# Change the passcodes (defaults: student1234 / teacher1234)
AIA_STUDENT_PASS="..." AIA_TEACHER_PASS="..." python3 site-app/build.py --clean

# Figure audit — bounds, 12px type floor, banned SVG constructs, label collisions.
# Each level's STYLE.md requires this to print "--- 0 finding(s)". L2 and L3 only; L1 has no generator.
cd levels/level-2-builder/36-week-course/figures/_generator && python3 _gen_audit.py
cd levels/level-3-engineer/36-week-course/figures/_generator && python3 _gen_audit.py
```

There is no lint or test command. Verification here means: **execute the Python in the markdown,
validate the SVGs, and crawl the links.** See "Verifying content".

## Other artefacts

Two self-contained slide decks (no CDN, no webfonts), sharing the same shell: speaker notes (`N`),
dark mode (`T`), keyboard navigation, `#sN` deep links, and a print stylesheet giving one slide per
page with notes. Palettes are copied from the course `figures/STYLE.md` so slides and figures match.

- **`presentations/for-parents.html`** — 16 slides for a parent evening.
- **`presentations/for-investors.html`** — 18 slides for an investor conversation.

**Every number in both decks is cross-checked against the repo.** If you change figure, week or test
counts, re-check the stats slides. Note the two figure conventions: `fig-*.svg` files total **1,137**
(what the decks cite as "diagrams"), while all `*.svg` including each level's `_motifs.svg` sprite
sheet totals **1,140**. Keep a deck internally consistent with one convention.

The investor deck deliberately contains **no invented metrics** — market size, pricing, unit economics
and the raise are dashed-border placeholders marked "fill before presenting", and slide 1 states there
are no users, no pilot and no revenue. Do not "helpfully" populate those with plausible numbers.

## The website generator (`site-app/`)

`site-app/build.py` renders every complete level into one static site with **passcode-gated two-tier
encryption**. `dist/` is generated output — never edit it; edit `assets_src/app.css` and
`assets_src/app.js`, or the `HOME_JS` string inside `build.py`.

Architecture worth knowing before changing it:

- **`ALL_LEVELS`** is the single source of truth for which levels exist, their URL key (`l1`…),
  accent colour and term names. Adding a level is one entry.
- **`_level_is_complete()` gates shipping.** A level appears only when its README plus all 36 weeks
  in all three books exist; otherwise the build prints exactly what is short and the level is listed
  as "not built yet" on the root page. A half-built level on the site reads as broken links, not as
  work in progress — that is why the gate is strict.
- **Routes are level-prefixed** (`l3/chapter/week-07.html`). `build_route_map()` maps every source
  path → route across *all* levels first, so cross-level markdown links resolve. `make_resolver()`
  emits `unavailable:` for anything outside the generated site; the build counts these and renders
  them inert rather than as broken links.
- **`parse_weeks()` locates the type column rather than trusting an index**, because the plan tables
  differ per level: L1 has 6 columns, L2 adds "New syntax" (7), L3 adds "New maths" too. Keep that
  property if you touch it.
- **Encryption.** Both passcodes derive AES-256 keys via PBKDF2-HMAC-SHA256 (250k iterations) from
  one shared salt. Student-tier pages are encrypted under the student key, teacher-tier under the
  teacher key, and the student key is *also* stored wrapped under the teacher key — so one teacher
  unlock opens both tiers, but a student passcode cannot go the other way. Only the root
  `index.html` is plaintext; every other page ships as a ~20 KB shell with an empty content element.
  Browser side is WebCrypto in `assets_src/app.js`; keys live in `sessionStorage`.
- **The markdown renderer is deliberately not general-purpose.** It covers exactly the dialect this
  course uses. Three invariants exist because all three were real bugs:
  - Inline patterns are compiled once and matched with an explicit `pos` — **never against
    `text[i:]`**, which copies the string tail per character and made a 99 KB Level 2 file hang.
  - The paragraph branch **always consumes at least one line**, so the main loop cannot stall on a
    content shape no branch handles.
  - A run of lines starting with `|` that is *not* a table is captured as preformatted ASCII art.
    Without this, an unfenced pointer diagram in L2 week 1 spun the renderer forever.
- Progress-tracking `localStorage` keys are namespaced per level (`aia-done-l3`), because week 5 of
  Level 1 and week 5 of Level 3 are different weeks.

## Course content conventions

Every weekly file follows a fixed section order marked with emoji. Each level settled into its own
consistent dialect (L3 adds 🔢 for maths sections); **match the surrounding files rather than
inventing a variant** — mid-file drift is worse than either choice.

Hard rules the content depends on:

- **Level 1 contains zero code.** Unplugged activities, Teachable Machine, Scratch, Quick Draw,
  spreadsheets. Verified: the only fenced languages in L1 are `svg`, `markdown`, `bash`.
- **Level 2 is Python 3 + numpy/pandas/matplotlib/scikit-learn.** No seaborn, no torch.
- **Level 3 adds PyTorch — and is fully offline.** `pip` is blocked by a corporate proxy (403) and
  **`torchvision` is not installed and cannot be**. Image work uses `sklearn.datasets.load_digits()`
  (1797 8×8 digits) and numpy-generated images. CIFAR-10/torchvision appear only inside optional
  "when you have internet" callouts and nothing may depend on them. This deliberately diverges from
  reference `module-07-cnns-for-images.md`, which trains on CIFAR-10.
- **Ladders are the pacing control, and they are enforced.** `36-week-course/README.md` holds a
  **syntax ladder** (L2, L3) and a **maths ladder** (L3): max ~4 new constructs and at most one new
  mathematical idea per week, and nothing may be used before its week. Check the ladder before using
  `zip`, `enumerate`, comprehensions, f-strings, `@`/matmul, `requires_grad`, "gradient", "variance".
- **Maths is introduced numerically before it is named** (L3). A derivative is "how steep is this
  hill right here", computed with a tiny step and checked against the symbolic answer. No limits, no
  proofs, no chain-rule-as-symbol-manipulation. The teacher is assumed not to know calculus.
- **No term is used before it is defined**, across the whole arc.
- **Never hand the student a teacher file.** Teacher guides contain every answer and name the
  mistakes the student is expected to make.
- **Outputs in markdown must be real, and seeded.** Blocks are meant to have been executed and their
  actual stdout pasted. Any printed number derived from randomness must set a seed. Invented or stale
  output is the defect class that has bitten this repo most — e.g. `round(48.0996, 2)` documented as
  printing `48.1` when Python prints `48.10`.
- **Errors are curriculum.** Many blocks are *deliberately* broken to teach traceback reading (L2
  week 25 typos `ax.set_xlable` on purpose, with a checklist item saying so). Before "fixing" a
  failing block, read the surrounding prose — you will usually find it is intentional.
- **Figures diagram the mental model, never screenshot the code** (and in L3, never a formula
  either — they show what the formula does to numbers). Each level's
  `36-week-course/figures/STYLE.md` is the binding spec: palette by role, `viewBox` only with no
  `width`/`height`, `role="img"` + `<title>` + `<desc>`, 12px type floor, no external references,
  colour never the only carrier of meaning.
- **Alt text and `<title>` play different roles** and may differ: alt describes *what is drawn* for a
  screen reader, `<title>` states *what it means*. (An earlier spec demanded they match word for
  word; 67 embeds usefully didn't, so the rule was amended rather than the content degraded.)

## Verifying content

After editing course markdown, these are the checks that actually catch things.

**Executing every Python block.** One process per *file*, exec'ing blocks sequentially into one
shared `globals()` dict — linear. Do **not** re-run accumulated blocks per block; that is quadratic
and will appear to hang. Set `MPLBACKEND=Agg` and `stdin=DEVNULL` (so `input()` raises `EOFError`
instead of blocking forever) and a per-file timeout. Expect **only ~54% to run clean, and that is
correct**: failures decompose into deliberate broken examples, "add this to the file" fragments,
imports of learner-created modules, `NameError` cascades from an earlier failure in the same file,
and blocks that wait on `input()` or start a server. Triage before believing any of them is a bug.

```bash
# SVG contract, across a level
python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" <file.svg>
# plus: <title>, <desc>, role="img", viewBox present; no width/height on root;
#       no <image|http|@font-face|<script|<foreignObject

# Broken links: crawl dist/ AND the decrypted page bodies — most in-content links live inside
# ciphertext once built, so a plain HTML crawl sees under a third of them.
```

Last full verification (2026-09-23), independently re-run rather than trusted from build reports:
324 weekly files with zero truncated/thin, 1,140 SVGs all valid, 5,001 markdown links and 1,747
figure embeds with 0 broken, nav chains intact across all 9 book×level combinations, offline
guarantee holding (91 network-ish hits: 39 prohibitions, 48 localhost, 2 optional callouts, 0 real
dependencies), and all 5,171 Python blocks executed with **no confirmed real bugs**.

## Building or extending a level

A taught level is far too large to author inline. Levels 1–3 were each built with a background
`Workflow`: a planner agent (which writes the README and the ladders) plus a design-system agent,
then **three** authoring stages per 3-week block — teacher guide → student guides → workbooks — then
extras, then an audit. Two lessons are load-bearing:

- **Three stages, not two.** Teacher files run 1,500–1,800 lines / ~100 KB. A stage that read a
  teacher file *and* wrote 6 files stalled repeatedly ("no progress for 180000ms" × 6 attempts).
  Downstream stages must `grep` + offset-read the teacher file, never read it whole.
- **Batch to ~3 concurrent blocks.** The account enforces **$300/day** and **160 requests/4 min**.
  Twelve concurrent authoring agents blow the rate limit and die mid-write, producing nothing.
- **Run the audit as its own workflow on a fresh day.** As the last phase it was starved by the
  budget on every Level 3 run and never executed.

Each level costs roughly **$900–1,200** (three to four days at the cap).

## Known state and gaps

- **L3 weeks 34–36 were renumbered (2026-10-02) to real, measured output** of the reprinted pizza
  corpus. The reference project ships at **threshold 0.65**: the real cost sweep (cost = 10·fp + fn
  on 16 validation rows) ties 0.65 and 0.70 at 4, tie-break to the lower; 0.55 can never win because
  0.50 dominates it. The reference build is reproducible by extracting the Answer Key code from
  `teacher-guide/week-34.md` and `week-35.md` (set `--threshold` default 0.65). The 111-request log
  figures (76/35 labels, mean p 0.4546, band 16 of 111 = 14.4%, mean OOV 0.1795) come from a real
  111-request run (20× `cold food and a rude driver` plus 91 other reviews; exact mix not printed in Week 35); latency figures are
  machine-dependent. Not verified: `projects/capstone.md` keeps its own threshold (0.50) and traps,
  and its Milestone 6 code uses `DOCS`/`LABELS` that exist nowhere else in the repo. The `tiny_v1`/`tiny_v2` toys in workbooks 34–35 are
  separate and still use 0.55 on purpose.
- **L3 audit (2026-10-03):** structure, 1,447 links, 366 SVGs, nav chains, the figure audit
  (0 findings) and a decrypted-site crawl (402 pages, 6,826 links) are all clean. Findings handled:
  ~19 constructs appear before their syntax-ladder week — now listed in the level README's "Used ahead
  of the ladder" table (the four-a-week cap stops the ladder absorbing them; most are explained in-week,
  the rest are unchecked); the capstone's `COST_FN`/`COST_FP` comments were swapped relative to its card
  (fixed). The capstone's "real output" blocks still come from a separate 80-review corpus
  (threshold 0.50) that is not in the repo, and its price direction (fine-comment-called-negative = 10)
  is deliberately the opposite of Week 34's.
- **No SVG has ever been visually rendered.** Validity is contract-checked only. Each level has a
  `figures/_preview.html` for eyeballing.
- L3 figure fixes were applied to `.svg` files directly, so re-running `figures/_generator/` would
  overwrite them.
- ~1,600 of L2's and a similar share of L3's Python blocks have no adjacent output to diff against —
  verified to run, but nothing asserted about their values.
- There is no `.gitignore`, so generated output is committed: `site-app/dist/` (~2,060 files) and
  17 `__pycache__` files are tracked. Rebuilding or running the figure generators dirties the
  working tree with regenerated files — expect large diffs and don't commit them by accident.
- `site/index.html` (the old single-file 4-level map) and each level's
  `36-week-course/site/index.html` are hand-authored pages that predate `site-app/` and are **not**
  generated by it. They can drift.
- **Level 4 has a plan, a kit and patched modules, but no weekly files.** Done (2026-10-03):
  `36-week-course/README.md` (syllabus, both ladders, phasing, ~$1,400–2,150); stage 0b `_ledger/` (every
  reference script run offline on CPU, real outputs, defect list); 0c `l4lib/` (six unit-tested modules,
  every stand-in labelled "stand-in, not a model"); figure `STYLE.md` + fixed `_gen_audit.py`; 0d the nine
  reference modules patched offline against the ledger (each ends in a "Patch log"). The ledger showed the
  original modules had real defects (e.g. M8's rules baseline is 25/30 not 17/30, which flipped its lesson).
  **Wave A done (weeks 1–9: 27 files, 2026-10-04, executed and ladder-checked, no figures yet).**
  **Not done:** waves B–D (weeks 10–36) and figures — so `_level_is_complete()` keeps L4 off the site — and the plan's "Decisions the owner must make" remain
  as recommended-but-unconfirmed. Known leftovers: `_ledger/scripts/rag.py` has an unused
  `MiniLMEmbedder` that would download weights; M7's `build_registry` is missing (breaks M9/capstone
  imports in the ledger); M6's in-corpus note still says "about 4.5 for GPT-2"; the M1/M3/M8 patch
  runs produced some numbers (batch-size, dropout, SNEAKY Jaccard tables) that are not in the ledger.
  Wave A open items: `teacher-guide/week-03.md` calls `trace()` (~line 236) before defining it (~446);
  teacher-only snippets in weeks 4–6 use constructs the ladder lists later (`torch.arange`, `masked_fill`,
  `cdist`, `quantile`, `torch.randint`); the ladder lists `torch.cat` as new in W12 but L3 W27 has it;
  workbooks end with a student-facing folded ANSWERS page (decide if wanted); week-8 uses `.data =`,
  which is not a ladder row.
