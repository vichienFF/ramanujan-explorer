r"""Step 5 at PRIME POWERS (public evidence for the FFA draft, repro referee item 2): brute-force per-class SPEC over GF(p^n) vs the explicit  # LOCAL-OK: minutes
closed forms of p4_step5_c1/cd0/rep (Lemmas c1, cd0, repc) and vs the target -q + 10 + 5chi(-1) + 6chi(-2) + 2chi(-3) - 2chi(-7).
Field: GF(p^n) by log/antilog tables from a primitive polynomial (sympy galoistools); elements are base-p integers (digit k = coefficient of x^k).
Per-class definition (same as referee4/perclass.py): for each member, r(r-1)(r-2) - sing*(r-2) - sum over non-singular ordered pairs of (1+chi(-D4(t1+t2,t1 t2))),
classes c=1 (all d), c+d=0 (c != 1), rep (members (Y^-3,(1-Y)^-3), Y not in {0,1}, excluding c=1 and c+d=0, deduplicated).
CONTROL: at prime q the GF code reproduces referee4/perclass.pieces(q) (independent mod-p implementation) for q = 11, 13, 17, 19.
Usage: python p4_step5_pp.py p^n [p^n ...]   (writes nothing; prints one line per q)
"""
import sys, numpy as np, sympy as sp
from sympy.polys.galoistools import gf_irreducible_p, gf_pow_mod
from sympy.polys.domains import ZZ
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
class GF:
    def __init__(s, p, n):
        s.p, s.n, s.q = p, n, p**n; q = s.q; N = q - 1
        if n == 1:
            g = next(g for g in range(2, p) if all(pow(g, N//r, p) != 1 for r in sp.factorint(N)))
            exp = [pow(g, i, p) for i in range(N)]
        else:
            fac = list(sp.factorint(N))
            for tt in range(p**n):
                c = [(tt // p**i) % p for i in range(n)]; P = [1] + c[::-1]
                if c[0] and gf_irreducible_p(P, p, ZZ) and all(gf_pow_mod([1, 0], N//r, P, p, ZZ) != [1] for r in fac): break
            exp = []; v = [1] + [0]*(n-1)
            for i in range(N):
                exp.append(sum(dd * p**k for k, dd in enumerate(v))); top = v[-1]; v = [0] + v[:-1]; v = [(v[k] - top*c[k]) % p for k in range(n)]
        s.exp = np.array(exp, np.int64); s.log = np.full(q, -1, np.int64); s.log[s.exp] = np.arange(N)
        W = p ** np.arange(n); s.DIG = (np.arange(q)[:, None] // W) % p; s.W = W
    def add(s, a, b): return int(((s.DIG[a] + s.DIG[b]) % s.p) @ s.W)
    def neg(s, a): return int(((-s.DIG[a]) % s.p) @ s.W)
    def sub(s, a, b): return s.add(a, s.neg(b))
    def mul(s, a, b): return 0 if a == 0 or b == 0 else int(s.exp[(s.log[a] + s.log[b]) % (s.q-1)])
    def inv(s, a): return int(s.exp[(-s.log[a]) % (s.q-1)])
    def pw(s, a, k): return 0 if a == 0 else int(s.exp[(k * s.log[a]) % (s.q-1)])
    def I(s, k):                                  # integer k in the prime field
        k %= s.p; return int(k)                  # digit-0 encoding
    def chi(s, a): return 0 if a == 0 else (1 if s.log[a] % 2 == 0 else -1)
def ev(F, coeffs, x):                             # polynomial with integer coefficients (low -> high) at field element x
    r = 0
    for c in reversed(coeffs): r = F.add(F.mul(r, x), F.I(c))
    return r
def D4(F, u, v):
    terms = [(7, 4, 0), (12, 3, 1), (12, 3, 0), (12, 2, 2), (-4, 2, 1), (12, 2, 0), (-16, 0, 3), (32, 0, 2), (-16, 0, 1)]
    r = 0
    for c, i, j in terms: r = F.add(r, F.mul(F.I(c), F.mul(F.pw(u, i) if i else 1, F.pw(v, j) if j else 1)))
    return r
def pieces(F):
    q = F.q; one = 1; out = {'c=1': 0, 'c+d=0': 0, 'rep': 0}
    Y = list(range(q)); y4 = [F.pw(y, 4) for y in Y]; omy = [F.sub(one, y) for y in Y]; omy4 = [F.pw(t, 4) for t in omy]
    tval = {y: F.mul(y, F.inv(omy[y])) for y in Y if y != one}
    def contrib(c, d, X):
        roots = [y for y in Y if F.sub(F.add(F.mul(c, y4[y]), F.mul(d, omy4[y])), one) == 0]
        r = len(roots); ts = [tval[y] for y in roots if y != one]; sing = M = 0
        for a in ts:
            for b in ts:
                if a == b: continue
                if F.pw(a, 4) == F.pw(b, 4): sing += 1; continue
                M += 1 + F.chi(F.neg(D4(F, F.add(a, b), F.mul(a, b))))
        out[X] += r*(r-1)*(r-2) - sing*(r-2) - M
    for d in range(1, q): contrib(one, d, 'c=1')
    for c in range(1, q):
        if c == one: continue
        contrib(c, F.neg(c), 'c+d=0')
    seen = set()
    for y0 in range(q):
        if y0 in (0, one): continue
        c = F.pw(F.inv(y0), 3); d = F.pw(F.inv(omy[y0]), 3)
        if c == one or F.add(c, d) == 0 or (c, d) in seen: continue
        seen.add((c, d)); contrib(c, d, 'rep')
    return out
def Z(F, coeffs): return {x for x in range(F.q) if ev(F, coeffs, x) == 0}
def closed(F):
    q, chi, I = F.q, F.chi, F.I
    f1, f2, f3, f7 = chi(I(-1)), chi(I(-2)), chi(I(-3)), chi(I(-7))
    w1 = lambda u: 1 + chi(F.neg(ev(F, [4, 6, 3], u)))
    ZE = Z(F, [1, 1]) | Z(F, [5, 8, 4]) | Z(F, [4, 5, 2]) | Z(F, [4, 6, 3]); ZI = Z(F, [13, 24, 12]) | Z(F, [1, 2])
    c1 = 2*(q - f3) - 2*sum(w1(u) for u in ZE) - sum(w1(u) for u in ZI - ZE - {0, I(-2)})
    w2 = lambda s: 1 + chi(F.neg(ev(F, [4, 0, 3], s)))
    ZE2 = Z(F, [0, 1]) | Z(F, [1, 0, 1]) | Z(F, [1, 1]) | Z(F, [2, -1, 1]) | Z(F, [4, 0, 3]); ZI2 = Z(F, [1, 0, 3]); PM = {I(2), I(-2)}
    cd0 = -(q - f3) + sum(w2(s) for s in ZE2) + sum(w2(s) for s in PM - ZE2) - sum(w2(s) for s in ZI2 - ZE2 - PM)
    w3 = lambda y: 1 + chi(F.mul(I(-2), ev(F, [1, -1, 1], y)))
    X0 = {0, 1} | Z(F, [1, 1, 1]) | Z(F, [1, -3, 3]) | Z(F, [1, -1, 1]); Zs = Z(F, [1, -2, 2]) | Z(F, [1, 0, 1]) | Z(F, [2, -2, 1])
    rep = -2*(q - f2) + 2*sum(w3(y) for y in X0) + 2*len(Zs - X0) - 2*len(Z(F, [1, -1, 1]))
    return {'c=1': c1, 'c+d=0': cd0, 'rep': rep}, -q + 10 + 5*f1 + 6*f2 + 2*f3 - 2*f7
if __name__ == '__main__':
    exec(open('referee4/perclass.py', encoding='utf-8').read().split("if __name__=='__main__':")[0], g := {})
    ctl = all(pieces(GF(qq, 1)) == g['pieces'](qq) for qq in (11, 13, 17, 19))
    print('CONTROL (GF code = referee4/perclass.pieces at q=11,13,17,19):', 'PASS' if ctl else 'FAIL', flush=True)
    for a in sys.argv[1:]:
        p, n = map(int, a.split('^')); F = GF(p, n); b = pieces(F); cf, tgt = closed(F)
        print('q=%d^%d=%d brute %s closed %s | SPEC %d target %d -> %s' % (p, n, F.q, b, cf, sum(b.values()), tgt,
              'EQUAL' if b == cf and sum(b.values()) == tgt else 'DIFF'), flush=True)
