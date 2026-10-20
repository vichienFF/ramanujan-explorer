# Independent re-check of the symbolic identities directly over GF(p) and ZZ-content checks
import sys
for base in [QQ, GF(2), GF(3), GF(5), GF(7)]:
    R = PolynomialRing(base, ['x%d' % i for i in range(6)]); xs = list(R.gens())
    xi = xs + [-xs[0]-xs[3], -xs[1]-xs[4], -xs[2]-xs[5]]
    X = lambda j: xi[j % 9]
    Fr = R.fraction_field()
    shift = R.hom([X(j+1) for j in range(6)], R)
    def tau(f, k=1):
        f = Fr(f)
        for _ in range(k): f = shift(f.numerator())/shift(f.denominator())
        return f
    # check tau^3 maps x0->x3, x3->-x0-x3 (phi) and tau^9 = id on all gens
    ok9 = all(tau(g,9) == Fr(g) for g in xs)
    A = sum(Fr(X(3*i)*X(3*i+4))/X(3*i+1) for i in range(3))
    B = sum(Fr(X(3*i)*X(3*i+2))/X(3*i-1) for i in range(3))
    C = sum(Fr(X(3*i)*X(3*i+4)*X(3*i+2))/(X(3*i+1)*X(3*i-1)) for i in range(3))
    # A,B,C must be tau^3-invariant (they lie in F)
    inF = all(tau(E,3) == E for E in [A,B,C])
    N = lambda f: f*tau(f)*tau(f,2)
    id1 = (N(A)+N(B)) == 0
    D = matrix(Fr, [[B, A, 0], [0, tau(B), tau(A)], [tau(A,2), 0, tau(B,2)]])
    adj = D.adjugate(); c = vector(Fr, [C, tau(C), tau(C,2)])
    id2 = all(v == 0 for v in adj*c)
    minor = D[0,0]*D[1,1]-D[0,1]*D[1,0]
    # exact factorisation of A: A*xi1*xi4*xi7 == -(xi1 xi3 - xi0 xi4)(xi1^2+xi1 xi4+xi4^2) ?
    lhs = R(A*X(1)*X(4)*X(7))
    fac = (X(1)*X(3)-X(0)*X(4))*(X(1)**2+X(1)*X(4)+X(4)**2)
    print(base, "tau^9=id:", ok9, "| A,B,C phi-inv:", inF, "| N(A)+N(B)=0:", id1, "| adj(D)c=0:", id2,
          "| A*xi1xi4xi7 = +fac:", lhs == fac, " = -fac:", lhs == -fac)
    sys.stdout.flush()
