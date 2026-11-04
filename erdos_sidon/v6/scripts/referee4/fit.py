import pickle
from collections import defaultdict
res=pickle.load(open('res_7_700.pkl','rb'))
def chi(a,p): a%=p; return 0 if a==0 else (1 if pow(a,(p-1)//2,p)==1 else -1)
from fractions import Fraction
for X in ('c=1','c+d=0','rep'):
    cl=defaultdict(list)
    for q,v in res.items():
        if q in (7,13): continue
        sig=tuple(chi(a,q) for a in (-1,2,-3,-7))
        cl[sig].append((q,v[X]))
    print(X)
    for sig,L in sorted(cl.items()):
        # fit A q+B through first two, test rest
        if len(L)<3: print(sig,'too few',L); continue
        (q1,v1),(q2,v2)=L[0],L[1]
        A=Fraction(v2-v1,q2-q1); B=v1-A*q1
        bad=[(q,v) for q,v in L if A*q+B!=v]
        print(sig,len(L),'A=%s B=%s'%(A,B),'BAD' if bad else 'ok',bad[:3])
