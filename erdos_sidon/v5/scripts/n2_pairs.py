r"""Follow-up of n2_sibling.py (its prediction 'b_q sits in N1111' FAILED: N1111 = (q-5)(q-11)/24 exactly on q==2 mod 3, tiny residuals otherwise).  # LOCAL-OK: seconds
NEW PREDICTION (stated before running): the transfer breaks at the residual quadratic. For an unordered pair {y1,y2} of distinct roots in
F_q minus {0,1} the line system fixes (c,d); if c,d != 0 the quartic = (y-y1)(y-y2)(y^2 - s y + p) with s = 2-y1-y2.
S2 = sum over admissible pairs of chi(s^2 - 4p) carries the K3 term: S2 - poly(q) = k * b_q with ONE constant k for all q==1 mod 3.
CONTROL: #admissible pairs computed two ways (direct pair loop vs sum over (c,d) of C(#roots,2) from brute force) must agree at q=7,11."""
import sys
import numpy as np
from n2_eta import b  # noqa
def chi(a, q):
    a %= q
    return 0 if a == 0 else (1 if pow(a, (q - 1) // 2, q) == 1 else -1)
def pairs(q):
    P = S = 0
    for y1 in range(2, q):
        for y2 in range(y1 + 1, q):
            A = [[(1 - y1)**2 % q, y1*y1 % q], [(1 - y2)**2 % q, y2*y2 % q]]
            det = (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % q
            if det == 0: continue
            r1 = y1*y1*(1 - y1)**2 % q; r2 = y2*y2*(1 - y2)**2 % q; di = pow(det, -1, q)
            c = (r1*A[1][1] - A[0][1]*r2) * di % q; d = (A[0][0]*r2 - r1*A[1][0]) * di % q
            if c == 0 or d == 0: continue
            # quartic y^4 - 2y^3 + (1-c-d) y^2 + 2c y - c = (y^2 - e1 y + e2)(y^2 - s y + p)
            e1 = (y1 + y2) % q; e2 = y1*y2 % q; s = (2 - e1) % q; p = (-c) * pow(e2, -1, q) % q
            P += 1; S += chi(s*s - 4*p, q)
    return P, S
def brute_pairs(q):
    t = 0
    for c in range(1, q):
        for d in range(1, q):
            n = sum((y*y*(1-y)**2 - c*(1-y)**2 - d*y*y) % q == 0 for y in range(2, q)); t += n*(n-1)//2
    return t
if __name__ == "__main__":  # import-safe (E43/E44: n2_lines imports pairs/chi)
    for q in (7, 11):
        print('CONTROL q=%d pairs %d vs brute %d %s' % (q, pairs(q)[0], brute_pairs(q), 'PASS' if pairs(q)[0] == brute_pairs(q) else 'FAIL'))
    rows = [(q,) + pairs(q) for q in map(int, sys.argv[1:])]
    two = [r for r in rows if r[0] % 3 == 2]
    A = np.array([[q*q, q, 1] for q, _, _ in two], float)
    cP = np.linalg.lstsq(A, np.array([r[1] for r in two], float), rcond=None)[0]; cS = np.linalg.lstsq(A, np.array([r[2] for r in two], float), rcond=None)[0]
    print('q==2 mod 3 fits: P ~ %s (max res %.2f) ; S2 ~ %s (max res %.2f)' % (np.round(cP, 4), max(abs(r[1] - cP @ [r[0]**2, r[0], 1]) for r in two), np.round(cS, 4), max(abs(r[2] - cS @ [r[0]**2, r[0], 1]) for r in two)))
    for q, P, S in rows:
        if q % 3 == 1:
            rs = S - cS @ [q*q, q, 1]; rp = P - cP @ [q*q, q, 1]
            print('  q=%d  P res %.2f | S2 res %.2f  b_q %d  ratio %.4f' % (q, rp, rs, b(q), rs / b(q)))
