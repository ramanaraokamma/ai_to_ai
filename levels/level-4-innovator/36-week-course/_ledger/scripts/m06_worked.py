from m06_lib import *
import numpy as np
q="Why did post-norm need warmup?"
v=index.emb.v
print("vocab size:",len(v.vocabulary_), "M shape:",index.M.shape)
qv=index.emb.encode([q])[0]
names=v.get_feature_names_out()
for i in np.nonzero(qv)[0]: print(f"  {names[i]:10s} {qv[i]:.4f}")
print("analyzer tokens:", v.build_analyzer()(q))
sims=index.M@qv
for i,s in enumerate(sims): print(f"chunk {i:2d} {titles[i][13:]:30s} {s:.3f}")
print("zeros:",int((sims==0).sum()), "best/second:", sorted(sims)[-1]/sorted(sims)[-2])
print("words NOTEBOOK:",len(NOTEBOOK.split()),"chunk words:",sum(len(c.split()) for c in chunks))
print("tokens approx (words*1.3):",len(NOTEBOOK.split())*1.3)
# cost arithmetic
print("long ctx:",200000*10000/1e6*2.0,"rag:",1000*10000/1e6*2.0,"ratio",(200000*10000)/(1000*10000),"cached ~",200000*10000/1e6*2.0/10)
print("step8:",161/1e6*2,58/1e6*10,161/1e6*2+58/1e6*10,"paste:",950/1e6*2+58/1e6*10, (950/1e6*2+58/1e6*10)/(161/1e6*2+58/1e6*10))
print("eight-point-five:",0.596/0.070)
# Gate: GPU question
print("GPU q top-1:",index.search("Which GPU did I train the tiny GPT on?",1)[0][:2])
# context sent for Q7 tokens via stub counter
import stub_anthropic as sa
