# Genus + Jacobian of the c+d=0 pair locus C2: (h(x)-h(y))/(x-y)=0, h=(t-1)(t^2+1)/(1+t)^3, and of the repeated-root pair locus C3.  # LOCAL-OK: seconds
# CONTROL: the same routine on the c=1 locus (g(x)-g(y))/(x-y), g=(1+t)^4-t^4 (a conic, proved Step 4zf) must report genus 0.
from sage.all import QQ, PolynomialRing, Curve, EllipticCurve
R = PolynomialRing(QQ, ['x', 'y']); x, y = R.gens()
def resid(num, den):   # numerator of (num(x)/den(x) - num(y)/den(y))/(x-y)
    P = num(x)*den(y) - num(y)*den(x); return R(P // (x - y))
g = lambda t: (1+t)**4 - t**4; one = lambda t: 1
C1 = Curve(resid(g, one)); print('CONTROL c=1 locus genus:', C1.genus(), '(expect 0)')
h_num = lambda t: (t-1)*(t**2+1); h_den = lambda t: (1+t)**3
C2 = Curve(resid(h_num, h_den)); print('c+d=0 locus: degree', C2.defining_polynomial().total_degree(), 'genus', C2.genus())
try:
    E = C2.projective_closure()
    print('irreducible:', C2.is_irreducible())
except Exception as ex: print('closure err', ex)
