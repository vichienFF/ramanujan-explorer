"""Check: sum_{rho != 0,1} N(rho)^2 == sum_{lambda != 0} sum_mu (I_lambda(mu))_3 - corrections?  I_lambda(mu) = |S cap (lambda S + mu)|."""
import random, numpy as np, sys, math
sys.path.insert(0, '..')
from c3r_fast import singer_fast, ratio_counts, inv_table
for q in (5, 17, 41, 59):
    S, m = singer_fast(q, random.Random(1000003 * q)); n = len(S); inS = np.zeros(m, bool); inS[S] = True
    N = ratio_counts(S, m, inv_table(m)); lhs = int((N[2:].astype(np.int64) ** 2).sum())
    rhs = 0
    for lam in range(1, m):
        if math.gcd(lam, m) != 1: continue
        img = (lam * S) % m
        I = np.zeros(m, np.int64)
        for t in img: I[(S - t) % m] += 1       # I[mu] = #{(s,t): s = lam*t' + mu}
        rhs += int((I * (I - 1) * (I - 2)).sum())
    print(q, "sum N^2 =", lhs, " sum_{lam,mu} (I)_3 =", rhs, " diff", rhs - lhs, flush=True)
