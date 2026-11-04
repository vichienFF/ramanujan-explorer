# MW rank over Q(i): all 11 sections from p4_picard.py (incl. the 3 needing sqrt(-1)); rank from singular values of the height matrix.  # LOCAL-OK: seconds
# CONTROL: the 8 Q-rational sections alone must again give exactly one non-zero singular value (p4_mw.sage.py result).
from sage.all import QQ, NumberField, polygen, EllipticCurve, RDF
x = polygen(QQ); K = NumberField(x**2 + 1, 'i')
def e(k): return ((k-1)**2*(k+2)*(k+4), k*(k-2)*(k+3)**2)
S = [(1,(0,0,0,1,1,0,2)),(1,(0,0,1,1,0,2,0)),(1,(0,1,0,1,1,1,0)),(1,(0,1,1,0,1,1,0)),(1,(0,2,0,0,0,2,0)),(-1,(0,2,1,0,1,0,0)),(-1,(1,0,0,1,0,2,0)),
     (1,(1,0,1,1,1,0,0)),(1,(1,1,0,1,0,1,0)),(1,(1,1,1,0,0,1,0)),(1,(1,2,0,0,1,0,0))]
QRAT = [1,2,3,4,7,8,9,10]
for k0 in (5, 11):
    a, b = e(K(k0)); E = EllipticCurve(K, [0, -(a+b), 0, a*b, 0]); facs = [k0, k0-1, k0+2, k0+4, k0-2, k0+3, k0+1]; P = []
    for c, ex in S:
        X = K(c)
        for f, n in zip(facs, ex): X *= f**n
        Y2 = X*(X-a)*(X-b); assert Y2.is_square(), (c, ex); P.append(E(X, Y2.sqrt()))
    def rk(L): return sum(1 for s in E.height_pairing_matrix(L).change_ring(RDF).singular_values() if s > 1e-6)
    print('k0=%d: CONTROL Q-rational subset rank %d (expect 1) | all 11 over Q(i): rank %d' % (k0, rk([P[j] for j in QRAT]), rk(P)))
