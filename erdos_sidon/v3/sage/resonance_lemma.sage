# Resonance Lemma check: K=GF(r^9), F=GF(r^3), L=ker Tr_{K/F}; |R_x| for all x in P(L)
import sys
from collections import Counter
for r in [int(a) for a in sys.argv[1:]]:
    K = GF(r**9, 'w'); q = r**3
    tau  = lambda v: v**r
    taui = lambda v: v**(r**8)
    Tr = lambda v: v + v**q + v**(q*q)
    # basis of L over F: pick e,f in ker Tr linearly independent over F
    g = K.multiplicative_generator(); m = q*q+q+1
    pts = []
    h = g**((r**9-1)//m)  # not needed; enumerate P(L) via g^i, i<m
    v = K(1)
    for i in range(m):
        if Tr(v) == 0: pts.append(v)
        v *= g
    assert len(pts) == q+1
    cnt = Counter()
    for x in pts:
        d = x/(tau(x)*taui(x))
        c = sum(1 for y in pts if Tr(d*tau(y)*taui(y)) == 0)
        cnt[c] += 1
    print("r=%d q=%d: |R_x| distribution %s" % (r, q, dict(cnt))); sys.stdout.flush()
