import time; _T=time.time()
from m02_lib import *
lstm, _ = train("lstm", verbose=False)
print("lstm final trained, elapsed", round(time.time()-_T,1))
@torch.no_grad()
def score(m, words):
    """Average per-character teacher-forced loss for each word."""
    m.eval()
    out = []
    for w in words:
        w = w[:MAXLEN - 1]
        ids = torch.tensor([encode(w)])
        inp = torch.full((1, MAXLEN), PAD, dtype=torch.long)
        inp[:, 1:] = ids[:, :-1]
        logits, _ = m(inp)
        loss = F.cross_entropy(logits.reshape(-1, V), ids.reshape(-1),
                               ignore_index=PAD)
        out.append(loss.item())
    return np.array(out)

real_scores = score(lstm, NAMES)
gen = [g for g in sample(lstm, 200, temperature=1.0, seed=7) if len(g) > 0]
gen_scores = score(lstm, gen)

print(f"real names   mean {real_scores.mean():.3f}  median "
      f"{np.median(real_scores):.3f}  n={len(real_scores)}")
print(f"generated    mean {gen_scores.mean():.3f}  median "
      f"{np.median(gen_scores):.3f}  n={len(gen_scores)}")
print(f"gap = {gen_scores.mean() - real_scores.mean():.3f} nats/char")

plt.figure(figsize=(7, 4))
bins = np.linspace(0, max(gen_scores.max(), real_scores.max()), 30)
plt.hist(real_scores, bins=bins, alpha=0.6, label="real names")
plt.hist(gen_scores, bins=bins, alpha=0.6, label="model's own samples")
plt.axvline(real_scores.mean(), ls="--")
plt.axvline(gen_scores.mean(), ls="--", color="C1")
plt.xlabel("per-character loss (nats)"); plt.ylabel("count"); plt.legend()
plt.tight_layout(); plt.savefig("exposure_bias.png", dpi=110); plt.close()
