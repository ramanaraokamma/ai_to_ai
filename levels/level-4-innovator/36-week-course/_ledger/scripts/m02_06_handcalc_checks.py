import math
# Practice 1 GRU by hand (module answer key)
sig=lambda x:1/(1+math.exp(-x))
h=0.0
for t,x in enumerate([1,0,0],1):
    z=sig(2*x-1); ht=math.tanh(1.5*x+0.5*h); h=(1-z)*h+z*ht
    print(f"t={t} z={z:.4f} htilde={ht:.4f} h={h:.4f}")
# Practice 2 softmax temperature
import torch, torch.nn.functional as F
lg=torch.tensor([3.0,2.0,1.0])
for T in (0.5,1.0,4.0): print("T",T,[round(v,3) for v in F.softmax(lg/T,-1).tolist()])
p=F.softmax(lg,-1); p2=p.clone(); p2[2]=0; p2=p2/p2.sum(); print("top-k=2 T=1",[round(v,3) for v in p2.tolist()])
print("0.95**400 =",0.95**400, " 0.982**40 =",0.982**40, " sigma(2),sigma(0) =",sig(2),sig(0))
# vocab line: temperature 0.579->0.831 and top-k example in vocabulary table
q=F.softmax(torch.tensor([2.0,1.0,0.5,0.0]),-1); print("[2,1,.5,0] T=1",[round(v,3) for v in q.tolist()])
q5=F.softmax(torch.tensor([2.0,1.0,0.5,0.0])/0.5,-1); print("[2,1,.5,0] T=.5",[round(v,3) for v in q5.tolist()])
qk=q.clone(); qk[2:]=0; qk=qk/qk.sum(); print("top-k 2",[round(v,3) for v in qk.tolist()])
