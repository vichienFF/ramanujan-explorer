# Step (b): N(rho) for Singer sets ~ F_q-points of the universal curve
#   C_{u,v}: s^{u-v} r^v = t^u,  (s-1)^{u-v} (r-1)^v = (t-1)^u   (rho = u/v), diagonal s=r=t removed.
# Counts split-model points over F_p (s,r,t not in {0,1}); prints (count - p)/sqrt(p).
import sys, numpy as np
from math import gcd, sqrt
def pw(x, e, p):  # vectorised x^e mod p, e may be negative (x nonzero)
    if e < 0: x = np.array([pow(int(a), p-2, p) for a in x], dtype=np.int64); e = -e
    r = np.ones_like(x); b = x.copy()
    while e:
        if e & 1: r = r*b % p
        b = b*b % p; e >>= 1
    return r
def count(u, v, p):
    x = np.arange(2, p, dtype=np.int64)          # exclude 0,1
    tk = pw(x, u, p)*p + pw(x-1, u, p)            # key of t
    tab = np.bincount(tk, minlength=p*p)
    A = pw(x, u-v, p); B = pw(x-1, u-v, p); C = pw(x, v, p); D = pw(x-1, v, p)
    tot = 0
    for i in range(len(x)):                       # s = x[i], r = all x
        key = (A[i]*C % p)*p + (B[i]*D % p)
        tot += int(tab[key].sum())
    # remove diagonal s=r=t (always a solution)
    return tot - len(x)
if __name__ == "__main__":
    ratios = sorted({(u//gcd(u,v), v//gcd(u,v)) for u in range(-6,7) for v in range(1,7) if u != 0 and u != v})
    primes = [int(a) for a in sys.argv[1:]] or [211, 503, 1009]
    for (u, v) in ratios:
        row = [(count(u, v, p) - p)/sqrt(p) for p in primes]
        print(f"rho={u}/{v}", " ".join(f"{z:8.2f}" for z in row), flush=True)
