import sys, pickle
from collections import defaultdict
def isp(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
def pieces(q):
    chi=[0]*q
    for a in range(1,q): chi[a*a%q]=1
    for a in range(1,q):
        if chi[a]==0: chi[a]=-1
    Y=range(q); inv=lambda a: pow(a%q,q-2,q)
    out={'c=1':0,'c+d=0':0,'rep':0}
    p4=[pow(a,4,q) for a in range(q)]
    def member(c,d):
        roots=[y for y in Y if (c*p4[y]+d*p4[(1-y)%q]-1)%q==0]
        return roots
    def contrib(c,d,roots,X):
        r=len(roots)
        ts=[y*inv(1-y)%q for y in roots if y!=1]
        sing=0; M=0
        for a in ts:
            for b in ts:
                if a==b: continue
                if p4[a]==p4[b]: sing+=1; continue
                M+=1+chi[(-D4((a+b)%q,a*b%q))%q]
        out[X]+= r*(r-1)*(r-2)-sing*(r-2)-M
    for d in range(1,q):
        roots=member(1,d); contrib(1,d,roots,'c=1')
    for c in range(2,q):
        d=(-c)%q; roots=member(c,d); contrib(c,d,roots,'c+d=0')
    seen=set()
    for y0 in range(2,q):
        c=pow(y0,-3,q); d=pow(1-y0,-3,q)
        if c==1 or (c+d)%q==0 or (c,d) in seen: continue
        seen.add((c,d)); roots=member(c,d); contrib(c,d,roots,'rep')
    return out
if __name__=='__main__':
    lo,hi=int(sys.argv[1]),int(sys.argv[2]); res={}
    for q in range(lo,hi):
        if isp(q) and q>=7:
            res[q]=pieces(q); print(q,res[q],flush=True)
    pickle.dump(res,open('res_%d_%d.pkl'%(lo,hi),'wb'))
