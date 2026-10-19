# PLAN PP-V3 (FROZEN 2026-10-19, before the Kaggle run; smoke test q <= 64 seen and disclosed)
Smoke (q <= 64): V/((#good rho) E) = 7.7 (q=8), 9.0 (27), 13.1 (32), 18.7 (64), 6.1 (25), 4.2 (49), 8.1 (16); N(rho) = 0 mod 3 always.
Hypothesis V3-gen: the multiplier group of a Singer set with q = p^k is {p^j : j < 3k} (order 3k), triples come in multiplier
orbits, so V/((#good) E) = 3k (1 + o(1)) (prime q: 3k = 3, matching V3).
Test (q >= 121 in shards a,b: 121,125,128,169,243,256,289,343,361,512,529,625,729,841,961,1024,1331,1369):
PASS if |V/(#good E) / (3k) - 1| <= 0.10 for >= 80% of these q (allowing small-good-count noise), and N = 0 mod 3 always.
Shard c (2026-10-19, same frozen rule): q = 1681, 1849, 2048, 2187, 2197.
Shard d (2026-10-19, same frozen rule, extension): q = 2209, 2401, 2809, 3125.
