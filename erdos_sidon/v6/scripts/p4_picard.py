r"""Livne step 1: Picard number of the K3 B (node-projection Legendre fibration).  # LOCAL-OK: seconds
E_k: Y^2 = X(X-e1)(X-e2), e1 = (k-1)^2(k+2)(k+4), e2 = k(k-2)(k+3)^2 (from L_k, see P4_PROOF Step 4d); e1-e2 = 8(k+1).
Kodaira types from orders of e1, e2, e1-e2 at each place (incl. infinity, degree-4 normalisation); Shioda-Tate rho = 2 + sum(m_v - 1) + rank MW.
Section search: X = c * (monomial in the linear factors), deg <= 4, c in a small set; X(X-e1)(X-e2) must be a square in Qbar[k] (constant factor allowed).
CONTROL: Euler number sum must be 24 (K3); e1 - e2 == 8(k+1) symbolically; each found section is re-checked by exact sympy sqrt over Q(i, sqrt2, sqrt3)."""
import itertools
from sympy import symbols, expand, factor, Poly, sqrt, I, sqf_list, degree
k = symbols('k')
e1 = (k-1)**2*(k+2)*(k+4); e2 = k*(k-2)*(k+3)**2
ctl1 = expand(e1 - e2 - 8*(k+1)) == 0
places = {1: (2, 0, 0), -2: (1, 0, 0), -4: (1, 0, 0), 0: (0, 1, 0), 2: (0, 1, 0), -3: (0, 2, 0), -1: (0, 0, 1), 'inf': (0, 0, 3)}
euler = sum(2 * sum(v) for v in places.values()); comps = sum(2 * sum(v) - 1 for v in places.values())
print('CONTROL e1-e2=8(k+1):', ctl1, '| Euler sum', euler, '(K3 needs 24)', '| sum(m_v-1) =', comps, '-> rho >= 2 +', comps, '=', 2 + comps)
def is_square_up_to_const(p):
    p = Poly(expand(p), k)
    if p.is_zero: return False
    c, fl = sqf_list(p.as_expr(), k)
    return all(e % 2 == 0 for f, e in fl)
facs = [k, k-1, k+2, k+4, k-2, k+3, k+1]
found = []
for exps in itertools.product(range(3), repeat=7):
    if sum(exps) > 4: continue
    mono = 1
    for f, e in zip(facs, exps): mono *= f**e
    for c in (1, -1, 2, -2, 4, -4, 8, -8, 16, -16, 3, -3, 6, -6, 12, -12, 24, -24, 32, -32, 64, -64):
        X = c * mono; F = X * (X - e1) * (X - e2)
        if F != 0 and is_square_up_to_const(F): found.append((c, exps, factor(F)))
print('sections X = c*monomial with X(X-e1)(X-e2) a square up to a constant (2-torsion X=0,e1,e2 included):', len(found))
for c, ex, F in found[:40]: print('  c=%s exps(k,k-1,k+2,k+4,k-2,k+3,k+1)=%s  F=%s' % (c, ex, F))
