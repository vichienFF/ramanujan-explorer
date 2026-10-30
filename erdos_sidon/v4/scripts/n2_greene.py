r"""HAND (2026-10-30): with u=y1+y2, v=y1*y2, w=2v-u, x=u-1, z=w+1 the obstruction becomes
T(q) = sum_{x,z in F_q} chi((x^2-1)(z^2-1)(x^2+1-2z)).  # LOCAL-OK: seconds
PREDICTION (stated before running): T and Greene's 3F2(4) are both tied to b_q: (i) G(4) := sum_{x,y} chi(x y (1-x)(1-y)(x-4y)) = +-b_q
(Ono 1998, Trans. AMS 350, Thm: 3F2(4)_p = 4a^2-2p if p=a^2+3b^2, 0 if p==2 mod 3 -- SOURCE to be read), and (ii) T = A(q) + k*b_q with
A polynomial, one k for all q.
CONTROL: Ono's closed form must reproduce b_q from n2_eta (independent eta-product expansion) for every tested p: b_q = 4a^2-2q, q=a^2+3b^2."""
import sys
import numpy as np
from n2_eta import b  # noqa
def chi(a, q):
    a %= q
    return 0 if a == 0 else (1 if pow(a, (q - 1) // 2, q) == 1 else -1)
def ono(q):
    if q % 3 == 2: return 0
    a = next(a for a in range(1, q) if any(a*a + 3*bb*bb == q for bb in range(1, q)))
    return 4*a*a - 2*q
qs = list(map(int, sys.argv[1:]))
print('CONTROL Ono closed form == eta coefficient:', 'PASS' if all(ono(q) == b(q) for q in qs) else 'FAIL', [(q, ono(q), b(q)) for q in qs if ono(q) != b(q)])
rows = []
for q in qs:
    G = sum(chi(x*y*(1-x)*(1-y)*(x-4*y), q) for x in range(q) for y in range(q))
    T = sum(chi((x*x-1)*(z*z-1)*(x*x+1-2*z), q) for x in range(q) for z in range(q))
    rows.append((q, G, T)); print('q=%d G(4)=%d  T=%d  b_q=%d' % (q, G, T, b(q)))
two = [r for r in rows if r[0] % 3 == 2]
cT = np.linalg.lstsq(np.array([[q, 1] for q, _, _ in two], float), np.array([r[2] for r in two], float), rcond=None)[0]
print('T on q==2 mod 3 ~ %s ; residuals elsewhere / b_q:' % np.round(cT, 4), [(q, round((T - cT @ [q, 1]) / b(q), 4)) for q, G, T in rows if q % 3 == 1])
