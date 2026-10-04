from compare import compare
mk=lambda name,d:{"name":name,"n":30,"overall":sum(c for c,_ in d.values())/30,"per_category":{k:(c,t,c/t) for k,(c,t) in d.items()}}
b=mk("prompted",{"greeting":(6,6),"refund":(6,7),"technical":(6,7),"billing":(4,5),"out_of_scope":(4,5)})
a=mk("ft",{"greeting":(6,6),"refund":(7,7),"technical":(7,7),"billing":(5,5),"out_of_scope":(2,5)})
compare(b,a)
print("\nLoRA rank table arithmetic (base 66,957,317; head 594,437)")
head=768*768+768+768*5+5
for r in (1,2,4,8,16,32):
    ad=6*2*(r*768*2); tr=ad+head; tot=66957317+ad
    print(f"r={r:2d} adapter {ad:,} trainable {tr:,} % {tr/tot*100:.2f}")
