# General certificate. Smooth points P_i of G over number fields K_i (simple factors on rational slices / at infinity).
# The geometric component through P_i is defined over a subfield of K_i, so k = #components divides every [K_i:Q];
# if gcd = 1 -> k = 1. Else factor G over the smallest K_i: irreducible there -> k = 1.
from math import gcd
from sympy import symbols, Poly, factor_list, Rational, QQ, CRootOf
s, t = symbols('s t')
def smooth_fields(G, nslices=24):
    P = Poly(G, s, t); d = P.total_degree(); Ps = P.diff(s); Pt = P.diff(t); out = []
    top = Poly(sum(c*s**i*t**j for (i, j), c in P.terms() if i + j == d), s, t)
    for f, m in factor_list(top.as_expr().subs(t, 1), s)[1]:
        if m == 1 and Poly(f, s).degree() >= 1: out.append(("inf", Poly(f, s)))
    for k in range(2, nslices):
        X = Rational((-1)**k*(k//2), 1 + (k % 3))
        for fix, var in ((s, t), (t, s)):
            hh = Poly(P.as_expr().subs(fix, X), var)
            if hh.degree() < 1: continue
            a = Poly(Ps.as_expr().subs(fix, X), var); b = Poly(Pt.as_expr().subs(fix, X), var)
            for f, m in factor_list(hh.as_expr(), var)[1]:
                f = Poly(f, var)
                if m == 1 and (f.gcd(a).degree() == 0 or f.gcd(b).degree() == 0):
                    out.append(((str(fix), str(X)), f))
    return out
def cert(G):
    F = smooth_fields(G); g = 0
    for w, f in F: g = gcd(g, f.degree())
    if g == 1: return "gcd of smooth-point field degrees = 1 (%s)" % sorted({f.degree() for _, f in F})[:6]
    w, f = min(F, key=lambda x: x[1].degree())
    if f.degree() == 1: return "rational smooth point"
    K = QQ.algebraic_field(CRootOf(f.as_expr(), 0))
    fl = Poly(G, s, t, domain=K).factor_list()[1]
    if len(fl) == 1 and fl[0][1] == 1:
        return "smooth pt over degree-%d field at %s; G irreducible over it" % (f.degree(), w)
    return None
