import sys, random, math, itertools
import numpy as np
sys.path.insert(0,'.')
from ppsinger import primitive_poly, polymulmod, polypow, singer_pp
def run(p,k):
    n=3*k; q=p**k; m=q*q+q+1; r=round(q**(1/3))
    rng=random.Random(1000003*q)
    S,mm,_=singer_pp(p,k,random.Random(1000003*q))   # same rng seed path as kernels
    # rebuild f exactly as singer_pp does
    f=primitive_poly(p,n,random.Random(1000003*q))
    mul=lambda a,b: polymulmod(a,b,f,p)
    def pw(a,e): return polypow(a,e,f,p)
    X=[0,1]+[0]*(n-2); one=[1]+[0]*(n-1)
    def gpow(i): return pw(X,i)
    add=lambda a,b:[(x+y)%p for x,y in zip(a,b)]; sub=lambda a,b:[(x-y)%p for x,y in zip(a,b)]
    def inv(a): return pw(a,p**n-2)
    def isF_r(c): return pw(c,r)==c
    Sl=[int(s) for s in S]; Sset=set(Sl)
    # basis of F=F_q inside K: powers of h = g^((p^n-1)/(q-1))
    h=pw(X,(p**n-1)//(q-1)); Fb=[one]; 
    for _ in range(k-1): Fb.append(mul(Fb[-1],h))
    e=gpow(Sl[0]); fv=gpow(Sl[1])
    cols=[mul(u,e) for u in Fb]+[mul(u,fv) for u in Fb]
    A=np.array(cols).T % p   # n x 2k
    def solve(y):
        # solve A z = y over F_p (Gaussian elimination)
        Mx=np.concatenate([A,np.array(y)[:,None]],1)%p; rows,cols_=Mx.shape; piv=[]; rI=0
        for c in range(2*k):
            pr=next((i for i in range(rI,rows) if Mx[i,c]%p),None)
            if pr is None: continue
            Mx[[rI,pr]]=Mx[[pr,rI]]; Mx[rI]=Mx[rI]*pow(int(Mx[rI,c]),-1,p)%p
            for i in range(rows):
                if i!=rI and Mx[i,c]: Mx[i]=(Mx[i]-Mx[i,c]*Mx[rI])%p
            piv.append(c); rI+=1
        z=[0]*(2*k)
        for i,c in enumerate(piv): z[c]=int(Mx[i,-1])
        a=[0]*n; b=[0]*n
        for j in range(k):
            a=add(a,[(z[j]*t)%p for t in Fb[j]]); b=add(b,[(z[k+j]*t)%p for t in Fb[j]])
        return a,b
    def coord(i):
        a,b=solve(gpow(i))
        if not any(a): return None   # infinity
        return mul(b,inv(a))
    rho=(r+1)*pow(r,4,m)%m
    bad=0; tested=0
    for a_ in Sl[:12]:
        parts=[b for b in Sl if b!=a_ and math.gcd((b-a_)%m,m)==1 and (a_+rho*(b-a_))%m in Sset and (a_+rho*(b-a_))%m not in (a_,b)]
        pts=[coord(a_)]+[coord(b) for b in parts]
        if any(t is None for t in pts): continue
        s1,s2,s3=pts[0],pts[1],pts[2]
        for s4 in pts[3:]:
            cr=mul(mul(sub(s1,s3),sub(s2,s4)),inv(mul(sub(s1,s4),sub(s2,s3))))
            tested+=1; bad+= (not isF_r(cr))
    print(f"q={q} r={r}: cross-ratio tests {tested}, NOT in F_r: {bad}")
for p,k in [(7,3)]: run(p,k)
