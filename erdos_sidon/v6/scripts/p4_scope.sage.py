# H-P4-SCOPE (registered PLAN_UNIFORM_A 2026-11-03): F3(4) = (q-2)(q+1) + b_q at q = 25,49,121,125; char 3 exploratory.  # LOCAL-OK: estimate from q=101 Singer 26 s (m10_sqrt.sage) -> q=125 ~1 min
# CONTROLS: proved value at q=7,13; I_4 multiset at q=11 = {0:40,1:54,2:30,3:6,4:3}.
import sys, time, numpy as np
from collections import Counter
from sage.all import GF
def singer(q):
    K = GF(q**3, 'a'); a = K.gen(); g = K.multiplicative_generator(); n = q**3 - 1; m = q*q + q + 1
    sub = [x for x in K if x**q == x]; log = {}; x = K(1)
    for i in range(n): log[x] = i; x *= g
    return np.array(sorted({log[c0 + c1 * a] % m for c0 in sub for c1 in sub if c0 != 0 or c1 != 0})), m
def ms(S, m, l):
    ind = np.zeros(m, np.int64); ind[S] = 1; lS = (l * S) % m
    return np.array([ind[(lS + mu) % m].sum() for mu in range(m)])
def F3(I): return int((I * (I - 1) * (I - 2)).sum())
def bp(p):
    if p % 3 != 1: return 0
    x = next(x for x in range(1, p) if any(x*x + 3*t*t == p for t in range(1, p))); return 4*x*x - 2*p
def bq(p, n):
    s0, s1 = 2, bp(p); e = p*p*(1 if pow(-3 % p, (p-1)//2, p) == 1 else -1)
    for _ in range(n - 1): s0, s1 = s1, s1 * bp(p) - e * s0
    return s1
S, m = singer(11); ctl = dict(Counter(ms(S, m, 4).tolist())) == {0: 40, 1: 54, 2: 30, 3: 6, 4: 3}
for q in (7, 13):
    S, m = singer(q); ctl &= F3(ms(S, m, 4)) == (q-2)*(q+1) + bp(q)
print('CONTROLS:', 'PASS' if ctl else 'FAIL', flush=True); ok = True
for p, n in ((5, 2), (7, 2), (11, 2), (5, 3), (3, 2), (3, 3), (3, 4)):
    q = p**n; t0 = time.time(); S, m = singer(q); v = F3(ms(S, m, 4))
    if p == 3: print('q=%d EXPLORATORY F3(4)-(q-2)(q+1) = %d (%.0fs)' % (q, v - (q-2)*(q+1), time.time()-t0), flush=True); continue
    pred = (q-2)*(q+1) + bq(p, n); ok &= v == pred
    print('q=%d F3(4)=%d predicted %d -> %s (%.0fs)' % (q, v, pred, 'EQUAL' if v == pred else 'DIFF %d' % (v - pred), time.time()-t0), flush=True)
print('H-P4-SCOPE:', ('PASS' if ok else 'FAIL') if ctl else 'VOID')
