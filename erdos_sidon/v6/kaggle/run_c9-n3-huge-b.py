# H-N3-HUGE (registered PLAN_UNIFORM_A 11-03): N3 formula at all primes in [LO,HI). Pure numpy, no secrets, internet off.
# BENCH: local q=2003 0.3 s/prime, q^2 scaling -> est < 6 h per kernel; time guard 10.5 h.
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

LO, HI = 13000, 20000

import sys, time, json
def chi(a, p): return 1 if pow(a % p, (p-1)//2, p) == 1 else -1
print("CONTROL REF:", "PASS" if ctl else "FAIL", flush=True); assert ctl
fails = []; n = 0; t0 = time.time(); q = LO
for q in range(LO, HI):
    if any(q % d == 0 for d in range(2, int(q**.5)+1)): continue
    if time.time() - t0 > 10.5*3600: print("TIME GUARD at", q); break
    N3 = Ns(q)[3]; pred = q*q - 7*q + 19 + 18*chi(-1, q) + 9*chi(-2, q) + 6*(1 + chi(-3, q)) + bq(q); n += 1
    if N3 != pred: fails.append(q)
res = dict(lo=LO, hi=HI, tested=n, fails=fails, last_q=q, sec=round(time.time()-t0))
json.dump(res, open("/kaggle/working/n3_huge.json", "w")); print(res)
