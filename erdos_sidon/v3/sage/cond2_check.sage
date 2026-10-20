R = PolynomialRing(QQ, ['x%d' % i for i in range(6)]); xs = list(R.gens())
xi = xs + [-xs[0]-xs[3], -xs[1]-xs[4], -xs[2]-xs[5]]
def X(j): return xi[j % 9]
Fr = R.fraction_field()
shift = R.hom([X(j+1) for j in range(6)], R)
def tau(f, k=1):
    for _ in range(k): f = shift(f.numerator())/shift(f.denominator())
    return f
A = sum(Fr(X(3*i)*X(3*i+4))/X(3*i+1) for i in range(3))
B = sum(Fr(X(3*i)*X(3*i+2))/X(3*i-1) for i in range(3))
C = sum(Fr(X(3*i)*X(3*i+4)*X(3*i+2))/(X(3*i+1)*X(3*i-1)) for i in range(3))
# Dickson matrix of f(Z) = A Z^r + B Z on (Z, Z^r, Z^{r^2}); row i = tau^i applied to (B, A, 0) shifted
D = matrix(Fr, [[B, A, 0], [0, tau(B), tau(A)], [tau(A,2), 0, tau(B,2)]])
print("det D == N(A)+N(B) == 0:", D.det().numerator() == 0)
adj = D.adjugate()
c = vector(Fr, [C, tau(C), tau(C,2)])
for k in range(3):
    row = adj.row(k)
    nz = any(e.numerator() != 0 for e in row)
    val = row * c
    print("adj row", k, "nonzero:", nz, " row·(C,C^r,C^r2) == 0:", val.numerator() == 0)
