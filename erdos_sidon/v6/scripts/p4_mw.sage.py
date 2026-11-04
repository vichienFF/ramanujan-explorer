# MW rank lower bound for B's fibration by specialisation (independence at k0 implies independence over Qbar(k)).  # LOCAL-OK: seconds
# CONTROL: the 2-torsion point (0,0) must have height 0 and every section must lie on E_k0.
from sage.all import QQ, EllipticCurve, matrix, sqrt, Integer
def e(k): return ((k-1)**2*(k+2)*(k+4), k*(k-2)*(k+3)**2)
# sections with X = c*monomial (from p4_picard.py, positive-constant ones), exps over (k,k-1,k+2,k+4,k-2,k+3,k+1)
S = [(1,(0,0,1,1,0,2,0)),(1,(0,1,0,1,1,1,0)),(1,(0,1,1,0,1,1,0)),(1,(0,2,0,0,0,2,0)),(1,(1,0,1,1,1,0,0)),(1,(1,1,0,1,0,1,0)),(1,(1,1,1,0,0,1,0)),(1,(1,2,0,0,1,0,0))]
for k0 in (5, 7, 11):
    a, b = e(QQ(k0)); E = EllipticCurve(QQ, [0, -(a+b), 0, a*b, 0])
    facs = [k0, k0-1, k0+2, k0+4, k0-2, k0+3, k0+1]; P = []
    for c, ex in S:
        X = QQ(c)
        for f, n in zip(facs, ex): X *= f**n
        Y2 = X*(X-a)*(X-b)
        if Y2.is_square(): P.append(E(X, Y2.sqrt()))
    T = E(0, 0); ctl = T.height() == 0
    M = matrix([[p.height_pairing(r) if hasattr(p,'height_pairing') else 0 for r in P] for p in P]) if P else None
    G = E.height_pairing_matrix(P) if P else None
    print('k0=%d: %d rational sections, CONTROL torsion height 0: %s, rank of height matrix = %s' % (k0, len(P), ctl, G.rank() if G is not None else 0))
# Exact independence: LLL-reduce the points (Sage finds integer relations); count non-torsion basis vectors. Also singular values of the height matrix.
for k0 in (5, 7, 11, 13):
    a, b = e(QQ(k0)); E = EllipticCurve(QQ, [0, -(a+b), 0, a*b, 0]); facs = [k0, k0-1, k0+2, k0+4, k0-2, k0+3, k0+1]; P = []
    for c, ex in S:
        X = QQ(c)
        for f, n in zip(facs, ex): X *= f**n
        Y2 = X*(X-a)*(X-b)
        if Y2.is_square(): P.append(E(X, Y2.sqrt()))
    sv = sorted(E.height_pairing_matrix(P).change_ring(__import__('sage.all', fromlist=['RDF']).RDF).singular_values())
    print('k0=%d: singular values of height matrix: %s' % (k0, ['%.2e' % s for s in sv]))
