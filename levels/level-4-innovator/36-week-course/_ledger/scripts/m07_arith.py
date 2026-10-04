ins=[612,742,861,998,1104]; outs=[78,66,92,71,58]
d=[b-a for a,b in zip(ins,ins[1:])]; print("diffs",d,"mean",sum(d)/4,"a",ins[0]-123)
print("sum in",sum(ins),"sum out",sum(outs),"cost",sum(ins)*2e-6+sum(outs)*1e-5)
# per-turn cum spend as printed
cum=0
for i,o in zip(ins,outs): cum+=i*2e-6+o*1e-5; print(f"{cum:.6f}",end=" ")
print()
S=lambda k:489*k+123*k*(k+1)/2
for k in (5,10,30): print("k",k,"in tokens model",S(k))
print("5: 489*5+123*15=",489*5+123*15,"rel err",(4317-4290)/4317)
c=lambda k:(489*k+61.5*k*k+61.5*k)*2e-6+73*k*1e-5
for k in (5,10,30): print("cost model",k,round(c(k),4))
print("coef lin",(489+61.5)*2e-6+73e-5,"quad",61.5*2e-6)
print("crossover k =",(0.00133/0.000123))
print("$/hour at 1000 in tok/turn: n/a (no turn rate given)")
print("bytes of demo summary:",len("250 extraction calls ≈ $0.36 at $0.00144/call (source: note 14).".encode()))
print("single rag call 612 in:",612*2e-6+ 78*1e-5)
print("194/1024=",194/1024)
