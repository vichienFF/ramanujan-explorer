import sys
from collections import defaultdict
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
def run(p):
    chi=[0]*p
    for a in range(1,p): chi[a*a%p]=1
    for a in range(1,p):
        if chi[a]==0: chi[a]=-1
    inv=lambda a: pow(a%p,p-2,p); i2=inv(2)
    sq={}
    for a in range(p): sq.setdefault(a*a%p,[]).append(a)
    p4=[pow(a,4,p) for a in range(p)]
    def wpair(a,b,r):   # finite pair weight
        if p4[a]==p4[b]: return 0
        return (r-2)-(1+chi[(-D4((a+b)%p,a*b%p))%p])
    # ---- c=1: u param
    dev1=set()
    gval=defaultdict(list)
    for t in range(p):
        if (t+1)%p: gval[((1+t)**4-t**4)%p].append(t)
    for u in range(p):
        for w in sq.get((-3*(u+1)**2-1)%p,[]):
            t1=(u+w)*i2%p; t2=(u-w)*i2%p
            if w==0: W=0
            else:
                d=((1+t1)**4-t1**4)%p
                if t1==p-1 or t2==p-1 or d==0: W=0
                else:
                    n=len(gval[d]); r=n+1
                    W=wpair(t1,t2,r)+2
            if W!=2: dev1.add(u)
    # ---- cd0: sigma param
    dev2=set()
    gv=defaultdict(list)
    for s in range(p): gv[s*(s*s+1)%p*i2%p].append(s)
    for sg in range(p):
        for w in sq.get((-3*sg*sg-4)%p,[]):
            s1=(sg+w)*i2%p; s2=(sg-w)*i2%p
            if w==0: W=0
            else:
                e=s1*(s1*s1+1)%p*i2%p
                if e in (0,1): W=0
                else:
                    r=len(gv[e]); t1=(1+s1)*inv(1-s1)%p; t2=(1+s2)*inv(1-s2)%p
                    W=wpair(t1,t2,r)
            if W!=-1: dev2.add(sg)
    # ---- rep: y0 param (member weight, summed over all pairs of the member)
    dev3=set(); seen={}
    def roots(c,d): return [y for y in range(p) if (c*p4[y]+d*p4[(1-y)%p]-1)%p==0]
    for y0 in range(p):
        gen=-2*(1+chi[(-2*(y0*y0-y0+1))%p])
        if y0 in (0,1): W=0
        else:
            c=pow(y0,-3,p); d=pow(1-y0,-3,p)
            if c==1 or (c+d)%p==0: W=0
            elif (c,d) in seen: W=0
            else:
                seen[(c,d)]=y0; R=roots(c,d); r=len(R)
                ts=[y*inv(1-y)%p for y in R if y!=1]
                W=sum(wpair(a,b,r) for a in ts for b in ts if a!=b)
        if W!=gen: dev3.add(y0)
    return dev1,dev2,dev3
def rootsmod(poly,p): return {x for x in range(p) if poly(x)%p==0}
for p in [int(a) for a in sys.argv[1:]]:
    d1,d2,d3=run(p)
    i2=pow(2,p-2,p)
    E1=set()
    for f in (lambda u:3*u*u+6*u+4,lambda u:2*u*u+5*u+4,lambda u:2*u+1,lambda u:4*u*u+8*u+5,lambda u:u+1,lambda u:12*u*u+24*u+13,lambda u:u,lambda u:u+2): E1|=rootsmod(f,p)
    E2=set()
    for f in (lambda x:3*x*x+4,lambda x:3*x*x+1,lambda x:x*x-x+2,lambda x:x+1,lambda x:x*x+1,lambda x:x,lambda x:x-2,lambda x:x+2): E2|=rootsmod(f,p)
    E3=set()
    for f in (lambda y:y,lambda y:y-1,lambda y:y*y-y+1,lambda y:y*y+y+1,lambda y:3*y*y-3*y+1,lambda y:2*y*y-2*y+1,lambda y:y*y+1,lambda y:y*y-2*y+2): E3|=rootsmod(f,p)
    print('p=%d c1 dev %s subset-of-E %s (|E|=%d) | cd0 dev %s subset %s | rep dev %s subset %s'%(p,sorted(d1),d1<=E1,len(E1),sorted(d2),d2<=E2,sorted(d3),d3<=E3))
    print('   missing-from-dev: c1',sorted(E1-d1),'cd0',sorted(E2-d2),'rep',sorted(E3-d3))
