# Boundary-rest reorganisation: rest = sum over special member classes X of (N3[X] - M[X]) - T_{-1}, where M[X] = sum of main terms over
# ordered pairs of distinct finite roots of members in X, T_{-1} = main terms of pairs containing t=-1. Prints each piece to fit/prove.  # LOCAL-OK: seconds
# CONTROL: the pieces add up to the boundary rest of p4_n3_assembly (= -3q+12+5f1+6f2+4f3, H-N3CAT PASS) at every q.
import numpy as np
def chi(a, q): a %= q; return 0 if a == 0 else (1 if pow(a, (q-1)//2, q) == 1 else -1)
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
def pieces(q):
    Y = np.arange(q); inv = lambda a: pow(a % q, q-2, q)
    out = {'c=1': [0, 0], 'c+d=0': [0, 0], 'rep': [0, 0]}
    for c in range(1, q):
        for d in range(1, q):
            vals = (c*Y**4 + d*(1-Y)**4 - 1) % q; roots = [int(y) for y in Y[vals == 0]]; r = len(roots)
            if r < 2 and c != 1 and (c+d) % q: continue
            # repeated root? derivative test in y: f'(y) = 4c y^3 - 4d (1-y)^3
            rep = any((4*c*y**3 - 4*d*(1-y)**3) % q == 0 for y in roots)
            X = 'c=1' if c == 1 else ('c+d=0' if (c+d) % q == 0 else ('rep' if rep else None))
            if X is None: continue
            ts = [y * inv(1-y) % q for y in roots if y != 1]
            sing = [(a, b) for a in ts for b in ts if a != b and pow(a, 4, q) == pow(b, 4, q)]   # already in the singular category
            M = sum(1 + chi(-D4((a+b) % q, a*b % q), q) for a in ts for b in ts if a != b and pow(a, 4, q) != pow(b, 4, q))
            out[X][0] += r*(r-1)*(r-2) - len(sing)*(r-2); out[X][1] += M
    Tm1 = 2 * sum(1 + chi(-D4((t-1) % q, -t % q), q) for t in range(q) if t != q-1)
    return out, Tm1
for q in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
    out, Tm1 = pieces(q); f1, f2, f3, f7 = chi(-1, q), chi(-2, q), chi(-3, q), chi(-7, q)
    rest = sum(a - b for a, b in out.values()) - Tm1; pred = -3*q + 12 + 5*f1 + 6*f2 + 4*f3
    print('q=%d CONTROL rest==pred %s | f1 f2 f3 f7 = %d %d %d %d | N3,M per class %s | T-1 %d' % (q, rest == pred, f1, f2, f3, f7, out, Tm1))
