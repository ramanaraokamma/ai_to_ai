# calibration.py — is "definitely" worth anything?
# Needs numpy. No API key, no cost. Data is 40 real-shaped results typed inline.
import numpy as np

# (confidence the system expressed as a number, was it actually correct 0/1)
RESULTS = [
    (0.95, 1), (0.95, 1), (0.95, 0), (0.95, 1), (0.95, 1), (0.95, 0),
    (0.95, 1), (0.95, 0), (0.95, 1), (0.95, 1), (0.95, 0), (0.95, 1),
    (0.75, 1), (0.75, 1), (0.75, 0), (0.75, 1), (0.75, 1), (0.75, 1),
    (0.75, 0), (0.75, 1), (0.75, 1), (0.75, 0), (0.75, 1), (0.75, 1),
    (0.75, 1), (0.75, 0), (0.75, 1),
    (0.55, 1), (0.55, 0), (0.55, 1), (0.55, 0), (0.55, 1), (0.55, 0),
    (0.55, 0), (0.55, 1),
    (0.05, 0), (0.05, 0), (0.05, 0), (0.05, 0), (0.05, 0),
]

conf = np.array([c for c, _ in RESULTS], dtype=float)
correct = np.array([y for _, y in RESULTS], dtype=float)
n = len(RESULTS)

print(f"{'bucket':<10} {'n':>4} {'stated':>8} {'actual':>8} {'gap':>8}")
print("-" * 42)

ece = 0.0                                   # expected calibration error
for lo, hi, label in [(0.90, 1.01, "0.90-1.00"),
                      (0.70, 0.90, "0.70-0.89"),
                      (0.50, 0.70, "0.50-0.69"),
                      (0.00, 0.50, "0.00-0.49")]:
    mask = (conf >= lo) & (conf < hi)
    k = int(mask.sum())
    if k == 0:
        continue
    stated = conf[mask].mean()              # what it claimed
    actual = correct[mask].mean()           # what it delivered
    gap = actual - stated
    ece += (k / n) * abs(gap)               # weight each bucket by its size
    print(f"{label:<10} {k:>4} {stated:>8.3f} {actual:>8.3f} {gap:>+8.3f}")

brier = float(np.mean((conf - correct) ** 2))
print("-" * 42)
print(f"expected calibration error (ECE) = {ece:.4f}")
print(f"Brier score                      = {brier:.4f}   (lower is better)")
print(f"overall accuracy                 = {correct.mean():.4f}")

