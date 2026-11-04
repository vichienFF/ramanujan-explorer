r"""P4 Step 2 hand proof check: N2 = q^2 - 4q + 10 + 5 phi(-1).  # LOCAL-OK: seconds
Proof (P4_PROOF.md Step 2): m = |mu_4(F_q)| = 3 + phi(-1).
 y1 in {0,1}: y1=0 forces d=1, then y2=1 (c=1) or y2 notin{0,1} with c=(1-v2^4)/y2^4 != 0 iff v2 notin mu_4 -> q - m; same for y1=1.
 y1 generic, y2 in {0,1}: 2(q-1-m).
 both generic: t=y/(1-y) in T = F_q^* \ {-1} (|T| = q-2), equation c t^4 + d = (1+t)^4. With coordinates (X,Y,Z)=(t,1,-(1+t)) on X+Y+Z=0,
  degeneracy classes A: t1^4=t2^4, B: (1+t1)^4=(1+t2)^4, C: ((1+t1)/t1)^4=((1+t2)/t2)^4; any two imply the third.
  none -> 1 solution; exactly one -> 0 (inconsistent / c=0 / d=0); all three -> q-2 solutions (c free, c != 0, d != 0).
  |A|=|B|=|C| = (m-1)(q-3) (S3 symmetry of the line), |ABC| = (m-1)(m-2) (t1 = (eta-1)/(zeta-eta), zeta,eta in mu_4\{1}, zeta != eta).
 N2 = (q-2)(q-3) - [3(m-1)(q-3) - 2(m-1)(m-2)] + (q-2)(m-1)(m-2) + 2(q-m) + 2(q-1-m).
CONTROL: p4_n3.py independent brute force values N2 at q=5..19 (20,26,82,132,236,290) and direct brute-force class sizes |A|,|B|,|C|,|ABC| per q."""
import sys
from sympy import symbols, expand
Q, F1 = symbols('q f1')
def n2(q, m): return (q - 2) * (q - 3) - (3 * (m - 1) * (q - 3) - 2 * (m - 1) * (m - 2)) + (q - 2) * (m - 1) * (m - 2) + 2 * (q - m) + 2 * (q - 1 - m)
sym = [expand(n2(Q, 3 + f) - (Q**2 - 4 * Q + 10 + 5 * f)) == 0 for f in (1, -1)]
print('symbolic: hand count == q^2-4q+10+5phi(-1) for phi(-1)=+1,-1:', sym)
REF = {5: 20, 7: 26, 11: 82, 13: 132, 17: 236, 19: 290}
ctl = all(n2(q, 4 if q % 4 == 1 else 2) == v for q, v in REF.items())
print('CONTROL vs p4_n3.py brute force q=5..19:', 'PASS' if ctl else 'FAIL')
cls = True
for q in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
    m = 4 if q % 4 == 1 else 2; T = [t for t in range(1, q) if t != q - 1]
    p4 = lambda a: pow(a % q, 4, q); inv = lambda a: pow(a, q - 2, q)
    A = B = C = ABC = 0
    for t1 in T:
        for t2 in T:
            if t1 == t2: continue
            a = p4(t1) == p4(t2); b = p4(1 + t1) == p4(1 + t2); c = p4((1 + t1) * inv(t1)) == p4((1 + t2) * inv(t2))
            A += a; B += b; C += c; ABC += a and b and c
            if (a + b + c) == 2: cls = False                       # 'any two imply the third'
    cls &= (A, B, C, ABC) == ((m - 1) * (q - 3),) * 3 + ((m - 1) * (m - 2),)
print('class sizes |A|=|B|=|C|=(m-1)(q-3), |ABC|=(m-1)(m-2), two-imply-third, exact q=5..37:', cls)
sys.exit(0 if all(sym) and ctl and cls else 1)
