r"""C9 N(-2) bookkeeping (2026-10-30).  # LOCAL-OK: seconds
(1) Symbolic check of the hand claims: det = (y2-y1)(y1+y2-2y1y2), c = y1^2 y2^2 (y2-y1)(2-y1-y2)/det, d = (1-y1)^2(1-y2)^2 (y2^2-y1^2)/det
    => det=0 <-> 2v-u=0, c=0 <-> u=2, d=0 <-> u=0 (distinct y's not 0,1): all are factors of D -> excluded pairs contribute 0.
(2) Factorisation-type census of Q(y)=y^4-2y^3+(1-c-d)y^2+2cy-c over c,d in F_q^*, to write N(-2) = #(1)(3) via P, S2 and repeated-root types.
CONTROL: #type (1)(3) must equal the brute N(-2) of n1_cubic.py: 6, 36, 90 at q=5,11,17; and sum of all types = (q-1)^2."""
import sys
from sympy import symbols, Matrix, factor, simplify, Poly
from collections import Counter
y1, y2, y = symbols('y1 y2 y')
def symbolic_check():
    A = Matrix([[(1 - y1)**2, y1**2], [(1 - y2)**2, y2**2]]); r = Matrix([y1**2*(1 - y1)**2, y2**2*(1 - y2)**2])
    det = A.det(); c, d = A.LUsolve(r)
    ok1 = simplify(det - (y2 - y1)*(y1 + y2 - 2*y1*y2)) == 0
    ok2 = simplify(c - y1**2*y2**2*(y2 - y1)*(2 - y1 - y2)/det) == 0
    ok3 = simplify(d - (1 - y1)**2*(1 - y2)**2*(y2**2 - y1**2)/det) == 0
    print('symbolic det/c/d factorisations:', 'PASS' if ok1 and ok2 and ok3 else 'FAIL', ok1, ok2, ok3)
def census(q):
    t = Counter()
    for cc in range(1, q):
        for dd in range(1, q):
            P = Poly(y**4 - 2*y**3 + (1 - cc - dd)*y**2 + 2*cc*y - cc, y, modulus=q)
            t[tuple(sorted((g.degree(), e) for g, e in P.factor_list()[1]))] += 1
    return t
if __name__ == "__main__":  # import-safe (n2_assemble imports census)
    symbolic_check()
    ref = {5: 6, 11: 36, 17: 90}
    for q in map(int, sys.argv[1:]):
        t = census(q); n13 = t[((1, 1), (3, 1))]
        ctl = (n13 == ref[q] if q in ref else True) and sum(t.values()) == (q - 1)**2
        print('q=%d CONTROL %s | types %s' % (q, 'PASS' if ctl else 'FAIL', {k: v for k, v in sorted(t.items())}))
