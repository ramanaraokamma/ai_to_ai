"""dedup.py — run this BEFORE training, every single time."""
import re
from evalset import EVAL
from traindata import TRAIN_RAW


def toks(s):
    return set(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())


def jaccard(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def decontaminate(train, evalset, threshold=0.70, verbose=True):
    clean, removed = [], []
    for i, (t, y) in enumerate(train):
        worst = max(((jaccard(t, e), j, e) for j, (e, _) in enumerate(evalset)),
                    key=lambda x: x[0])
        if worst[0] >= threshold:
            removed.append((i, t, worst))
        else:
            clean.append((t, y))
    if verbose:
        print(f"contamination scan: {len(train)} train x {len(evalset)} eval")
        for i, t, (j, ei, e) in removed:
            kind = "EXACT" if j >= 0.999 else "NEAR "
            print(f"  {kind} train#{i:<3d} {t!r}\n"
                  f"        eval#{ei:<3d} {e!r}   Jaccard {j:.3f}")
        print(f"  removed {len(removed)}, kept {len(clean)}")
    return clean, removed


if __name__ == "__main__":
    TRAIN, _ = decontaminate(TRAIN_RAW, EVAL)

