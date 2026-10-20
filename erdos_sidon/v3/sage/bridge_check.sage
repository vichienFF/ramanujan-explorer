import sys
from collections import Counter
for r in [int(a) for a in sys.argv[1:]]:
    K = GF(r**9,'w'); q=r**3; m=q*q+q+1
    tau=lambda v,k=1: v**(r**(k%9)); phi=lambda v: v**q; Tr=lambda v: v+v**q+v**(q*q)
    g=K.multiplicative_generator(); pts=[]; v=K(1)
    for i in range(m):
        if Tr(v)==0: pts.append(v)
        v*=g
    Fset=[z for z in K if z**q==z] if q<=125 else None
    res=Counter(); Azero=0
    for x in pts:
        if (x**(q-1))**q == x**(q-1): continue   # phi-fixed: excluded
        xs=[x, phi(x), phi(phi(x))]
        Xc=lambda i,j: tau(xs[i%3], j)   # tau^j(x_i)
        A=sum(xs[i]*tau(xs[(i+1)%3])/tau(xs[i]) for i in range(3))
        B=sum(xs[i]*tau(xs[(i+1)%3],8)/tau(xs[i],8) for i in range(3))
        C=sum(xs[i]*tau(xs[(i+1)%3])*tau(xs[(i+1)%3],8)/(tau(xs[i])*tau(xs[i],8)) for i in range(3))
        if A==0: Azero+=1
        # count Z in F with A Z^r + B Z + C = 0, via roots of polynomial in K[Z] restricted to F
        PR.<Z>=PolynomialRing(K); f=A*Z**r+B*Z+C
        nZ=sum(1 for rt,mult in f.roots() if rt**q==rt)
        d=x/(tau(x)*tau(x,8)); nR=sum(1 for y in pts if Tr(d*tau(y)*tau(y,8))==0)
        res[(nZ, nR-1)]+=1
    print("r=%d: (#Z-solutions, partners) -> %s ; A==0 count %d" % (r, dict(res), Azero)); sys.stdout.flush()
