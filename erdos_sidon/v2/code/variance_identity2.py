"""V = sum over GOOD rho (rho, rho-1 units mod m) of (N(rho) - E)^2, E = mean over good rho; trend of V / q^3."""
import random, numpy as np, sys, math
sys.path.insert(0, '..')
from c3r_fast import singer_fast
import b22c_gaps as B
for q in [p for p in B.primes(5, 140)][::2]:
    S, m = singer_fast(q, random.Random(1000003 * q)); n = len(S); inS = np.zeros(m, bool); inS[S] = True
    base = np.zeros(m, np.int64)
    for a in S: base[(S - a) % m] = a
    d = np.arange(1, m); good = np.array([math.gcd(r, m) == 1 and math.gcd(r - 1, m) == 1 for r in range(m)])
    N = np.zeros(m)
    for rho in np.nonzero(good)[0]: N[rho] = inS[(base[d] + rho * d) % m].sum()
    Nr = N[good]; E = Nr.mean(); V = ((Nr - E) ** 2).sum()
    print(q, m, "good", int(good.sum()), "E", round(E, 2), "V/q^3", round(V / q**3, 3), "V/(#good*E)", round(V / (good.sum() * E), 3), flush=True)
