exec(open('pii.py').read().split('clean, counts')[0])
exec('CASES = ['+open('pii.py').read().split('CASES = [')[1].split('caught = 0')[0])
print('--- ex2'); 
CASES += [
    ("Ask Dr. Meera Iyer about it",              "NAME",     True),
    ("Flat 3B, Green Meadows, Bengaluru 560001", "ADDRESS",  True),
    ("DOB 14/03/2011",                           "DOB",      True),
    ("my handle is @ramana_k on the club chat",  "HANDLE",   True),
]

caught=sum(bool(redact(raw)[1]) for raw,_,_ in CASES); print(f"recall = {caught}/{len(CASES)} = {caught/len(CASES):.2f}")
for raw,k,_ in CASES[-4:]: print("  ",k,bool(redact(raw)[1]))
