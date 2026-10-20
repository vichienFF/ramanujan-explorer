import sys, math, random, numpy as np
sys.path.insert(0,'.')
from ppsinger import singer_pp
from collections import Counter
for p,k in [(2,3),(5,3),(2,9),(11,3)]:
    S,m,q=singer_pp(p,k,random.Random(1000003*p**k)); r=round(q**(1/3)); n=len(S)
    rho=(r+1)*pow(r,4,m)%m
    Sset=set(int(s) for s in S); B={}
    T=0
    for a in S:
        a=int(a); blk=set()
        for b in S:
            b=int(b)
            if b==a or math.gcd((b-a)%m,m)!=1: continue
            c=(a+rho*(b-a))%m
            if c in Sset and c!=a and c!=b: blk.add(b); T+=1
        B[a]=frozenset(blk|{a})
    sizes=Counter(len(v) for v in B.values())
    blocks=set(B.values()); consistent=all(B[b]==B[a] for a in B for b in B[a])
    print(f"q={q} m prime={all(m%d for d in range(2,int(m**.5)+1))} N(rho0)={T} r(q+1)={r*(q+1)} block sizes={dict(sizes)} distinct blocks={len(blocks)} (r^2-r+1={r*r-r+1}) partition-consistent={consistent}")
