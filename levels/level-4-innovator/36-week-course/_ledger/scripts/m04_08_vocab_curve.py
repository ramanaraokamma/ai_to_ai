import matplotlib.pyplot as plt
from bpe import BPETokenizer
from corpus import CORPUS

sizes = [256, 276, 306, 356, 406, 456, 556]
nbytes = len(CORPUS.encode("utf-8"))
xs, ys, merges = [], [], []

for vs in sizes:
    t = BPETokenizer().train(CORPUS, vocab_size=vs)
    n = len(t.encode(CORPUS))
    xs.append(vs); ys.append(nbytes / n); merges.append(len(t.merges))
    print(f"vocab {vs:4d}  merges {len(t.merges):4d}  tokens {n:5d}  b/tok {nbytes/n:.2f}")

sat = next(i for i in range(1, len(merges)) if merges[i] == merges[i - 1])

plt.figure(figsize=(7, 4))
plt.plot(xs, ys, "o-", label="bytes per token")
plt.axvline(256 + merges[sat], ls="--", c="crimson",
            label=f"training saturates at {merges[sat]} merges")
plt.xlabel("requested vocabulary size")
plt.ylabel("bytes per token (higher = better compression)")
plt.title("BPE compression vs vocabulary size on a 1,117-byte corpus")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig("vocab_curve.png", dpi=150); plt.close()
print("saved vocab_curve.png")
