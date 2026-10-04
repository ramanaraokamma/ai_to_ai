import numpy as np
# ex4: reconstruct from module's summary counts
rows=[(14,0.9,10),(11,0.7,8),(5,0.5,2)]
conf=np.array(sum(([c]*n for n,c,_ in rows),[]),float); y=np.array(sum(([1]*k+[0]*(n-k) for n,_,k in rows),[]),float)
ece=sum(n/30*abs(k/n-c) for n,c,k in rows)
print("ex4 ECE %.4f Brier %.4f acc %.4f"%(ece,np.mean((conf-y)**2),y.mean()))
# cost arithmetic in worked example
print("3100 in + 480 out:",3100/1e6*2+480/1e6*10)
# noise claim: sd of count out of 20 at p=.25
print("sd",(20*.25*.75)**.5)
# does tools.build_registry exist in module-7 tools.py?
import sys; sys.path.insert(0,'.')
try:
    from tools import build_registry
    print("build_registry exists")
except Exception as e: print("redteam.py import check:", type(e).__name__, e)
import agent, inspect
print("m07 run_agent return keys: answer, stop, iterations, spend, messages, trace  -> redteam uses trace['cost_usd'], trace['answer'] (KeyError / wrong type)")
