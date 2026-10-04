cats=["factual","multi_hop","arithmetic","out_of_scope","adversarial","ambiguous"]; n=[10,4,4,3,3,3]
T={"baseline":[.60,0,0,1,.33,0],"v1":[.90,.5,.75,1,1,.33],"v2":[1.0,.75,.75,.33,1,.33]}
for k,v in T.items():
    c=[round(a*b) for a,b in zip(v,n)]; print(k,"correct",c,sum(c),"/",sum(n),"=",round(sum(c)/sum(n),3),"(module:", {"baseline":.37,"v1":.78,"v2":.81}[k],")")
print("cost: in",41208*2e-6,"out",4930*10e-6,"sum",41208*2e-6+4930*1e-5,"cache saving @90%",22400*2e-6*.9,"mean/task",(41208*2e-6+4930*1e-5)/27)
print("budget/day",25*0.00488,"month",25*0.00488*30, "route mix",18+6+3)
print("agent vs retrieve: ratio cost",0.018/0.002,"latency",10/2)
