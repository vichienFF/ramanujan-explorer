import sympy as sp
x=sp.symbols('x')
def bad(name,P):
    bp=set(); keys=list(P)
    for k in keys:
        pk=sp.Poly(P[k],x)
        if pk.degree()>1: 
            dd=sp.discriminant(P[k],x); bp|=set(sp.factorint(abs(dd))) ; 
            print(name,k,'disc',dd, sp.factorint(abs(dd)))
    for a in range(len(keys)):
        for b in range(a+1,len(keys)):
            r=sp.resultant(P[keys[a]],P[keys[b]],x)
            if r==0: print('  common root',keys[a],keys[b]); continue
            f=sp.factorint(abs(r)); bp|=set(f)
            if any(p>13 for p in f) or 1: print('  res',keys[a],keys[b],r,list(f))
    print(name,'BAD PRIMES',sorted(bp))
cd0={'diag':3*x**2+4,'dbl':3*x**2+1,'1rho':x**2-x+2,'rhorho':x+1,'e0':x**2+1,'0':x,'p2':x-2,'m2':x+2}
bad('cd0 (sigma)',cd0)
y=x
rep={'0':y,'1':y-1,'disc0':y**2-y+1,'c1':y**2+y+1,'cd0':3*y**2-3*y+1,'sing1':2*y**2-2*y+1,'singi':y**2+1,'sing1+i':y**2-2*y+2}
bad('rep (y0)',rep)
c1={'diag':3*x**2+6*x+4,'t1=-1':2*x**2+5*x+4,'t3=-1':2*x+1,'d0':4*x**2+8*x+5,'-1':x+1,'dbl':12*x**2+24*x+13,'0':x,'-2':x+2}
bad('c1 (u)',c1)
