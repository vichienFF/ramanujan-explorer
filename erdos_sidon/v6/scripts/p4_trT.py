# H-TR (registered P4_PROOF Step 4j): trT(p) = -sum_{v in P1(F_p)} a_v - p(1+(-1/p)) vs b_p (12.3.c.a) and vs B(p)=sum chi(s m H(s,m)).
# CONTROLS: smooth-fibre #E_k = 0 mod 4 (full rational 2-torsion); vectorised a_v equals a scalar loop at p=13.
import sys, numpy as np
def chi_tab(p):
    t = np.zeros(p, np.int64); t[(np.arange(1, p) ** 2) % p] = 1; t[t == 0] = -1; t[0] = 0; return t
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
def run(p):
    c = chi_tab(p); X = np.arange(p); ctl = True; S = 0
    for k in range(p):
        e1 = (k-1)**2*(k+2)*(k+4) % p; e2 = k*(k-2)*(k+3)**2 % p
        sv = int(c[(X * (X - e1) * (X - e2)) % p].sum()); S += sv          # sv = -a_k
        disc = (e1 * e2 * (e1 - e2)) % p
        if disc: ctl &= (p + 1 + sv) % 4 == 0
    S += -1                                                                 # a_inf = 1 (split I6, node at x=1)
    s = X[:, None]; m = X[None, :]
    H = (m**3 + 8*m*m - 3*m*s*s + 6*m*s + 13*m + 2*s**3 + 2*s*s - 10*s + 6) % p
    B = int(c[(s * m % p) * H % p].sum())
    return S - p * (1 + c[p - 1]), B, ctl, c
def scalar_check(p):
    c = chi_tab(p); tot = 0
    for k in range(p):
        e1 = (k-1)**2*(k+2)*(k+4); e2 = k*(k-2)*(k+3)**2
        for x in range(p): tot += c[(x*(x-e1)*(x-e2)) % p]
    return tot - 1
ctl = scalar_check(13) - 13 * (1 + chi_tab(13)[12]) == run(13)[0]
LO, HI = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (7, 200)   # repro referee 11-03: 200..420 run now reproducible
P = [p for p in range(LO, HI) if all(p % d for d in range(2, int(p**.5) + 1))]; rows = []
for p in P:
    tr, B, c2, c = run(p); ctl &= c2; L = {a: int(c[a % p]) for a in (-1, 2, 3, 5)}; rows.append((p, tr, B, bq(p), L))
print('CONTROLS:', 'PASS' if ctl else 'FAIL')
import itertools
best = None
for sub in itertools.product((0, 1), repeat=4):
    for sg in (1, -1):
        eps = lambda L: sg * np.prod([L[a] for a, u in zip((-1, 2, 3, 5), sub) if u])
        bad = [r[0] for r in rows if r[1] != eps(r[4]) * r[3]]
        if best is None or len(bad) < len(best[2]): best = (sub, sg, bad)
print('best eps: sign %d * chars %s ; primes failing trT = eps*b_p: %s (of %d)' % (best[1], [a for a, u in zip((-1, 2, 3, 5), best[0]) if u], best[2], len(rows)))
for r in rows[:8]: print('p=%d trT=%d b_p=%d B=%d B-2p=%d' % (r[0], r[1], r[3], r[2], r[2] - 2 * r[0]))
bad2 = [r[0] for r in rows if r[2] != 2 * r[0] + r[4][-1] * r[0] + r[1]]
print('B(p) = 2p + (-1/p)p + trT(p): failures %s (of %d)' % (bad2, len(rows)))
