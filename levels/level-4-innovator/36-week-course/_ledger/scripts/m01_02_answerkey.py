import time, math
from m01_lib import *
_T=time.time()
def sec(t): print(f"\n##### {t}  (t+{time.time()-_T:.1f}s)")
sec("Practice 1: lr cliff (block 6)")
for lr in [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
    run(f"adamw lr={lr}", lr=lr)
sec("Practice 2: predict the curve shape (configs stated in Practice 2)")
run("lr=1e-6", lr=1e-6, epochs=60)
run("lr=0.5", lr=0.5, epochs=60)
run("dropout=0.8", dropout=0.8, epochs=60)
run("lr=3e-3 epochs=5", lr=3e-3, epochs=5)
sec("Practice 3: linear scaling (block 7)")
for bs, lr in [(32,1e-3),(64,1e-3),(64,2e-3),(128,1e-3),
               (128,4e-3),(256,1e-3),(256,8e-3)]:
    run(f"bs={bs} lr={lr}", batch_size=bs, lr=lr)
sec("Practice 3: fixed-steps (block 8)")
for bs in [32, 64, 128, 256]:
    epochs = int(60 * bs / 64)      # constant total step count
    run(f"bs={bs} fixed-steps", batch_size=bs, lr=1e-3 * bs / 64, epochs=epochs)
sec("Practice 4: grad norm (blocks 10)")
h_ok   = run("lr ok",   lr=3e-3)
h_high = run("lr high", lr=0.3)

plt.figure(figsize=(7,4))
plt.plot(h_ok["gnorm"],   label="lr=3e-3")
plt.plot(h_high["gnorm"], label="lr=0.3")
plt.yscale("log"); plt.xlabel("epoch"); plt.ylabel("grad norm")
plt.legend(); plt.savefig("gnorm_lr.png", dpi=110); plt.close()

h_plain = run("depth12 plain", depth=12, residual=False, epochs=40)
h_res   = run("depth12 res",   depth=12, residual=True,  epochs=40)
print("gnorm first/last epoch  lr ok :", round(h_ok["gnorm"][0],3), round(h_ok["gnorm"][-1],3))
print("gnorm first/last epoch  lr .3 :", round(h_high["gnorm"][0],3), round(h_high["gnorm"][-1],3))
print("gnorm max  lr ok / lr .3     :", round(max(h_ok["gnorm"]),3), round(max(h_high["gnorm"]),3))
for nm,h in (("depth12 plain",h_plain),("depth12 res",h_res)):
    print(nm,"gnorm first/last", round(h["gnorm"][0],4), round(h["gnorm"][-1],4), "train loss first/last", round(h["train"][0],3), round(h["train"][-1],3))
import m01_lib; model = m01_lib.LAST_MODEL   # LEDGER: fragment assumes a `model` variable
first_block_norm = model.blocks[0].fc.weight.grad.norm().item()
print("block0 fc.weight grad norm (last model = depth12 res):", first_block_norm)
sec("Practice 5: LR range test (block 11)")
import math

def lr_range_test(min_lr=1e-7, max_lr=1.0, steps=200, batch_size=64, seed=0):
    torch.manual_seed(seed)
    model = MLP().to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=min_lr)
    lossf = nn.CrossEntropyLoss()
    gamma = (max_lr / min_lr) ** (1 / steps)      # multiply lr by this each step
    lrs, losses, smooth = [], [], None
    g = torch.Generator(device="cpu").manual_seed(seed)

    for s in range(steps):
        idx = torch.randint(0, len(Xtr), (batch_size,), generator=g).to(DEVICE)
        loss = lossf(model(Xtr[idx]), ytr[idx])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        cur = min_lr * (gamma ** s)
        # exponential smoothing so the curve is readable
        smooth = loss.item() if smooth is None else 0.9 * smooth + 0.1 * loss.item()
        lrs.append(cur); losses.append(smooth)
        for pg in opt.param_groups:
            pg["lr"] = min_lr * (gamma ** (s + 1))
        if smooth > 4 * min(losses):              # diverged; stop early
            break

    plt.figure(figsize=(7, 4))
    plt.plot(lrs, losses)
    plt.xscale("log"); plt.xlabel("learning rate"); plt.ylabel("smoothed loss")
    plt.title("LR range test"); plt.tight_layout()
    plt.savefig("lr_range_test.png", dpi=110); plt.close()
    best = lrs[int(np.argmin(losses))]
    print(f"loss minimum at lr={best:.2e}  ->  suggested lr={best/10:.2e}")
    return best / 10

suggested = lr_range_test()
run("suggested", lr=suggested)
run("default 3e-3", lr=3e-3)
sec("Practice 6A: tiny batches (block 12)")
run("bn bs=2", norm="batch", batch_size=2, epochs=30)
run("ln bs=2", norm="layer", batch_size=2, epochs=30)
sec("Practice 6B: shifted validation, 2x2 (block 13 + ledger harness: train normally, then eval)")
Xva_shift = Xva + 1.5        # every validation feature shifted by 1.5 sd

def eval_on(model, Xv, yv):
    model.eval()
    with torch.no_grad():
        logits = model(Xv)
        return (nn.CrossEntropyLoss()(logits, yv).item(),
                (logits.argmax(1) == yv).float().mean().item())
for nm in ("batch","layer"):
    run("train "+nm, norm=nm)                 # LEDGER harness: default knobs
    mdl = m01_lib.LAST_MODEL
    print(f"  {nm:5s} matched : loss/acc {eval_on(mdl, Xva, yva)}")
    print(f"  {nm:5s} shifted : loss/acc {eval_on(mdl, Xva_shift, yva)}")
