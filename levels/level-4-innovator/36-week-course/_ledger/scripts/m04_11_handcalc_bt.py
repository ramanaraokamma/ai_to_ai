import math
sig=lambda x:1/(1+math.exp(-x))
r=dict(a=2.1,b=1.4,c=-0.3,d=2.6)
print("P(a>b)",round(sig(r['a']-r['b']),4),"P(d>a)",round(sig(r['d']-r['a']),4),"P(a>c)",round(sig(r['a']-r['c']),4))
print("c>d: sigma",round(sig(r['c']-r['d']),5)," loss",round(-math.log(sig(r['c']-r['d'])),3)," a>c loss",round(-math.log(sig(r['a']-r['c'])),4))
print("gap 2.0 BT loss (vocab table says 0.127):",round(-math.log(sig(2.0)),4))
print("+100 shift:",round(sig((r['a']+100)-(r['b']+100)),4))
print("English 183 chars 36 tok -> cost $",36/1e6*2.0," Hindi 171 tok -> $",171/1e6*2.0, " x10M:",36/1e6*2*1e7,171/1e6*2*1e7)
print("SFT 0.0003% etc not computable here")
