r"""P4 Step 5c: symbolic + exact checks of the HAND proof of the degenerate (d=-c) correction sums.  # LOCAL-OK: seconds
Proof sketch (P4_PROOF.md Step 5c): g(y)=y^4-(1-y)^4; s=2y-1 gives g = s(s^2+1)/2 =: h(s)/2.
 N1 = #{y: g(y)!=0} = q-1-(1+phi(-1)).  N2 = #{s1!=s2, h(s1)=h(s2)!=0}: conic s1^2+s1 s2+s2^2=-1 has q-phi(-3) points (norm form, disc -3),
 minus diagonal (3s^2=-1: 1+phi(-3)), minus zero-level pairs (ordered distinct pairs from {0,+-i}: 3(1+phi(-1))).
 N3: third root s3=-s1-s2 (no s^2 term); s3 in {s1,s2} iff s2=-2s1 or s1=-2s2 (each 1+phi(-3) pairs) -> N3 = N2 - 2(1+phi(-3)).
 D3 = (q-1) - a1 - a2 - a3 with a2 = 1+phi(-3) critical values, a3 = N3/6, a1 = N1 - 2a2 - 3a3  ->  (q-phi(-3))/3.
CONTROL: the final formulas equal p4_closed.py brute-force values (deg N1..3, D3) at q=5..43 (independent script, REF from its output)."""
import sys
from sympy import symbols, expand, simplify, Rational, factor
y, s, s1, s2, Q, F1, F3 = symbols('y s s1 s2 q f1 f3')
ok = []
ok.append(expand((y**4 - (1 - y)**4) - (lambda S: S * (S**2 + 1) / 2)(2 * y - 1)) == 0)                       # g = h(s)/2
ok.append(simplify((s1**3 + s1 - s2**3 - s2) / (s1 - s2) - (s1**2 + s1 * s2 + s2**2 + 1)) == 0)                # conic
ok.append(expand((s - s1) * (s - s2) * (s + s1 + s2) - (s**3 - (s1**2 + s1 * s2 + s2**2) * s + s1 * s2 * (s1 + s2))) == 0)  # 3rd root, s^1 coeff = -(conic form) = 1 on C
ok.append(expand((s1**2 + s1 * s2 + s2**2).subs(s2, -2 * s1) - 3 * s1**2) == 0)                               # s2=-2s1 on C iff 3s1^2=-1
N1 = Q - 2 - F1; N2 = Q - F3 - (1 + F3) - 3 * (1 + F1); N3 = N2 - 2 * (1 + F3)
a2 = 1 + F3; a3 = N3 / 6; a1 = N1 - 2 * a2 - 3 * a3; D3 = (Q - 1) - a1 - a2 - a3
ok.append(simplify(D3 - (Q - F3) / 3) == 0)
print('symbolic steps:', ok)
def leg(a, q): return 0 if a % q == 0 else (1 if pow(a % q, (q - 1) // 2, q) == 1 else -1)
REF = {5: (2, 0, 0, 2), 7: (6, 4, 0, 2), 11: (10, 12, 12, 4), 13: (10, 4, 0, 4), 17: (14, 12, 12, 6), 19: (18, 16, 12, 6),
       23: (22, 24, 24, 8), 29: (26, 24, 24, 10), 31: (30, 28, 24, 10), 37: (34, 28, 24, 12), 41: (38, 36, 36, 14), 43: (42, 40, 36, 14)}
ctl = all(tuple(int(e.subs({Q: q, F1: leg(-1, q), F3: leg(-3, q)})) for e in (N1, N2, N3, D3)) == v for q, v in REF.items())
print('CONTROL hand formulas vs brute force (p4_corr/p4_closed) q=5..43:', 'PASS' if ctl else 'FAIL')
# norm-form count used in N2: #{x^2+xy+y^2 = -1} = q - phi(-3), exact check
cnt = all(sum(1 for a in range(q) for b in range(q) if (a * a + a * b + b * b + 1) % q == 0) == q - leg(-3, q) for q in REF)
print('conic point count q - phi(-3) exact on q=5..43:', cnt)
sys.exit(0 if all(ok) and ctl and cnt else 1)
