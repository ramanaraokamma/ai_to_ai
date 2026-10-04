# LEDGER helper for ablations / mask / sinusoidal scripts

import time, math
import torch
from m03_lib import *
import m03_lib

@torch.no_grad()
def est(model, iters=20, block=None):
    model.eval(); out={}
    for split in ["train","val"]:
        ls=torch.zeros(iters)
        for k in range(iters):
            x,y=get_batch(split); _,l=model(x,y); ls[k]=l.item()
        out[split]=ls.mean().item()
    model.train(); return out

def fit(model, steps, eval_every=50, log=True):
    """Same optimiser/schedule as module-03 (AdamW 3e-4, wd .1, warmup 100, cosine), horizon = `steps`."""
    opt=torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
    WARM=100
    sched=torch.optim.lr_scheduler.LambdaLR(opt, lambda s:((s+1)/WARM if s<WARM else 0.5*(1+math.cos(math.pi*(s-WARM)/(steps-WARM)))))
    best=(9e9,-1); t0=time.time()
    for step in range(steps):
        x,y=get_batch("train"); _,loss=model(x,y)
        opt.zero_grad(set_to_none=True); loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step(); sched.step()
        if step%eval_every==0 or step==steps-1:
            lo=est(model)
            if lo["val"]<best[0]: best=(lo["val"],step)
            if log and (step%250==0 or step==steps-1): print(f"  step {step:4d} train {lo['train']:.3f} val {lo['val']:.3f}", flush=True)
    return best, lo, time.time()-t0
