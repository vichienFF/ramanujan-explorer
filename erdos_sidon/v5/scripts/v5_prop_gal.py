r"""Proposition 5 (Version 5 release; the v4 release had no script for it): for every UNIT l mod m,  # LOCAL-OK: seconds
C(l) = m^2 P(l) - ((q-1)m-1)^2 - (m-1)  and  P(l) = P(l^{-1}).
C(l) from Jacobi sums J[a,b] (2-D FFT of the log-pair histogram, row a = 0 removed: n1_sym.Cvals); P(l) by direct count of pairs.
CONTROL (independent theory, Theorem 3(a)): P(2) = P(-1) = (q-2)^2.  Non-units l are skipped (the proposition is for units).
Usage: python v5_prop_gal.py q1 q2 ...  (odd primes); exit 1 on any failure."""
import sys, math
from collections import Counter
from n1_sym import Cvals
from n1_char import field
bad = 0
for q in map(int, sys.argv[1:] or [5, 7, 11]):
    log = field(q); m, C = Cvals(q); one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    pts = Counter((log[sub(one, y)] % m, log[y] % m) for y in log if sub(one, y) in log)
    P = lambda l: sum(c * pts.get((l * a % m, l * b % m), 0) for (a, b), c in pts.items())
    ctl = P(2) == (q - 2) ** 2 == P(m - 1)
    units = [l for l in C if math.gcd(l, m) == 1]
    K = ((q - 1) * m - 1) ** 2 + (m - 1)
    ok = all(abs(C[l] - (m * m * P(l) - K)) < 1e-3 * m * m and P(l) == P(pow(l, -1, m)) for l in units)
    bad += not (ok and ctl)
    print('q=%d CONTROL P(2)=P(-1)=(q-2)^2: %s | Prop 5 on all %d units l: %s' % (q, 'PASS' if ctl else 'FAIL', len(units), 'MATCH' if ok else 'FAIL'))
sys.exit(1 if bad else 0)
