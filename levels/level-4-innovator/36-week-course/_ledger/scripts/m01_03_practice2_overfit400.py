from m01_lib import *
import m01_lib
# ------------------------------------------- 5. deliberately overfit
X2, y2 = make_spirals(n_per_class=600, noise=0.35, seed=1)
n2 = int(0.7 * len(X2))
Xtr_full = torch.tensor(X2[:n2], device=DEVICE)
ytr_full = torch.tensor(y2[:n2], device=DEVICE)
mu2, sd2 = Xtr_full.mean(0, keepdim=True), Xtr_full.std(0, keepdim=True)

Xtr, ytr = ((Xtr_full - mu2) / sd2)[:120], ytr_full[:120]   # only 120 examples!
Xva = (torch.tensor(X2[n2:], device=DEVICE) - mu2) / sd2
yva = torch.tensor(y2[n2:], device=DEVICE)


import m01_lib as _m
_m.Xtr,_m.ytr,_m.Xva,_m.yva=Xtr,ytr,Xva,yva   # run() reads module globals
h=run("120 ex, 400 epochs", epochs=400)
import numpy as np
print("best val", round(min(h["val"]),3), "@ epoch", int(np.argmin(h["val"])), "final val", round(h["val"][-1],3))
