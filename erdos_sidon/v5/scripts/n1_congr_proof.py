r"""Hand proof sketch (2026-10-29) of AN-C9-N1 congruence, test here.  # LOCAL-OK: seconds
Claim: C(l) = m^2 P(l) - m Q with P(l) = #{(y,y') in (K\{0,1})^2 : L(1-y) = l L(1-y'), L(y) = l L(y')} (L = log mod m) and Q independent of l.
S3 = <y->1-y, y->1/y> acts diagonally on pairs and preserves the relation (both maps are Z-linear on (L(1-y), L(y)) since -1 in F*);
its fixed points (1/2, -1, 2, roots of y^2-y+1) all lie in F_q, where L = 0; pairs with one coordinate in F force the other into F.
=> pairs outside F^2 form free S3-orbits, pairs in F^2 always count: P(l) == (q-2)^2 (mod 6) for every l.  => C/m == const (mod 6m).
Test: P(l) mod 6 constant and equal to (q-2)^2 mod 6; C(l) - m^2 P(l) constant in l (that constant = -mQ)."""
import sys
from n1_sym import Cvals
from n1_char import field
from collections import Counter
for q in map(int, sys.argv[1:]):
    log = field(q); m, C = Cvals(q); one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    pts = Counter((log[sub(one, y)] % m, log[y] % m) for y in log if sub(one, y) in log)
    P = {l: sum(c * pts.get((l * a % m, l * b % m), 0) for (a, b), c in pts.items()) for l in C}
    res = {P[l] % 6 for l in C}; diff = {round(C[l] - m * m * P[l]) for l in C}
    print('q=%d  P mod 6 values %s  (q-2)^2 mod 6 = %d   C - m^2 P distinct values: %d %s' % (q, res, (q - 2) ** 2 % 6, len(diff), sorted(diff)[:2]))
