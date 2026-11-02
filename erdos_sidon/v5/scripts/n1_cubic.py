r"""C(3) vs C(-2): count (c,d) in F*^2 whose F_q-polynomial has an irreducible cubic factor.  # LOCAL-OK: seconds
Hypothesis (hand): P(l) - (q-2)^2 = 3 * N(l), N(l) = #{(c,d): poly_l has a cubic irreducible factor} (each gives 3 roots in K\F).
l=3: (c-d)y^3 + 3d y^2 - 3d y + (d-1);  l=-2: c(1-y)^2 + d y^2 - y^2(1-y)^2.  Control: compare 3N with P from n1_conic (27,189,495 at q=5,11,17)."""
import sys
from sympy import symbols, Poly, GF
y = symbols('y')
for q in map(int, sys.argv[1:]):
    N = {}
    for name, f in (('3', lambda c, d: (c - d) * y**3 + 3 * d * y**2 - 3 * d * y + d - 1), ('-2', lambda c, d: c * (1 - y)**2 + d * y**2 - y**2 * (1 - y)**2)):
        n = 0
        for c in range(1, q):
            for d in range(1, q):
                P = Poly(f(c, d), y, modulus=q)
                if P.is_zero: continue
                n += sum(e for g, e in P.factor_list()[1] if g.degree() == 3)
        N[name] = n
    print('q=%d  N(3)=%d N(-2)=%d  -> (q-2)^2 + 3N = %d, %d' % (q, N['3'], N['-2'], (q-2)**2 + 3*N['3'], (q-2)**2 + 3*N['-2'])); sys.stdout.flush()
