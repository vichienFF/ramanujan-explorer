# Kill-test Step 4q: in char 5 (field F_25, contains i) the fibration has I6 at k=1,2,inf and I2 at k=-2,0,-1 (trivial rank 20).  # LOCAL-OK: seconds
# MW rank >= 2 of the reduced 11 sections => rho = 22 (supersingular). Shioda heights with the char-5 fibre list.
# CONTROLS: torsion h=0, h(2P)=4h(P), h(P+T)=h(P) (same as p4_shioda), and the char-0 script still gives rank 2 (run separately).
from sage.all import GF, PolynomialRing, EllipticCurve, matrix, QQ
K = GF(25, 'w'); i = K(-1).sqrt(); R = PolynomialRing(K, 'k'); k = R.gen(); F = R.fraction_field()
e1 = (k-1)**2*(k+2)*(k+4); e2 = k*(k-2)*(k+3)**2; E = EllipticCurve(F, [0, -(e1+e2), 0, e1*e2, 0])
FIN = [(1, 3, 0), (2, 3, 0), (-2, 1, 0), (0, 1, 0), (-1, 1, 'e1')]
def ordv(f, v):
    f = F(f)
    return 10**6 if f == 0 else R(f.numerator()).valuation(k - v) - R(f.denominator()).valuation(k - v)
def deg(f):
    f = F(f); return R(f.numerator()).degree() - R(f.denominator()).degree() if f != 0 else -10**6
def h(P):
    if P.is_zero(): return QQ(0)
    x = F(P[0]); PO = QQ(0)
    for f, mlt in R(x.denominator()).factor(): PO += QQ(mlt * f.degree()) / 2
    oinf = 4 - deg(x)
    if oinf < 0: PO += QQ(-oinf) / 2
    c = QQ(0)
    for v, r, node in FIN:
        o = ordv(x - (e1 if node == 'e1' else 0), v)
        if ordv(x, v) >= 0 and o > 0: j = min(o, r); c += QQ(j * (2*r - j)) / (2*r)
    oi = 4 - deg(x - e1)
    if oinf >= 0 and oi > 0: j = min(oi, 3); c += QQ(j * (6 - j)) / 6
    return 4 + 2 * PO - c
S = [(1,(0,0,0,1,1,0,2)),(1,(0,0,1,1,0,2,0)),(1,(0,1,0,1,1,1,0)),(1,(0,1,1,0,1,1,0)),(1,(0,2,0,0,0,2,0)),(-1,(0,2,1,0,1,0,0)),(-1,(1,0,0,1,0,2,0)),
     (1,(1,0,1,1,1,0,0)),(1,(1,1,0,1,0,1,0)),(1,(1,1,1,0,0,1,0)),(1,(1,2,0,0,1,0,0))]
facs = [k, k-1, k+2, k+4, k-2, k+3, k+1]; P = []
for c, ex in S:
    X = R(c)
    for f, n in zip(facs, ex): X *= f**n
    ok, Y = (X*(X-e1)*(X-e2)).is_square(root=True); assert ok; P.append(E(X, Y))
T = [E(0, 0), E(e1, 0), E(e2, 0)]
ctl = all(h(t) == 0 for t in T) and all(h(2*p) == 4*h(p) for p in P) and all(h(p + t) == h(p) for p in P for t in T)
G = matrix(QQ, len(P), len(P), lambda a, b: (h(P[a] + P[b]) - h(P[a]) - h(P[b])) / 2)
print('CONTROLS:', 'PASS' if ctl else 'FAIL', '| char-5 heights', [h(p) for p in P], '| Gram rank', G.rank(), '->', 'rho = 22 (supersingular)' if G.rank() >= 2 else 'rho < 22: hypothesis NOT supported')
