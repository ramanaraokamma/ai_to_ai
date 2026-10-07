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
**All four levels have the taught edition** (36 weeks × teacher guide / student guide / workbook, plus extras). Level 4 was written offline and has its own plan, shared kit and ledger — see "Known state".

Top-level orientation docs live at the repo root, not under `levels/`: `README.md`,
`START_HERE.md`, `CURRICULUM_MAP.md`, `RESOURCES.md`, and `teacher-guide/`. `site-app/README.md`
documents the generator.

Scale, so you know what you are touching: ~550 markdown files, ~680,000 lines, ~1,360 SVGs. Each
taught level is 120 files / 36 weeks. Do not attempt whole-level edits inline —
see "Building a level" below.

## Commands

```bash
# Build + serve the website (all complete levels). Binds 127.0.0.1 only — nothing is published.
# serve.sh runs serve.py, which resolves extensionless URLs the way Cloudflare Workers does —
# plain `python3 -m http.server` will 404 on every generated link.
./site-app/serve.sh                  # → http://localhost:8000/
./site-app/serve.sh 9000             # different port
./site-app/serve.sh --rebuild        # regenerate first, after editing course markdown

# Build only  (~3 s for four levels)
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

## Quality gates and the review pipeline

Three tools live in `levels/` and are the way to check a change; all run from the repo root.

```bash
python3 levels/check_structure.py [level-N-name ...]       # 36x3 files present, links resolve, SVG contract, every fig embedded
python3 levels/polish_check.py FILE ...                    # content-safety gate for presentation edits (vs git HEAD)
python3 levels/polish_check.py --hygiene-only FILE ...     # heading/fence/whitespace hygiene only, no baseline
```

`polish_check.py` fails on any change to a fenced code block body, a link/figure target, or a number
in the prose (digits inside file names are ignored), and enforces: one H1, no skipped heading level, every
fence closed and language-tagged, no tabs, trailing spaces or 3+ blank lines. **Commit before polishing** —
it compares against `HEAD`. `levels/PRESENTATION-SPEC.md` is the binding brief for presentation work
(invariants + the standard); its rules that matter most: no sentence that hints at an exercise's answer,
no new claims, section purpose lines say what a section is *for* not what it will prove.

All 432 weekly files pass `--hygiene-only` and `check_structure.py` passes for all four levels. Each level's
figure audit (`figures/_generator/_gen_audit.py`; L2, L3, L4 only) prints 0 findings. Running the audit or a
generator rewrites tracked `__pycache__` files in L2/L3 — restore them with `git checkout --`.

**What every level has been through (2026-10).** (1) A *per-week subject-matter review*: one agent per week
reading all three books for whether the teaching is *true* — recomputing hand arithmetic, reading code against
its prose, checking overclaims. Claims checked / high-severity found: L1 2,861 / 46, L2 3,460 / 43,
L3 3,246 / 61, L4 2,757 / 6. These were real errors invisible to the earlier execution/number audits (a
false equivalence between two averages, a harmonic-mean rule taught backwards, an impossible activity goal,
"three orders of magnitude" for a factor of 100). (2) *Teacher-key realignment* (L1–L3): every teacher
guide's homework script and Answer Key had been written against a workbook layout that never shipped (invented
"Page W.N" labels; the key covered a third of the real sections). All 108 keys were rewritten from each
workbook's own Answers section; coverage of workbook answer values in the key rose from ~0.70 to ~0.96.
**This class of bug — two files that disagree — is invisible to per-file audits; check across the three books.**
(3) A *content-safe presentation polish* of all 432 weekly files, each block followed by a reviewer who reads the
diff for meaning drift (they reverted 78 hunks in total across the four levels: invented sentences, answer-leaking "Look at…" lines,
dropped numbers). Depth is uneven — roughly half of the file reports describe a light pass, mostly because the
files were already well structured. (4) A *close-reading verification*: polishers log in-passing observations;
they were re-checked by recomputation (L1–L4: 410 notes → 76 real defects, 70 fixed).

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

**Open decisions that need the owner** (agents correctly declined to guess):
- **L4 Week 23** urgency labels for tickets t3 and t8: the written spec in `RULES` favours urgency 3 for
  both (double charge = money at risk; locked out = blocked), so the lesson claim "the specification does
  not decide" is wrong as written — reword it, or relabel the gold and refreeze with a new fingerprint.
- **L3 Week 30** whether to rename the "Dark & Tannic" cluster (spans 3 books, a figure and code).
- **L3 Weeks 35–36** latency figures come from mixed runs; pick one canonical run and re-render
  fig-w35-5 / fig-w36-1/2/4/6.
- **L1 Week 12** the best `mass_g` cut scores 11/12, not 10/12 (changes a ranking table, a scoreboard and
  the bar figures); **Week 16** the worked-example stapler (74/15/11) gives away the card-6 surprise (99/1/0);
  **Week 18** the "husky in the snow" single-background mechanism was only hedged, and Experiments 2–3 use
  ~15 photos per class against a 40-per-class baseline.
- **L4 plan decisions** ("Decisions the owner must make" in `level-4-innovator/36-week-course/README.md`)
  are recommended-but-unconfirmed: learner age 15–16, `tokenizers` allowed in Week 20 only, the
  "stand-in, not a model" banner on site pages.

**Known limits**
- **No SVG has ever been visually rendered** (headless Chrome is blocked by the sandbox). Validity is
  contract-checked only and the audit cannot see text overflowing a box. Each level has
  `figures/_preview.html` for eyeballing. L4 has ~108 figures vs L3's ~365 — a lean first pass.
- **L1 has no figure generator, and many L2/L3 figure fixes were applied to the `.svg` directly**, so
  re-running those generators would overwrite them. L4 figures are generated: change the module in
  `figures/_generator/` and run `python3 _gen_build.py` there (deterministic, byte-identical) — never
  edit an L4 SVG alone.
- ~1,600 of L2's, a similar share of L3's, and many of L4's Python blocks have no adjacent output to diff
  against — verified to run, nothing asserted about their values.
- The polish is uneven in depth (see above); the remaining low-severity review findings (hundreds across the
  four levels, mostly judged taste calls) are not applied.
- **Level 4 specifics.** Its reference modules were patched offline against `_ledger/` (every reference
  script run on CPU; the originals had real defects — e.g. M8's rules baseline is 25/30 not 17/30), shared
  code is `l4lib/` (unit-tested; every scripted stand-in says "stand-in, not a model"). Weekly files have
  no prev/next nav links, only "Next Week Preview" prose. Known leftovers: `_ledger/scripts/rag.py` has an
  unused `MiniLMEmbedder` that would download weights; M6's in-corpus note still says "about 4.5 for GPT-2";
  some M1/M3/M8 numbers came from patch-agent runs and are not in the ledger; the README ladder rows for
  W17 `torch.randint` and W22 `.detach()` still list them as new though used earlier (see "Ladder
  amendments"); Week 22 still says `nn.Parameter` "comes in Week 31".
- **L3 weeks 34–36** ship the reference project at **threshold 0.65** (real cost sweep, cost = 10·fp + fn
  on 16 validation rows, ties 0.65/0.70 at 4, lower taken; 0.55 can never win because 0.50 dominates it).
  Reproduce the build by extracting the Answer Key code from `teacher-guide/week-34.md` and `week-35.md`.
  `projects/capstone.md` deliberately prices mistakes the other way (fine-comment-called-negative = 10) and
  its "real output" comes from a separate 80-review corpus (threshold 0.50) not in the repo.
- L3 uses ~19 constructs ahead of their syntax-ladder week (README "Used ahead of the ladder"); L4's
  README has "Ladder amendments" and a further list from the final audit.
- There is no `.gitignore`, so generated output is committed: `site-app/dist/` (~2,000+ files; every rebuild
  re-encrypts all pages under a new salt → ~800-file diffs, commit it separately) and 17 `__pycache__` files.
- `site/index.html` (the old single-file 4-level map) and each level's `36-week-course/site/index.html`
  are hand-authored pages that predate `site-app/` and are **not** generated by it. They can drift.

**Workflow lessons (from the 2026-10 runs).**
- A gateway 502 ("floodgate … ENOTFOUND") kills agents mid-run; resume with the same `resumeFromRunId`
  (finished agents replay from cache). Edit a verify prompt before resuming or its cached result is stale.
  If `scriptPath` is rejected, resend the script inline.
- Pipelined lanes verify concurrently, so a verifier can run before a sibling lane's files exist — run
  dependent blocks (a capstone) after the blocks they reuse, and finish with a cross-block reference check.
- Agents repeatedly: create empty typo files `eek-*.md` (delete them); delete tracked `__pycache__` outside
  their scope; add answer-leaking lines when told to "say what to look at"; edit an SVG directly so the next
  generator run silently undoes it. Tell them what they may delete, and check `git status` and
  `git ls-files -d` after every run.
- A per-file "light pass" cannot be seen by any gate; ask agents to say honestly when their pass was limited.
- Don't rely on a check script in `/tmp` — it disappeared once and two "links intact" claims rested on it.
  Keep tools in the repo (`levels/`).
