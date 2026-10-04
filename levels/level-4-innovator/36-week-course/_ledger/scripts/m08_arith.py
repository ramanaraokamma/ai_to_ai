from judge import cohen_kappa, kappa_label

# counts you get by comparing your own pass/fail labels with the judge's
k = cohen_kappa(both_pass=16, judge_pass_human_fail=6,
                judge_fail_human_pass=2, both_fail=6)
print(f"n={k['n']}  raw agreement p_o={k['p_o']:.4f}  chance p_e={k['p_e']:.4f}")
print(f"kappa = {k['kappa']:.4f}  ({kappa_label(k['kappa'])})")
print(f"judge pass rate {k['judge_pass_rate']:.3f} vs human {k['human_pass_rate']:.3f}"
      f"  ->  {'LENIENT' if k['judge_pass_rate'] > k['human_pass_rate'] else 'STRICT'}")
print(f"false passes {k['false_pass']}, false fails {k['false_fail']}")

print('--- X/Y'); 
for nm,a in [('X',(30,4,2,4)),('Y',(20,6,6,8))]:
    k=cohen_kappa(*a); print(nm, {x:round(v,4) if isinstance(v,float) else v for x,v in k.items()}, kappa_label(k['kappa']))
print('--- SNEAKY')
SNEAKY = [
    # eval#9  "is there a time limit on sending items back?"
    ("how many days do I have to post an unwanted product?",      "refund"),
    # eval#23 "what am I paying per month right now?"
    ("could you tell me my current monthly charge?",              "billing"),
    # eval#13 "clicking save does absolutely nothing"
    ("pressing the save button has no effect whatsoever",         "technical"),
    # eval#26 "how tall is Mount Kilimanjaro?"
    ("what is the elevation of Africa's highest peak?",           "out_of_scope"),
    # eval#20 "took the money twice on the 3rd"
    ("you debited my account two times earlier this month",       "billing"),
]

from dedup import jaccard
from evalset import EVAL

for text, _ in SNEAKY:
    best = max(((jaccard(text, e), e) for e, _ in EVAL), key=lambda x: x[0])
    print(f"{best[0]:.3f}  {text[:46]:48s} vs {best[1][:40]}")

# position-bias arithmetic from the module's stated counts
first=19+17; print("first-position wins",first,"/60 =",first/60)
print("consistent 22, flipped 8, flip rate",8/30, "v1 consistent 12/22 =",12/22, "naive 19/30 =",19/30)
print("first picks implied = consistent(22)*1 + 7*2 =",22+14)
print("v1 wins original order = 12 + 7 (always-first flips) =",12+7)
# regression table arithmetic
cats={'greeting':(6,6,6),'refund':(7,6,7),'technical':(7,6,7),'billing':(5,4,5),'out_of_scope':(5,4,2)}
N=30
d=sum(n/N*(a/n-b/n)*-1 for n,b,a in [(v[0],v[1],v[2]) for v in cats.values()])
print("sum n_c/N*delta_c =", sum(n/N*(a-b)/n for n,b,a in cats.values()), " prompted",sum(v[1] for v in cats.values()),"ft",sum(v[2] for v in cats.values()))
print({k:(round(b/n,3),round(a/n,3),round((a-b)/n,3)) for k,(n,b,a) in cats.items()})
print("terms:",[round(n/N*(a-b)/n,5) for n,b,a in cats.values()])
print("weighted before:",3*1+1*5,"after:",0*1+3*5)
print("jaccard 7/9 =",7/9)
# param arithmetic
emb=30522*768+512*768+2*768
layer=4*(768*768+768)+2*768+(768*3072+3072)+(3072*768+768)+2*768
base=emb+6*layer; print("distilbert encoder params",base)
heads=(768*768+768)+(768*5+5); print("w/ heads",base+heads, "claimed 66,957,317")
ad=6*2*(8*768+768*8); tr=ad+(768*768+768)+(768*5+5)
print("adapters",ad,"trainable",tr,"total",base+heads+ad,"frac",tr/(base+heads+ad))
print("ratio one proj",12288/589824)
print("full AdamW bytes @16/param GB",(base+heads)*16/1e9,"fp32 MB",(base+heads)*4/1e6)
