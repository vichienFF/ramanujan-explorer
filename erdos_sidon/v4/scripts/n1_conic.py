r"""AN-C9-N1 hand proof test (2026-10-29).  # LOCAL-OK: seconds
Hand proof (INFERENCE -> test): P(l) = #{(y,c,d): y in K\{0,1}, c,d in F*, c y^l + d (1-y)^l = 1}.  For l = 2 and l = -1 (= m-1, y^m in F*)
the equation is a nonzero polynomial over F_q of degree <= 2, so every root lies in F_q (F_q2 n F_q3 = F_q); for each y in F_q\{0,1}
exactly q-2 pairs (c,d) work.  => P(2) = P(-1) = (q-2)^2 = the minimum possible (only the F^2 block), for EVERY odd prime q (m prime or not).
Test: P(l) for l in 2,-1,3,-2,7,-6 vs (q-2)^2; whether (q-2)^2 is the global min of P; how many units l attain it (data-first).
Control: l = 1 must give P >> (q-2)^2."""
import sys
from n1_char import field
from collections import Counter
from math import gcd
for q in map(int, sys.argv[1:]):
    log = field(q); m = q * q + q + 1; one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    pts = Counter((log[sub(one, y)] % m, log[y] % m) for y in log if sub(one, y) in log)
    U = [l for l in range(1, m) if gcd(l, m) == 1]
    P = {l: sum(c * pts.get((l * a % m, l * b % m), 0) for (a, b), c in pts.items()) for l in U}
    base = (q - 2) ** 2; mn = min(P.values()); at = sorted(l for l in U if P[l] == mn)
    show = {s: P[s % m] for s in (1, 2, -1, 3, -2, 7, -6) if gcd(s % m, m) == 1}
    print('q=%d m=%d (q-2)^2=%d  P: %s  min P=%d attained by %d units: %s' % (q, m, base, show, mn, len(at), at[:12])); sys.stdout.flush()
