"""Arithmetic claims in module 05, recomputed (no model involved)."""
pi,po=2.00,10.00
c=lambda i,o:i/1e6*pi+o/1e6*po
print("one call 420/60:",c(420,60), "input",420/1e6*pi,"output",60/1e6*po)
print("60 calls:",60*c(420,60),"15 runs:",15*60*c(420,60))
print("probe 78/33:",f"{c(78,33):.6f}","78/20:",f"{c(78,20):.6f}")
print("541-token worst case x32:",32*c(541,60))
print("budget: 400/60 per call",c(400,60),"8 calls",8*c(400,60))
for n,i,o in [("v0",720,240),("v1chat",1120,560),("v2broken",720,160),("v1zs",480,640),("v2",2180,280),("v3",4320,280),("v4",4360,240),("v5",5120,240)]:
    print(n,f"${c(i,o):.4f}")
print("sum v1..v4 claimed:",round(c(480,640)+c(2180,280)+c(4320,280)+c(4360,240),4))
# frontier table: cost per 1000 calls -> monthly
for n,k in [("a",1.38),("b",1.39),("c",2.11),("d",9.40)]:
    print(n,"per1000 $",k,"monthly@1k/day",round(k*1*30,2),"monthly@1M/day",round(k*1000*30,0))
print("v3 cost/1000 calls from $0.0114/8 cases:",0.0114/8*1000)
print("field counts: const baseline 4+5+2+3 =",4+5+2+3,"of 32 =",14/32)
print("dumb stub 1+2+4+5 =",1+2+4+5,"/32 =",12/32)
print("v3 per-field 8+6+8+7=",8+6+8+7,"/32=",29/32, " v5 8+7+8+7=",30/32)
print("v2 8+5+6+6=",25/32, " v1 5+4+5+5=",19/32)
