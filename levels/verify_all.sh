#!/usr/bin/env bash
# verify_all.sh — run every static gate in one go. Run from anywhere; exits non-zero if any gate fails.
#   levels/verify_all.sh            all gates
#   levels/verify_all.sh --quick    skip the (slower) text-fit pass
set -u
cd "$(dirname "$0")/.."
fail=0
step() { echo; echo "== $1"; shift; "$@" || { echo "!! FAILED: $*"; fail=1; }; }

step "structure (files, links, SVG contract, embeds)" python3 levels/check_structure.py
step "weekly-file hygiene (432 files)" python3 levels/polish_check.py --hygiene-only \
    levels/level-*/36-week-course/{teacher-guide,student-guide,workbook}/week-*.md
[ -f levels/check_cross_book.py ] && step "teacher key vs workbook answers" python3 levels/check_cross_book.py
[ -f levels/check_ladder.py ] && step "syntax ladder" python3 levels/check_ladder.py
for g in levels/level-2-builder levels/level-3-engineer levels/level-4-innovator; do
  step "figure audit $(basename "$g")" bash -c "cd $g/36-week-course/figures/_generator && python3 _gen_audit.py | tail -1 | grep -q -- '--- 0 finding' && echo '0 findings'"
done
git checkout -- '*.pyc' 2>/dev/null   # audits rewrite tracked __pycache__ files
[ "${1:-}" = "--quick" ] || step "text fit (measured)" python3 levels/check_text_fit.py --summary
echo; [ $fail = 0 ] && echo "ALL GATES PASSED" || echo "SOME GATES FAILED"
exit $fail
