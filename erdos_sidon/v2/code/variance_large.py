"""V/(#rho*E) at larger q using O(n^3) ratio counts (c3r_fast.ratio_counts); only m prime (all rho good)."""
import random, numpy as np, sys, time
sys.path.insert(0, '..')
from c3r_fast import singer_fast, ratio_counts, inv_table
import b22c_gaps as B
def isprime(x): return x > 1 and all(x % d for d in range(2, int(x**0.5) + 1))
for q in [p for p in B.primes(int(sys.argv[1]), int(sys.argv[2])) if isprime(p*p + p + 1)]:
    t0 = time.time(); S, m = singer_fast(q, random.Random(1000003 * q)); n = len(S)
    N = ratio_counts(S, m, inv_table(m)).astype(float); Nr = N[2:]; E = n*(n-1)*(n-2)/(m-2)
    V = ((Nr - E)**2).sum(); mod3 = float((Nr % 3 == 0).mean())
    print(q, "V/(#E)", round(V/((m-2)*E), 4), "frac N%3==0", round(mod3, 4), f"{time.time()-t0:.0f}s", flush=True)
