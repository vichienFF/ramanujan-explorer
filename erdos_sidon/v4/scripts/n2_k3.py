r"""Hand step (2026-10-30): W + #{TQ=0} = What := sum_{P^2(F_q)} chi(G), G = (TQ-N)(TQ-9N), T=e1, Q=e2, N=e3 of (x,y,z) = (a, a^q, a^{q^2}).  # LOCAL-OK: seconds
(TQ-N = (x+y)(y+z)(z+x).)  For q == 2 mod 3 (z=0, #{TQ=0}=2q+2): N(-2) formula <=> What_twisted = 0 <=> the double sextic K3  w^2 = G,
Frobenius-twisted by the 3-cycle, has exactly q^2+q+1 points.  H3 (new): the UNTWISTED sum over x,y,z in F_q is also 0 for q == 2 mod 3.
CONTROL: What_twisted = W + 2q+2 - z with W, z from n2_wsum.py logic (q=5: W=-12 -> 0; q=7: W=-12, z=2 -> 2)."""
import sys
from fq3 import field, p2_reps, chi
for q in map(int, sys.argv[1:]):
    mul, inv, tr = field(q)
    tw = 0
    for u in p2_reps(q):
        T = tr(u); N = 1  # N(a) for representative: compute via a*a^q*a^{q^2}; use U = Tr(1/a): Q = N*U
        a2 = mul(u, u); a3 = mul(a2, u)
        # Newton: e1=T, p2=Tr(a^2), p3=Tr(a^3) -> e2=(T^2-p2)/2, e3=(p3 - T p2 + e2 T)/3... use e3 = (T^3 - 3 T p2 + 2 p3)/6
        p2, p3 = tr(a2), tr(a3)
        Q = (T * T - p2) * pow(2, -1, q) % q; N = (T**3 - 3 * T * p2 + 2 * p3) * pow(6, -1, q) % q
        tw += chi((T * Q - N) * (T * Q - 9 * N), q)
    un = 0
    for x, y, z in p2_reps(q):
        T, Q, N = x + y + z, x*y + y*z + z*x, x*y*z
        un += chi((T * Q - N) * (T * Q - 9 * N), q)
    ref = {5: 0, 7: 2}.get(q)
    print('q=%d (mod3=%d) What_twisted=%d%s  What_untwisted=%d' % (q, q % 3, tw, (' CONTROL ' + ('PASS' if tw == ref else 'FAIL')) if ref is not None else '', un))
