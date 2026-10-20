R = PolynomialRing(QQ, ['x%d' % i for i in range(6)]); xs = list(R.gens())
xi = xs + [-xs[0]-xs[3], -xs[1]-xs[4], -xs[2]-xs[5]]
def X(j): return xi[j % 9]
Fr = R.fraction_field()
A = sum(Fr(X(3*i)*X(3*i+4))/X(3*i+1) for i in range(3))
num = A.numerator(); den = A.denominator()
print("deg num:", num.total_degree(), " den:", den.factor())
print("num factor:", num.factor())
# phi-fixed condition: x^(q-1) in F  <=> x_1/x_0 = phi(x)/x invariant under phi <=> xi_3^2 = xi_0*xi_6 (i.e. (phi x)^2 = x * phi^2 x)
fixed = X(3)**2 - X(0)*X(6)
print("phi-fixed poly:", fixed.factor())
