import torch, torch.nn as nn
from lora import LoRALinear
torch.manual_seed(0)
base = nn.Linear(768, 768); x = torch.randn(4, 768)
l = LoRALinear(base, r=8, alpha=16)
print("step0 max |lora - base| :", (l(x) - base(x)).abs().max().item())
tr = sum(p.numel() for p in l.parameters() if p.requires_grad); fr = sum(p.numel() for p in l.parameters() if not p.requires_grad)
print("one 768x768 projection: trainable", tr, "frozen", fr, "ratio vs full 589,824 ->", round(tr/589824*100,2), "%")
opt = torch.optim.SGD([p for p in l.parameters() if p.requires_grad], lr=0.1)
y = torch.randn(4, 768)
for s in range(3):
    loss = ((l(x) - y)**2).mean(); opt.zero_grad(); loss.backward(); opt.step()
    print(f"step {s+1} loss {loss.item():.4f}  |B|={l.B.abs().max().item():.5f}  A.grad is None? {l.A.grad is None}")
print("base weight unchanged?", torch.equal(base.weight, l.base.weight), "requires_grad", base.weight.requires_grad)
