r"""Proof of F3(4) = (q-2)(q+1) + b_q, step checks (hand derivations, think-then-test).  # LOCAL-OK: seconds
f_{c,d}(y) = c y^4 + d (1-y)^4 - 1, (c,d) in (F_q^*)^2.
Step 1 (hand): N1 = sum_{c,d} #{y in F_q : f(y) = 0} = (q-2)^2 + 2(q-1)   [y not in {0,1}: q-2 each; y=0: d=1; y=1: c=1].
Step 2 (hand): ordered pairs of distinct roots (y1,y2) in F_q: with t = y/(1-y) (y != 1) the determinant is prop. to t1^4 - t2^4;
  the system has a unique (c,d) iff t2^4 != t1^4; exact count printed for comparison with the formula to be derived.
Target (H-M4 / P(4) observation): #(c,d) with an irreducible cubic factor = ((q-2)(q+1) + b_q)/3.
CONTROL: the brute-force cubic-factor count equals the proved l=-2 value for the same q (type_census.py, Thm 3c)."""
import sys
from sympy import Poly, symbols
y = symbols('y')
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
for q in map(int, sys.argv[1:] or [5, 7, 11, 13, 17]):
    N1 = 0; N2 = 0; cub = 0
    for c in range(1, q):
        for d in range(1, q):
            roots = [v for v in range(q) if (c * pow(v, 4, q) + d * pow(1 - v, 4, q) - 1) % q == 0]
            N1 += len(roots); N2 += len(roots) * (len(roots) - 1)
            P = Poly(c * y**4 + d * (1 - y)**4 - 1, y, modulus=q)
            if not P.is_zero and any(f.degree() == 3 for f, e in P.factor_list()[1]): cub += 1
    ok1 = N1 == (q - 2) ** 2 + 2 * (q - 1); target = ((q - 2) * (q + 1) + bq(q)) // 3
    print('q=%d (q mod 4 = %d) | step1 N1=%d formula %s | N2(ordered pairs)=%d | cubic-factor count %d target %d -> %s' % (
        q, q % 4, N1, 'MATCH' if ok1 else 'NO', N2, cub, target, 'MATCH' if cub == target else 'NO'))
