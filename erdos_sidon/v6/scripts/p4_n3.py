r"""Fast exact N_k = sum over (c,d) in (F_q^*)^2 of (#roots in F_q of c y^4 + d(1-y)^4 - 1)_k, k = 1,2,3.  # LOCAL-OK: seconds per q
For fixed c every y with (1-y) != 0 gives exactly one d_y = (1 - c y^4)/(1-y)^4; y = 1 is a root iff c = 1 (any d).
CONTROL: matches the sympy brute force of p4_step3.py at q = 5..19 (N1 17,37,101,145,257,325; N2 20,26,82,132,236,290; N3 18,6,54,96,216,276)
and the proved Step 1 formula N1 = (q-2)^2 + 2(q-1) for every q.
Then fits N3 per class of q mod 12 to A q^2 + B q + C + D b_q (exact integer check)."""
import sys, numpy as np
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
def Ns(q):
    ys = np.arange(q); A = pow_ = (ys ** 4) % q; B = ((1 - ys) % q) ** 4 % q
    inv = np.zeros(q, np.int64); inv[1:] = [pow(int(v), q - 2, q) for v in range(1, q)]
    N = [0, 0, 0, 0]
    for c in range(1, q):
        mask = ys != 1
        d = ((1 - c * A[mask]) % q) * inv[B[mask]] % q
        cnt = np.bincount(d, minlength=q)[1:].astype(np.int64)           # d = 0 excluded
        if c == 1: cnt += 1                                                 # y = 1 is a root for every d when c = 1
        for k in (1, 2, 3): N[k] += int(np.sum(np.prod([cnt - i for i in range(k)], axis=0)))
    return N
REF = {5: (17, 20, 18), 7: (37, 26, 6), 11: (101, 82, 54), 13: (145, 132, 96), 17: (257, 236, 216), 19: (325, 290, 276)}
ctl = all(tuple(Ns(q)[1:]) == v for q, v in REF.items())
print('CONTROL vs sympy brute force:', 'PASS' if ctl else 'FAIL')
QS = [p for p in range(5, int(sys.argv[1]) if sys.argv[1:] else 140) if all(p % d for d in range(2, int(p ** .5) + 1))]
rows = []
for q in QS:
    N = Ns(q); assert N[1] == (q - 2) ** 2 + 2 * (q - 1)
    rows.append((q, N[2], N[3], bq(q)))
print('q, N2, N3, b_q:', rows)
for r12 in (1, 5, 7, 11):
    R = [r for r in rows if r[0] % 12 == r12 and r[0] > 5]
    X = np.array([[q * q, q, 1, b] for q, _, _, b in R], float); Y = np.array([n3 for _, _, n3, _ in R], float)
    coef, *_ = np.linalg.lstsq(X, Y, rcond=None); res = Y - X @ coef
    print('q = %2d mod 12 (n=%d): N3 ~ %.4f q^2 + %.4f q + %.4f + %.4f b_q | max |residual| %.3g' % (r12, len(R), *coef, np.abs(res).max()))
# Closed form found 2026-11-02 from the residues mod 24 (5 constants from 4 classes mod 8 + the q mod 3 shift); exact check on every q:
def leg(a, q): return 0 if a % q == 0 else (1 if pow(a % q, (q - 1) // 2, q) == 1 else -1)
ok = [n3 == q * q - 7 * q + 19 + 18 * leg(-1, q) + 9 * leg(-2, q) + 6 * (1 + leg(-3, q)) + b for q, _, n3, b in rows]
ok2 = [n2 == q * q - 4 * q + 10 + 5 * leg(-1, q) for q, n2, _, _ in rows]
print('N3 closed form exact on %d/%d primes; N2 closed form exact on %d/%d' % (sum(ok), len(ok), sum(ok2), len(ok2)))
