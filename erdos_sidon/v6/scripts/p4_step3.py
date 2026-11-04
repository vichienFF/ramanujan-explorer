r"""P4 proof step 3 (hand): for a genuine quartic member (c+d != 0) with only simple roots in F_q, the number of distinct roots is 0,1,2 or 4
(3 roots force the 4th), so with N_k = sum over members of (#roots)_k:  n1 = N1 - N2 + N3/3.  # LOCAL-OK: seconds
Corrections: members with repeated roots and degenerate members (c+d=0, degree <= 3) are counted separately here.
Prints N3 and the decomposition so the closed form of N3 (where b_q should enter) can be guessed, and checks
  #(1,3) = n1(simple-root, genuine quartic) exactly.
CONTROL: #(1,3) brute force = target ((q-2)(q+1)+b_q)/3 minus degenerate (3,) members, cross-checked with type_census output."""
import sys
from sympy import Poly, symbols
y = symbols('y')
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
for q in map(int, sys.argv[1:] or [5, 7, 11, 13, 17, 19]):
    N = [0, 0, 0, 0]; t13 = 0; deg3 = 0; rep = 0; n1 = 0; N_g = [0, 0, 0, 0]
    for c in range(1, q):
        for d in range(1, q):
            P = Poly(c * y**4 + d * (1 - y)**4 - 1, y, modulus=q)
            fl = P.factor_list()[1]; degs = sorted(f.degree() for f, e in fl for _ in range(e))
            roots = [v for v in range(q) if P.eval(v) % q == 0]; k = len(roots)
            for j in range(1, 4): N[j] += {1: k, 2: k * (k - 1), 3: k * (k - 1) * (k - 2)}[j]
            genuine = (c + d) % q != 0; simple = all(e == 1 for f, e in fl)
            if genuine and simple:
                for j in range(1, 4): N_g[j] += {1: k, 2: k * (k - 1), 3: k * (k - 1) * (k - 2)}[j]
                n1 += k == 1
            if not genuine: deg3 += 1
            elif not simple: rep += 1
            if 3 in degs: t13 += 1
    lhs = N_g[1] - N_g[2] + N_g[3] // 3
    print('q=%d | N1 %d N2 %d N3 %d | genuine-simple: n1 %d vs N1-N2+N3/3 %d %s | members: degenerate %d, repeated-root %d | cubic-factor %d target %d' % (
        q, N[1], N[2], N[3], n1, lhs, 'MATCH' if n1 == lhs else 'NO', deg3, rep, t13, ((q - 2) * (q + 1) + bq(q)) // 3), flush=True)
