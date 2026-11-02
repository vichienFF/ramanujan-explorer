# N(-2) K3 identification (2026-10-30). Pencil C_k: (x+y)(y+z)(z+x) = k xyz  (k = p-1), rational point (1:-1:0).
# CONTROL: same code on the Hesse pencil x^3+y^3+z^3 = 3 m xyz must give discriminant ~ (m^3-1)^3 (4 I3 fibres incl. infinity).
R.<k> = QQ[]; K = FractionField(R)
P2.<x,y,z> = PolynomialRing(K)
def surf(F, pt, name):
    E = EllipticCurve_from_cubic(F, pt, morphism=False).minimal_model() if False else EllipticCurve_from_cubic(F, pt, morphism=False)
    E = E.short_weierstrass_model()
    D = R(E.discriminant().numerator()) * 1; Dd = R(E.discriminant().denominator())
    j = E.j_invariant()
    print(name, '| j =', j.factor() if j != 0 else 0)
    print('   disc num', D.factor(), '| den', Dd.factor())
    return E
m = k
surf(x^3+y^3+z^3-3*m*x*y*z, [1,-1,0], 'CONTROL Hesse')
E = surf((x+y)*(y+z)*(z+x)-k*x*y*z, [1,-1,0], 'pencil')
