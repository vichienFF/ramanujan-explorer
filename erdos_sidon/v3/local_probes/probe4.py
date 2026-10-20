import sys; sys.path.insert(0,'.')
from probe3 import Nvec
import numpy as np
from sympy import n_order
for p,k in [(5,3),(2,6),(3,3),(2,3),(13,2),(2,4),(11,3)]:
    N,good,m,q=Nvec(p,k); idx=np.nonzero(good)[0]; M=N[idx]//(3*k); mu=M.mean(); z=(M-mu)/np.sqrt(mu)
    o=np.argsort(-z)[:6]; top=sorted(int(idx[j]) for j in o)
    r=round(q**(1/3))
    share=((M[o]-mu)**2-mu).sum()/len(M)/mu
    feats=[]
    for x in top:
        feats.append((x, n_order(x,m), (x*x-x+1)%m==0, [a for a in range(9) if pow(x,1,m)==pow(r,a,m) or (-x)%m==pow(r,a,m)]))
    print(f"q={q} m={m} Var/E-1={M.var()/mu-1:.4f} top6 share={share:.4f} M_top={int(M[o[0]])} mu={mu:.1f}")
    for f in feats: print("   rho",f[0],"ord",f[1],"rho^2-rho+1=0:",f[2],"pm r^a:",f[3])
