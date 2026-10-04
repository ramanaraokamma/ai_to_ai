import torch
import torch.nn.functional as F

RESPONSES = ["A: numbered recipe, 6 lines, no filler",
             "B: correct recipe buried in 3 paragraphs of preamble",
             "C: vague answer that never lists ingredients",
             "D: refuses a harmless cooking question"]

# The frozen reference model (this is our "SFT model").
ref_logits = torch.tensor([0.4, 0.6, 1.2, 0.8])
ref_logp = F.log_softmax(ref_logits, dim=-1)

PAIRS = [(0, 3), (0, 2), (0, 1), (1, 2), (1, 3), (2, 3)]   # (chosen, rejected)


def run_dpo(beta, steps, lr=0.05, trace=False):
    policy_logits = torch.nn.Parameter(ref_logits.clone())
    opt = torch.optim.Adam([policy_logits], lr=lr)
    for s in range(1, steps + 1):
        logp = F.log_softmax(policy_logits, dim=-1)
        margins = torch.stack([
            beta * ((logp[w] - ref_logp[w]) - (logp[l] - ref_logp[l]))
            for w, l in PAIRS])
        loss = -F.logsigmoid(margins).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        if trace and s in (1, 50, 150, 300):
            p = F.softmax(policy_logits, -1).detach()
            print(f"  step {s:4d}  loss {loss.item():.4f}   probs " +
                  " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)))
    p = F.softmax(policy_logits, -1).detach()
    kl = (p * (torch.log(p) - ref_logp)).sum()          # KL(policy || reference)
    return p, kl.item(), loss.item()


ref_p = torch.softmax(ref_logits, -1)
print("reference policy:", " ".join(f"{RESPONSES[i][0]}={ref_p[i]:.3f}" for i in range(4)))
print("\nbeta = 0.2, 300 steps:")
run_dpo(0.2, 300, trace=True)

print("\nbeta sweep, all at 300 steps:")
for b in [0.02, 0.1, 0.5, 1.0, 5.0]:
    p, kl, l = run_dpo(b, 300)
    print(f"  beta {b:4.2f}  " +
          " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)) +
          f"   KL(pi||ref)={kl:.3f}  loss={l:.4f}")
