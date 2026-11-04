# H-CH3-N3-BIG (registered PLAN_UNIFORM_A 11-04): N1..N3 over GF(p^n) by pure numpy. Private, internet off, no secrets. BENCH: est 3^10 ~0.6 h + 5^7 ~1.1 h; < 10 h.
"""Pure-numpy N1,N2,N3 counter over GF(p^n) (no Sage; runs on Kaggle).  # LOCAL-OK: q <= 59049 in minutes (benchmark printed)
N_k = sum_{c,d in F*} (r)_k, r = #{y in F: c y^4 + d (1-y)^4 = 1}. Field: log/antilog tables from a primitive polynomial (sympy galoistools),
elements encoded as base-p integers; addition digit-wise, multiplication via logs.
Usage: python gf_ncount.py p^n [p^n ...]
CONTROL: Sage values (p4_ch3_counts / p4_n3_pp outputs): q=9 -> (65, 60, 36); q=49 N3=2022; q=125 N3=14778; prime q=7 -> (37, 26, 6).
"""
import sys, time, numpy as np
from sympy.polys.galoistools import gf_irreducible_p, gf_pow_mod
from sympy.polys.domains import ZZ
from sympy import factorint
def primitive_poly(p, n):
    N = p**n - 1; fac = list(factorint(N))
    for t in range(p**n):
        c = [(t // p**i) % p for i in range(n)]; P = [1] + c[::-1]
        if c[0] == 0 or not gf_irreducible_p(P, p, ZZ): continue
        if n == 1 or all(gf_pow_mod([1, 0], N // r, P, p, ZZ) != [1] for r in fac): return c
def field(p, n):
    q = p**n; W = p ** np.arange(n)
    if n == 1:
        g = next(g for g in range(2, p) if all(pow(g, (p-1)//r, p) != 1 for r in factorint(p-1))) if p > 2 else 1
        exp = np.array([pow(g, i, p) for i in range(q-1)], np.int64)
    else:
        c = primitive_poly(p, n); exp = np.zeros(q-1, np.int64); v = [1] + [0]*(n-1)
        for i in range(q-1):
            exp[i] = sum(d * p**k for k, d in enumerate(v))
            top = v[-1]; v = [0] + v[:-1]
            v = [(v[k] - top * c[k]) % p for k in range(n)]
    log = np.full(q, -1, np.int64); log[exp] = np.arange(q-1)
    DIG = (np.arange(q)[:, None] // W) % p
    add = lambda a, b: ((DIG[a] + DIG[b]) % p) @ W
    neg = lambda a: ((-DIG[a]) % p) @ W
    def mul(a, b):
        r = exp[(log[a] + log[b]) % (q-1)]; return np.where((a == 0) | (b == 0), 0, r)
    def inv(a): return exp[(-log[a]) % (q-1)]
    def pw(a, k): return np.where(a == 0, 0, exp[(k * log[a]) % (q-1)])
    one = int(exp[0]); assert one == 1
    return q, add, neg, mul, inv, pw
def Ns(p, n):
    q, add, neg, mul, inv, pw = field(p, n); Y = np.arange(q); Y = Y[Y != 1]
    oneY = add(np.ones_like(Y), neg(Y)); Y4 = pw(Y, 4); D4 = inv(pw(oneY, 4)); N = [0, 0, 0]
    for c in range(1, q):
        d = mul(add(np.ones_like(Y), neg(mul(np.full_like(Y, c), Y4))), D4)
        cnt = np.bincount(d, minlength=q).astype(np.int64)[1:]
        if c == 1: cnt += 1
        N[0] += int(cnt.sum()); N[1] += int((cnt*(cnt-1)).sum()); N[2] += int((cnt*(cnt-1)*(cnt-2)).sum())
    return tuple(N)

ARGS = ['11^5']

import json, time
t0 = time.time()
ctl = Ns(3, 2) == (65, 60, 36) and Ns(7, 1) == (37, 26, 6) and Ns(7, 2)[2] == 2022 and Ns(5, 3)[2] == 14778
print("CONTROL:", "PASS" if ctl else "FAIL", flush=True); assert ctl
res = {}
for a in ARGS:
    p, n = map(int, a.split("^")); t1 = time.time(); N = Ns(p, n); res[a] = [N, round(time.time()-t1)]
    print(a, N, flush=True); json.dump(res, open("/kaggle/working/gf_ncount.json", "w"))
