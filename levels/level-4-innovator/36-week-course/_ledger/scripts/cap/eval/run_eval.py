# eval/run_eval.py — python eval/run_eval.py
import sys, statistics
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from spine import answer                          # noqa: E402
from guards import BudgetGuard                    # noqa: E402
from cases import CASES                           # noqa: E402
from score import score_case                      # noqa: E402

budget = BudgetGuard(limit_usd=0.50)               # the whole run is capped
rows, by_cat = [], defaultdict(list)

for case in CASES:
    ans = answer(case["q"], budget=budget)
    ok, reason = score_case(case, ans)
    rows.append((case, ans, ok, reason))
    by_cat[case["category"]].append(ok)
    mark = "✅" if ok else "❌"
    print(f"{mark} {case['id']:4s} {case['category']:13s} "
          f"{ans.route:9s} ${ans.cost_usd:.5f} {ans.latency_s:5.2f}s  {reason}")

overall = sum(ok for *_, ok, _ in rows) / len(rows)
print(f"\n{'category':15s} {'n':>3s} {'score':>7s}")
for cat, oks in sorted(by_cat.items()):
    print(f"{cat:15s} {len(oks):3d} {sum(oks)/len(oks):7.2f}")
print(f"{'OVERALL':15s} {len(rows):3d} {overall:7.2f}")

lat = sorted(a.latency_s for _, a, _, _ in rows)
cost = [a.cost_usd for _, a, _, _ in rows]
pct = lambda v, p: v[max(0, min(len(v) - 1, round(p / 100 * len(v)) - 1))]
print(f"\ncost  mean ${statistics.mean(cost):.5f}  p95 ${pct(sorted(cost), 95):.5f}")
print(f"lat   p50 {pct(lat, 50):.2f}s        p95 {pct(lat, 95):.2f}s")
print(f"spend {budget.spent:.4f} of {budget.limit:.2f}")

