# Galois action of Gal(Q(i)/Q) on MW(B)(x)Q: trace of sigma (i -> -i) must be 0 so that m(q) = trace Frob on MW(x)Q = 1 + (-1/q).  # LOCAL-OK: seconds
# Uses exact Shioda heights from p4_shioda.sage.py (its controls re-run on import). CONTROL: sigma fixes the Q-rational section P1 (<sP1,P1> = h(P1)), and sigma^2 = id.
import sys; sys.argv = ['x']
exec(open('p4_shioda.sage.py').read().split("print('heights:'")[0])
def conjF(f):
    f = F(f); cj = lambda p: R(p).map_coefficients(lambda c: c.conjugate())
    return F(cj(f.numerator())) / F(cj(f.denominator()))
def sig(Pt): return E(conjF(Pt[0]), conjF(Pt[1]))
def pair(A_, B_): return (h(A_ + B_) - h(A_) - h(B_)) / 2
b = [P[0], P[1]]; Gm = matrix(QQ, 2, 2, lambda a, c: pair(b[a], b[c])); Mm = matrix(QQ, 2, 2, lambda a, c: pair(sig(b[a]), b[c]))
S = Gm.inverse() * Mm.transpose()   # columns = coords of sigma(b_a) in basis b
ok = pair(sig(P[1]), P[1]) == h(P[1]) and S * S == 1
print('CONTROL sigma fixes Q-rational P1 and sigma^2=1:', 'PASS' if ok else 'FAIL', '| sigma matrix', S.list(), '| trace', S.trace(), '-> m(q) = 1 + (-1/q)' if S.trace() == 0 else '-> m(q) claim WRONG')
