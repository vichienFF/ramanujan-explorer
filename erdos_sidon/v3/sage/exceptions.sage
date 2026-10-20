import sys
from collections import Counter
for r in [int(a) for a in sys.argv[1:]]:
    K = GF(r**9, 'w'); q = r**3; m = q*q+q+1
    tau = lambda v: v**r; taui = lambda v: v**(r**8); Tr = lambda v: v + v**q + v**(q*q)
    g = K.multiplicative_generator(); pts = []; v = K(1)
    for i in range(m):
        if Tr(v) == 0: pts.append(v)
        v *= g
    U = [tau(y)*taui(y) for y in pts]
    Fq = [z for z in K if z**q == z and z != 0] if q < 200 else None
    cnt = Counter(); exc = []
    for x in pts:
        d = x/(tau(x)*taui(x))
        c = sum(1 for u in U if Tr(d*u) == 0)
        cnt[c] += 1
        if c != r+1: exc.append(x)
    # is x fixed by phi (x^q = lambda x, lambda in F^*)? i.e. x^(q-1) in F
    fixed = [ (x**(q-1))**q == x**(q-1) for x in exc ]
    allfixed = sum(1 for x in pts if (x**(q-1))**q == x**(q-1))
    print("r=%d (r mod 3=%d): dist %s | exceptional points phi-fixed: %s | total phi-fixed points in P(L): %d" % (r, r%3, dict(cnt), fixed, allfixed)); sys.stdout.flush()
