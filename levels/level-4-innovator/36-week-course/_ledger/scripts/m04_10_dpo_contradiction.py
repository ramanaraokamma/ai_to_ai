import torch
import torch.nn.functional as F

ref_logits = torch.tensor([0.4, 0.6, 1.2, 0.8])
ref_logp = F.log_softmax(ref_logits, dim=-1)

def run(pairs, beta=0.1, steps=300, lr=0.05):
    pl = torch.nn.Parameter(ref_logits.clone())
    opt = torch.optim.Adam([pl], lr=lr)
    for _ in range(steps):
        logp = F.log_softmax(pl, dim=-1)
        m = torch.stack([beta * ((logp[w] - ref_logp[w]) - (logp[l] - ref_logp[l]))
                         for w, l in pairs])
        loss = -F.logsigmoid(m).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return F.softmax(pl, -1).detach(), loss.item()

BASE = [(0, 3), (0, 2), (1, 2), (1, 3), (2, 3)]

p, l = run(BASE + [(0, 1), (1, 0)])
print("contradiction:", " ".join(f"{c}={p[i]:.3f}" for i, c in enumerate("ABCD")),
      f" loss={l:.4f}")

p, l = run([(0, 1), (1, 2), (2, 0)])
print("cycle        :", " ".join(f"{c}={p[i]:.3f}" for i, c in enumerate("ABCD")),
      f" loss={l:.4f}")
