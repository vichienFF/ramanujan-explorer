# Symbolic check: conjugates xi_j = tau^j(x), j mod 9, with Tr_{K/F} relations xi_j + xi_{j+3} + xi_{j+6} = 0.
R = PolynomialRing(QQ, ['x%d' % i for i in range(6)]); xs = list(R.gens())
xi = xs + [-xs[0]-xs[3], -xs[1]-xs[4], -xs[2]-xs[5]]
def X(j): return xi[j % 9]
Fr = R.fraction_field()
# tau acts as index shift j -> j+1 on the 6 free variables (images of x6,x7,x8 via relations are consistent)
shift = R.hom([X(j+1) for j in range(6)], R)
def tau(f): return shift(f.numerator()) / shift(f.denominator())
A = sum(Fr(X(3*i)*X(3*i+4))/X(3*i+1) for i in range(3))
B = sum(Fr(X(3*i)*X(3*i+2))/X(3*i-1) for i in range(3))
C = sum(Fr(X(3*i)*X(3*i+4)*X(3*i+2))/(X(3*i+1)*X(3*i-1)) for i in range(3))
def N(f): return f*tau(f)*tau(tau(f))
# consistency: tau^9 = id and tau^3 permutes (x0,x3,x6) cyclically
t9 = Fr(xs[0])
for _ in range(9): t9 = tau(t9)
print("tau^9(x0)==x0:", t9 == xs[0])
print("N(A)+N(B) == 0 :", (N(A)+N(B)).numerator() == 0)
print("N(A)-N(B) == 0 :", (N(A)-N(B)).numerator() == 0)
