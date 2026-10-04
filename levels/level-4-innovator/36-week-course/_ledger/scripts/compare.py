"""compare.py"""
from evalset import LABELS
from scorer import report


def compare(before, after, min_n=5, drop_threshold=0.10):
    print(f"\n{'category':14s} {'n':>3s} {'before':>8s} {'after':>8s} {'delta':>8s}")
    print("-" * 46)
    regressions = []
    for cat in LABELS:
        cb, n, ab = before["per_category"][cat]
        ca, _, aa = after["per_category"][cat]
        d = aa - ab
        flag = ""
        if n >= min_n and d <= -drop_threshold:
            flag = "  <-- REGRESSION"
            regressions.append((cat, n, ab, aa, d))
        print(f"{cat:14s} {n:3d} {ab:8.3f} {aa:8.3f} {d:+8.3f}{flag}")
    print("-" * 46)
    d_all = after["overall"] - before["overall"]
    print(f"{'OVERALL':14s} {before['n']:3d} {before['overall']:8.3f} "
          f"{after['overall']:8.3f} {d_all:+8.3f}")

    # decompose the headline delta into per-category contributions
    print("\ncontribution of each category to the overall delta:")
    for cat in LABELS:
        cb, n, ab = before["per_category"][cat]
        _, _, aa = after["per_category"][cat]
        print(f"  {cat:14s} (n/N = {n}/{before['n']}) x {aa - ab:+.3f} "
              f"= {n / before['n'] * (aa - ab):+.4f}")

    if regressions:
        print(f"\n🚨 {len(regressions)} REGRESSION(S) — do not ship on the average alone:")
        for cat, n, ab, aa, d in regressions:
            print(f"   {cat}: {ab:.3f} -> {aa:.3f} ({d:+.1%} on n={n})")
    else:
        print("\n✅ no category with n>=5 dropped by more than 10 points")
    return regressions

