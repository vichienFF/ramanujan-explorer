"""Sage-free Singer set for q = 3^n via a GF(3) bit-plane LFSR (enables q = 243 locally / on Kaggle).  # LOCAL-OK: q=243 est. < 25 min (benchmark at q=27, 81 printed)
S = {i mod m : x^i in F_q*1 + F_q*x}, m = q^2+q+1, field F_{3^{3n}} = F_3[x]/(P), P primitive (sympy galoistools), so x generates F*.
Usage: python singer3.py n [n ...]   -> prints F3(4) = sum (I-0)(I-1)(I-2) for the I_4 multiset.
CONTROL: F3(4) must equal the Sage values 72 (q=9), 648 (q=27), 6480 (q=81) (p4_scope / H-CH3 outputs); |S| = q+1 and distinct differences at q=9.
H-CH3B (registered): q=243 -> predicted 58320.
"""
import sys, time, numpy as np
from sympy.polys.galoistools import gf_irreducible_p, gf_pow_mod
from sympy.polys.domains import ZZ
from sympy import factorint
def add(a, b):   # GF(3)^k vectors as bit-planes (ones, twos)
    x1, x2 = a; y1, y2 = b; n1 = ~(y1 | y2); n0 = ~(x1 | x2)
    return ((x1 & n1) | (n0 & y1) | (x2 & y2), (x2 & n1) | (n0 & y2) | (x1 & y1))
def neg(a): return (a[1], a[0])
def primitive_poly(k):
    N = 3**k - 1; fac = list(factorint(N))
    for t in range(3**k):
        c = [(t // 3**i) % 3 for i in range(k)]; P = [1] + c[::-1]          # monic, coefficients high -> low
        if c[0] == 0 or not gf_irreducible_p(P, 3, ZZ): continue
        if all(gf_pow_mod([1, 0], N // r, P, 3, ZZ) != [1] for r in fac): return c   # c[i] = coeff of x^i
def field(k):
    c = primitive_poly(k); top = 1 << (k - 1); mask = (1 << k) - 1
    red = (sum(1 << i for i in range(k) if (-c[i]) % 3 == 1), sum(1 << i for i in range(k) if (-c[i]) % 3 == 2))  # x^k = -sum c_i x^i
    def xmul(a):
        x1, x2 = a; d = 1 if x1 & top else (2 if x2 & top else 0); a = ((x1 << 1) & mask, (x2 << 1) & mask)
        return a if d == 0 else add(a, red if d == 1 else neg(red))
    def mul(a, b):
        acc = (0, 0); cur = b
        for i in range(k):
            if (a[0] >> i) & 1: acc = add(acc, cur)
            elif (a[1] >> i) & 1: acc = add(acc, neg(cur))
            cur = xmul(cur)
        return acc
    return xmul, mul
def F3_4(n):
    q = 3**n; k = 3*n; m = q*q + q + 1; xmul, mul = field(k); one = (1, 0); X = (2, 0)
    w = one
    for _ in range(m): w = xmul(w)                                   # w = x^m generates F_q*
    sub = [(0, 0)]; e = one
    for _ in range(q - 1): sub.append(e); e = mul(e, w)
    V = {a[0] | (a[1] << k) for a in (add(c0, mul(c1, X)) for c0 in sub for c1 in sub)}
    S = set(); e = one
    for i in range(3**k - 1):
        if (e[0] | (e[1] << k)) in V: S.add(i % m)
        e = xmul(e)
    S = np.array(sorted(S)); ind = np.zeros(m, np.int64); ind[S] = 1; lS = (4 * S) % m
    I = np.array([ind[(lS + mu) % m].sum() for mu in range(m)])
    return int((I * (I-1) * (I-2)).sum()), len(S), S, m
if __name__ == '__main__':
    t0 = time.time(); v, sz, S, m = F3_4(2)
    diffs = {(a - b) % m for a in S for b in S if a != b}
    ctl = v == 72 and sz == 10 and len(diffs) == sz * (sz - 1)
    for n, ref in ((3, 648), (4, 6480)):
        t1 = time.time(); ctl &= F3_4(n)[0] == ref; print('q=%d control done in %.0fs' % (3**n, time.time() - t1), flush=True)
    print('CONTROL (Sage values q=9,27,81; Singer property q=9):', 'PASS' if ctl else 'FAIL', flush=True)
    for n in [int(a) for a in sys.argv[1:]]:
        t1 = time.time(); v = F3_4(n)[0]; q = 3**n; pred = q * (q - 2 + (-1)**n)
        print('q=%d F3(4)=%d predicted %d -> %s (%.0fs)' % (q, v, pred, 'EQUAL' if v == pred else 'DIFF', time.time() - t1), flush=True)
