r"""Vectorised brute-force SPEC over GF(p^n) (FFA round-2 referee item: direct SPEC at q = 13^4 = 28561). Same per-class definition as  # LOCAL-OK: small q in seconds; 13^4 on Kaggle
referee4/perclass.py / p4_step5_pp.py, but the roots of each member are found with numpy (grouping y by the member they lie on).
Members: c=1: d(y) = (1 - y^4)/(1-y)^4 for y != 1, plus y = 1 on every c=1 member; c+d=0 (c != 1): c(y) = 1/(y^4 - (1-y)^4); rep: (Y^-3, (1-Y)^-3),
Y not in {0,1}, c != 1, c+d != 0, deduplicated (roots found by a vectorised evaluation per member).
CONTROL: equals p4_step5_pp.pieces (independent scalar code) at q = 7^2, 13, 11^2; and SPEC = -q+10+5f1+6f2+2f3-2chi(-7) is printed for comparison.
Usage: python p4_step5_vec.py p^n [p^n ...]
"""
import sys, time, numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
exec(open('p4_step5_pp.py', encoding='utf-8').read().split("if __name__ == '__main__':")[0])   # GF (scalar), pieces, closed, D4
def pieces_vec(F):
    q = F.q; Y = np.arange(q); W = F.W; DIG = F.DIG; p = F.p; N = q - 1; exp, log = F.exp, F.log
    add = lambda a, b: ((DIG[a] + DIG[b]) % p) @ W
    neg = lambda a: ((-DIG[a]) % p) @ W
    mul = lambda a, b: np.where((a == 0) | (b == 0), 0, exp[(log[a] + log[b]) % N])
    inv = lambda a: exp[(-log[a]) % N]
    pw = lambda a, k: np.where(a == 0, 0, exp[(k * log[a]) % N])
    one = 1; omy = add(np.ones_like(Y), neg(Y)); y4 = pw(Y, 4); o4 = pw(omy, 4)
    tval = np.zeros(q, np.int64); m1 = Y != one; tval[m1] = mul(Y[m1], inv(omy[m1]))
    out = {'c=1': 0, 'c+d=0': 0, 'rep': 0}
    def contrib(roots, X):
        r = len(roots); ts = [int(tval[y]) for y in roots if y != one]; sing = M = 0
        for a in ts:
            for b in ts:
                if a == b: continue
                if F.pw(a, 4) == F.pw(b, 4): sing += 1; continue
                M += 1 + F.chi(F.neg(D4(F, F.add(a, b), F.mul(a, b))))
        out[X] += r*(r-1)*(r-2) - sing*(r-2) - M
    # c = 1: group y != 1 by d(y); every member also has the root y = 1
    ys = Y[m1]; dval = mul(add(np.ones_like(ys), neg(y4[ys])), inv(o4[ys]))
    groups = {}
    for y, d in zip(ys.tolist(), dval.tolist()):
        if d != 0: groups.setdefault(d, []).append(y)
    for d in range(1, q):
        contrib(groups.get(d, []) + [one], 'c=1')
    # c + d = 0, c != 1: c(y) = 1/(y^4 - (1-y)^4)
    g = add(y4, neg(o4)); nz = g != 0; cval = np.zeros(q, np.int64); cval[nz] = inv(g[nz])
    groups = {}
    for y in Y[nz].tolist():
        groups.setdefault(int(cval[y]), []).append(y)
    for c, roots in groups.items():
        if c != one and len(roots) >= 2: contrib(roots, 'c+d=0')
    # repeated members
    seen = set()
    for y0 in range(q):
        if y0 in (0, one): continue
        c = F.pw(F.inv(y0), 3); d = F.pw(F.inv(int(omy[y0])), 3)
        if c == one or F.add(c, d) == 0 or (c, d) in seen: continue
        seen.add((c, d)); vals = add(mul(np.full(q, c), y4), mul(np.full(q, d), o4))
        roots = Y[vals == one].tolist()
        if len(roots) >= 2: contrib(roots, 'rep')
    return out
if __name__ == '__main__':
    ctl = all(pieces_vec(GF(p, n)) == pieces(GF(p, n)) for p, n in [(7, 2), (13, 1), (11, 2)])
    print('CONTROL (vectorised = scalar p4_step5_pp.pieces at q=49, 13, 121):', 'PASS' if ctl else 'FAIL', flush=True)
    for a in sys.argv[1:]:
        p, n = map(int, a.split('^')); F = GF(p, n); t0 = time.time(); b = pieces_vec(F); cf, tgt = closed(F)
        print('q=%d^%d=%d brute %s | SPEC %d | closed %s | target %d -> %s (%.0fs)' % (p, n, F.q, b, sum(b.values()), cf, tgt,
              'EQUAL' if b == cf and sum(b.values()) == tgt else 'DIFF', time.time() - t0), flush=True)
