# Referee 3 item 13: N3 formula (Step 4a) at prime powers incl. exceptional 49 = 7^2, 169 = 13^2 (+ 121, 125 as extra).  # LOCAL-OK: O(q^2), est. < 5 min
# N3 = sum_{c,d in F*} r(r-1)(r-2), r = #{y: c y^4 + d (1-y)^4 = 1}. Formula: q^2-7q+19+18phi(-1)+9phi(-2)+6(1+phi(-3))+b_q (b_q = alpha^n+beta^n).
# CONTROL: same code at q = 7, 13 reproduces p4_n3.py's prime values (N3 = 6, 96 from its REF table).
from sage.all import GF
from collections import Counter
def N3(q):
    F = GF(q, 'a'); sq = {x*x for x in F if x != 0}; chi = lambda v: 0 if v == 0 else (1 if v in sq else -1); tot = 0
    for c in F:
        if c == 0: continue
        cnt = Counter()
        for y in F:
            if y == 1: continue
            cnt[(1 - c*y**4) / (1-y)**4] += 1
        for d, n in cnt.items():
            if d == 0: continue
            r = n + (1 if c == 1 else 0); tot += r*(r-1)*(r-2)
        if c == 1:   # members (1,d) with no finite root still have y=1 (r=1): contribute 0
            pass
    return tot, chi
def bq(p, n):
    bp = 0 if p % 3 != 1 else next(4*x*x - 2*p for x in range(1, p) if any(x*x + 3*t*t == p for t in range(1, p)))
    e = p*p*(1 if pow(-3 % p, (p-1)//2, p) == 1 else -1); s0, s1 = 2, bp
    for _ in range(n-1): s0, s1 = s1, s1*bp - e*s0
    return s1
ctl = N3(7)[0] == 6 and N3(13)[0] == 96; print('CONTROL:', 'PASS' if ctl else 'FAIL', flush=True)
import sys
PN = [tuple(map(int, a.split("^"))) for a in sys.argv[1:]] or [(7, 2), (13, 2), (11, 2), (5, 3)]
for p, n in PN:
    q = p**n; v, chi = N3(q); F = GF(q, 'a'); f = {a: chi(F(-a)) for a in (1, 2, 3)}
    pred = q*q - 7*q + 19 + 18*f[1] + 9*f[2] + 6*(1+f[3]) + bq(p, n)
    print('q=%d N3=%d formula %d -> %s' % (q, v, pred, 'EQUAL' if v == pred else 'DIFF %d' % (v - pred)), flush=True)
