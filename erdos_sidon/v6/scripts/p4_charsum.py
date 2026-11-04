r"""P4 N3 route: which character sum carries b_q?  D4(u,v) = residual-quadratic discriminant (p4_resid.py, sympy symmetrize).  # LOCAL-OK: seconds
Prints S_a = sum_{u,v} chi(D4), S_b = sum_{u,v} chi(u^2-4v) chi(D4) over all of F_q^2, and fits S - (elementary) vs b_q.
CONTROL: D4 evaluated at (u,v) from a random admissible root pair equals the discriminant of the residual quadratic computed by sympy factorisation (independent route), q=13."""
import sys, random
def chi(a, q): a %= q; return 0 if a == 0 else (1 if pow(a, (q - 1) // 2, q) == 1 else -1)
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
# control: residual quadratic of (1+t)^4 - c t^4 - d with roots t1,t2 (c,d from p4_resid formulas), disc via sympy over GF(13)
from sympy import Poly, symbols, div, GF
t = symbols('t'); q = 13; ok = True; random.seed(1)
for _ in range(30):
    t1, t2 = random.sample(range(1, q - 1), 2); s, p = (t1 + t2) % q, t1 * t2 % q
    den = s * (t1 * t1 + t2 * t2) % q
    if den == 0: continue
    inv = pow(den, q - 2, q)
    c = (s + 2) * (t1 * t1 + 2 * t1 + t2 * t2 + 2 * t2 + 2) * inv % q; d = (2 * p + s) * (2 * p * p + 2 * t1 * t1 * t2 + t1 * t1 + 2 * t1 * t2 * t2 + t2 * t2) * inv % q
    F = Poly((1 + t)**4 - c * t**4 - d, t, modulus=q); Qr, r = div(F, Poly((t - t1) * (t - t2), t, modulus=q))
    if not r.is_zero: ok = False; continue
    if Qr.degree() < 2: continue
    a2, a1, a0 = [int(x) % q for x in Qr.all_coeffs()]
    ok &= chi(a1 * a1 - 4 * a2 * a0, q) == chi(-4 * D4(s, p), q)
print('CONTROL residual disc == -4*D4 (chi) at q=13:', 'PASS' if ok else 'FAIL')
if not ok: sys.exit(1)
for q in [p for p in range(5, 120) if all(p % k for k in range(2, int(p ** .5) + 1))]:
    Sa = sum(chi(D4(u, v), q) for u in range(q) for v in range(q))
    Sb = sum(chi(u * u - 4 * v, q) * chi(D4(u, v), q) for u in range(q) for v in range(q))
    print('q=%3d f-1 %+d f-2 %+d f-3 %+d b_q %+4d | S_a %+5d | S_b %+5d | S_b - b_q*chi(-1)? %+d, S_b+b_q %+d' % (
        q, chi(-1, q), chi(-2, q), chi(-3, q), bq(q), Sa, Sb, Sb - bq(q), Sb + bq(q)))
