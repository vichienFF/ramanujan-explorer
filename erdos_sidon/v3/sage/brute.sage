# Independent brute force: build P(L) from an explicit F-basis (no Singer-generator enumeration)
import sys, time
from collections import Counter
for r in [int(a) for a in sys.argv[1:]]:
    t0=time.time()
    K = GF(r**9, 'w'); q = r**3
    fr = lambda v,k=1: v**(r**(k%9))
    Tr = lambda v: v + v**q + v**(q*q)
    g = K.multiplicative_generator()
    h = g**((r**9-1)//(q-1))                     # generator of F^*
    Fel = [K(0)] + [h**i for i in range(q-1)]
    # basis of L over F
    w0 = next(z for z in (K.random_element() for _ in range(100)) if Tr(z) != 0)
    proj = lambda z: z - (Tr(z)/Tr(w0))*w0
    e = proj(K.random_element())
    while e == 0: e = proj(K.random_element())
    f = proj(K.random_element())
    while f == 0 or (f/e)**q == f/e: f = proj(K.random_element())
    pts = [e + s*f for s in Fel] + [f]
    assert all(Tr(y) == 0 for y in pts) and len(pts) == q+1
    U = [fr(y)*fr(y,8) for y in pts]
    dist = Counter(); bad = []; Zmis = 0; Azero = 0
    for idx,x in enumerate(pts):
        psi = (x**q)/x
        fixed = (psi**q == psi)
        d = x/(fr(x)*fr(x,8))
        Rx = [j for j,u in enumerate(U) if Tr(d*u) == 0]
        n = len(Rx)
        assert idx in Rx                           # y = x always in R_x
        dist[(fixed, n)] += 1
        if (not fixed and n != r+1) or (fixed and n != 1): bad.append(idx)
        if not fixed:
            A = Tr(x*fr(psi)); B = Tr(x*fr(psi,8)); C = Tr(x*fr(psi)*fr(psi,8))
            if A == 0: Azero += 1
            # count Z in F with A Z^r + B Z + C = 0 (brute over F when small)
            if q <= 343:
                nZ = sum(1 for Z in Fel if A*Z**r + B*Z + C == 0)
                if nZ != n-1: Zmis += 1
    print("r=%d q=%d: {(phi-fixed, |R_x|): count} = %s | violations=%d | A==0 among non-fixed=%d | Z-count mismatches=%d | %.0fs"
          % (r, q, dict(dist), len(bad), Azero, Zmis, time.time()-t0)); sys.stdout.flush()
