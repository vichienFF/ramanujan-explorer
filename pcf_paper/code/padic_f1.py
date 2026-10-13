"""Track B: prime exponents in the gcd for F1 (exact) - find d_p(n) = v_p(gcd(P_n,Q_n))
compared with v_p(n!): e_p(n) = 2 v_p(n!) - d_p(n)  (p != 3)  and f_3(n) = d_3(n) - v_3(n!)"""
import json, math
from collections import Counter

A = lambda k: 4*k*k + 10*k - 3
B = lambda k: -k*k*(k+4)*(3*k-4)
N = 600
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def vp(x, p):
    if x == 0:
        return 10**9
    c = 0
    while x % p == 0:
        x //= p; c += 1
    return c


def vfact(n, p):
    return sum(n // p**k for k in range(1, 20))


P0, P1, Q0, Q1 = 1, A(0), 0, 1
rows = []
for n in range(1, N + 1):
    P0, P1 = P1, A(n)*P1 + B(n)*P0
    Q0, Q1 = Q1, A(n)*Q1 + B(n)*Q0
    rows.append({p: (min(vp(P1, p), vp(Q1, p)), vfact(n, p)) for p in PR})
out = {}
for p in PR:
    if p == 3:
        f = [r[p][0] - r[p][1] for r in rows]
        out[p] = {"f3=d-v(n!)": dict(Counter(f).most_common(8)), "min": min(f), "max": max(f), "first40": f[:40]}
    else:
        e = [2*r[p][1] - r[p][0] for r in rows]
        out[p] = {"e=2v(n!)-d": dict(Counter(e).most_common(8)), "min": min(e), "max": max(e), "first40": e[:40]}
json.dump(out, open("bf_runs/test_fr/padic_f1.json", "w"), indent=0)
for p in PR:
    k = [x for x in out[p] if x not in ("min", "max", "first40")][0]
    print(p, "range", out[p]["min"], "..", out[p]["max"], "| dist", out[p][k], "| n=1..40:", out[p]["first40"])
