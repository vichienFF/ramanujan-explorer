r"""Uniform-step KILL-TEST (2026-10-30, registered before running, STEPB_PROOF 'refined plan after E61').  # LOCAL-OK: minutes
Hand: P(l) = (q-2)^2 [F-block] + #{y in K\F : 1, y^l, (1-y)^l F-dependent with nonzero coefficients} = q^2 + O(q) generically, and the y-set is
a surface of degree ~2l in A^3, so its H^2 transcendental part should GROW with the height of l (barrier) unless averaging kills it.
Statistic: r(l,q) = (P(l) - (q-2)^2 - q^2)/q over primes q; report mean and sd over q for each l.
PREDICTION: l in {3,-2} (CM K3): sd ~ 1; sd increases with height (4,-3,5,-4,3/2,...). 'Flat sd' would be the new phenomenon.
CONTROL: P(2) = P(-1) = (q-2)^2 exactly; P(-2) = (q-2)^2 + q^2 - q - 2 + b_q exactly (theorem N2_PROOF)."""
import sys, statistics
from math import gcd
from collections import Counter
from n1_char import field
from n2_eta import b
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LS = [('2', 2, 1), ('-1', -1, 1), ('3', 3, 1), ('-2', -2, 1), ('4', 4, 1), ('-3', -3, 1), ('3/2', 3, 2), ('5', 5, 1), ('-4', -4, 1), ('5/2', 5, 2), ('6', 6, 1), ('7', 7, 1)]
res = {name: [] for name, _, _ in LS}; ctl = True
for q in map(int, sys.argv[1:]):
    log = field(q); m = q*q + q + 1; one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    pts = Counter((log[sub(one, y)] % m, log[y] % m) for y in log if sub(one, y) in log)
    for name, a, d in LS:
        if gcd(d, m) != 1: continue
        l = a * pow(d, -1, m) % m
        if gcd(l, m) != 1: continue
        P = sum(c * pts.get((l * x % m, l * y % m), 0) for (x, y), c in pts.items())
        if name in ('2', '-1'): ctl &= P == (q - 2)**2
        if name == '-2': ctl &= P == (q - 2)**2 + q*q - q - 2 + b(q)
        res[name].append((P - (q - 2)**2 - q*q) / q)
print('CONTROL P(2)=P(-1)=(q-2)^2 and P(-2) theorem:', 'PASS' if ctl else 'FAIL')
for name, _, _ in LS:
    v = res[name]
    if len(v) > 2: print('l=%-4s n=%2d  mean r=%7.3f  sd r=%6.3f  max|r|=%6.2f' % (name, len(v), statistics.mean(v), statistics.stdev(v), max(map(abs, v))))
