from m03_lib import *
model = TinyGPT(V).to(DEVICE); model.load_state_dict(torch.load("tiny_gpt_m03.pt"))
print("loaded trained model, params", sum(p.numel() for p in model.parameters()))
def head_stats(model, text_sample):
    idx = torch.tensor([encode(text_sample)], device=DEVICE)
    model.eval()
    with torch.no_grad():
        model(idx)
    T = len(text_sample)
    space_pos = [i for i, c in enumerate(text_sample) if c == " "]
    rows = []
    for li in range(N_LAYER):
        for hi in range(N_HEAD):
            a = model.blocks[li].attn.heads[hi].last_attn[0]      # (T,T)
            pos = torch.arange(T, device=a.device).float()
            look = (((pos.unsqueeze(0) - pos.unsqueeze(1)).abs() * a)
                    .sum(-1)[5:].mean().item())
            prev = a.diagonal(-1).mean().item()                   # weight on t-1
            first = a[:, 0].mean().item()                         # weight on pos 0
            sp = 0.0
            for qi in range(5, T):
                prior = [s for s in space_pos if s < qi]
                if prior:
                    sp += a[qi, prior[-1]].item()
            sp /= max(1, T - 5)
            rows.append((f"L{li}H{hi}", look, prev, first, sp))
    print(f"{'head':6s} {'lookback':>9s} {'prev':>7s} {'pos0':>7s} {'lastspace':>10s}")
    for r in rows:
        print(f"{r[0]:6s} {r[1]:9.2f} {r[2]:7.3f} {r[3]:7.3f} {r[4]:10.3f}")
    return rows

rows = head_stats(model, "the old man walked home along the river tonight")
import numpy as np
arr=np.array([[r[1],r[2],r[3],r[4]] for r in rows])
print("model-wide mean look-back", round(arr[:,0].mean(),2))
for li in range(4): print("layer",li,"mean look-back",round(arr[li*4:(li+1)*4,0].mean(),2))
print("max prev-char weight head:", rows[int(arr[:,1].argmax())][0], round(arr[:,1].max(),3), "; min look-back head:", rows[int(arr[:,0].argmin())][0], round(arr[:,0].min(),2))
