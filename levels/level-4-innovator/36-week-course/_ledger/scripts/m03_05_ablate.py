import sys
from m03_train import *
name=sys.argv[1]
torch.manual_seed(1337)
import types
if name=="no_pos":
    class M(TinyGPT):
        def forward(self, idx, targets=None):
            B,T=idx.shape; x=self.tok_emb(idx)        # pos_emb removed
            for b in self.blocks: x=b(x)
            logits=self.head(self.ln_f(x)); loss=None
            if targets is not None: loss=F.cross_entropy(logits.reshape(-1,logits.size(-1)),targets.reshape(-1))
            return logits,loss
    model=M(V)
elif name=="one_head":  model=TinyGPT(V,n_head=1)
elif name=="one_layer": model=TinyGPT(V,n_layer=1)
else:
    model=TinyGPT(V)
    if name=="no_mlp":
        for b in model.blocks:
            b.forward=types.MethodType(lambda self,x: x+self.attn(self.ln1(x)), b)
    if name=="no_residual":
        for b in model.blocks:
            b.forward=types.MethodType(lambda self,x: self.ff(self.ln2(self.attn(self.ln1(x)))), b)
    if name=="no_scale":
        def fwd(self,x):
            B,T,C=x.shape; k,q,v=self.key(x),self.query(x),self.value(x)
            att=q@k.transpose(-2,-1)           # no * hs**-0.5
            att=att.masked_fill(self.tril[:T,:T]==0,float("-inf")); att=F.softmax(att,dim=-1)
            self.last_attn=att.detach(); return self.drop(att)@v
        for b in model.blocks:
            for h in b.attn.heads: h.forward=types.MethodType(fwd,h)
    if name=="no_mask":
        STEPS_OVERRIDE=500
        def fwd(self,x):
            B,T,C=x.shape; k,q,v=self.key(x),self.query(x),self.value(x)
            att=q@k.transpose(-2,-1)*k.shape[-1]**-0.5     # masked_fill removed
            att=F.softmax(att,dim=-1); self.last_attn=att.detach(); return self.drop(att)@v
        for b in model.blocks:
            for h in b.attn.heads: h.forward=types.MethodType(fwd,h)
model=model.to(DEVICE)
steps=500 if name=="no_mask" else 1500
print(name, "params", f"{sum(p.numel() for p in model.parameters()):,}", "steps", steps)
best,lo,sec=fit(model, steps)
print(f"RESULT {name}: best val {best[0]:.3f} @ step {best[1]}  final train {lo['train']:.3f} val {lo['val']:.3f}  ({sec:.0f}s train)")
if name=="no_mask":
    ctx=torch.tensor([[stoi["t"]]]); torch.manual_seed(0)
    print(repr(decode(model.generate(ctx,200,temperature=0.8)[0].tolist())))
