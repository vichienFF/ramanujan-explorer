r"""P4 Step 5d: checks of the HAND proof of the repeated-root correction sums.  # LOCAL-OK: seconds
Proof (P4_PROOF.md Step 5d): member with double root u in F_q\{0,1}: (c,d)=(u^-3,(1-u)^-3); f*u^3(1-u)^3 = (y-u)^2 Q_u(y),
 disc_y Q_u = -8u^2(u-1)^2(u^2-u+1), Q_u(u) = 6u^2(u-1)^2 != 0 (no triple roots), lead(Q_u) = 3u^2-3u+1 (=0 iff degenerate c+d=0).
 Generic u (u not 0,1; 3u^2-3u+1 != 0; u^2-u+1 != 0): G = q-4-2phi(-3) members, distinct roots k = 2 + chi(-2(u^2-u+1)).
 Special member (-1,-1) = -2(y^2-y+1)^2: 1+phi(-3) distinct roots (both double).  S = sum_generic chi(-2(u^2-u+1))
   = chi(-2)[-1 - 2 - (1+phi(-3)) chi(6)]  (sum_all chi(u^2-u+1) = -1 since disc=-3 != 0; u=0,1 give 1; on 3u^2-3u+1=0, u^2-u+1 = 2/3).
 => rep N1 = 2G + S + (1+phi(-3)); rep N3 = 6 * (G+S)/2; rep N2 = rep N3 + (1+phi(-3)); members = G + 1.
CONTROL: final values equal p4_closed.py brute force (REF at q=5..43, independent gcd-based detection)."""
import sys
from sympy import symbols, Poly, div, discriminant, factor, expand
y, u = symbols('y u'); v = 1 - u
n = expand(y**4 * v**3 + (1 - y)**4 * u**3 - u**3 * v**3)
Qq, r = div(Poly(n, y), Poly((y - u)**2, y)); Qe = Qq.as_expr()
ok = [r.is_zero, expand(discriminant(Qe, y) + 8 * u**2 * (u - 1)**2 * (u**2 - u + 1)) == 0,
      expand(Qe.subs(y, u) - 6 * u**2 * (u - 1)**2) == 0, expand(Poly(Qe, y).LC() - (3 * u**2 - 3 * u + 1)) == 0,
      expand(u**3 + v**3 - (3 * u**2 - 3 * u + 1)) == 0]
print('symbolic steps:', ok)
def chi(a, q): return 0 if a % q == 0 else (1 if pow(a % q, (q - 1) // 2, q) == 1 else -1)
REF = {5: (4, 9, 18, 18), 7: (2, 5, 8, 6), 11: (10, 15, 18, 18), 13: (8, 17, 26, 24), 17: (16, 27, 36, 36), 19: (14, 23, 26, 24),
       23: (22, 45, 72, 72), 29: (28, 57, 90, 90), 31: (26, 53, 80, 78), 37: (32, 65, 98, 96), 41: (40, 75, 108, 108), 43: (38, 71, 98, 96)}
ctl = True; Sok = True
for q, ref in REF.items():
    f3 = chi(-3, q); G = q - 4 - 2 * f3
    S = chi(-2, q) * (-3 - (1 + f3) * chi(6, q))
    Sbf = sum(chi(-2 * (w * w - w + 1), q) for w in range(2, q) if (3 * w * w - 3 * w + 1) % q and (w * w - w + 1) % q)
    Sok &= S == Sbf
    vals = (G + 1, 2 * G + S + (1 + f3), 3 * (G + S) + (1 + f3), 3 * (G + S))
    ctl &= vals == ref
print('character-sum closed form S exact (q=5..43):', Sok)
print('CONTROL hand formulas vs brute force (members, rep N1, N2, N3) q=5..43:', 'PASS' if ctl else 'FAIL')
sys.exit(0 if all(ok) and Sok and ctl else 1)
