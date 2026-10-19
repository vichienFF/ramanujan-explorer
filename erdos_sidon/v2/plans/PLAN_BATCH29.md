# PLAN Batch 29 (FROZEN before computation) - 2026-10-16
Replication + extension of Batch 28 (PASS): same forbidden-structure model R_k ~ -[C(k,3)P3(l) + C(k,4)P4(l)], now
(i) window C = 4 (l = 4q) and C = 2, (ii) k = 3..8 (k = 7, 8 never tested: the model predicts NO new 5+-point forbidden structures),
(iii) the OTHER half of the primes in [607, 1499] (primes[1::2]; never computed for any k).
NT = 3000 unit classes (seed 5q), Singer via singer_fast (seed 1000003 q), null random sets at every 8th q (seed 91q+1).
Tests (inverse-variance pooled rho_k = measured/predicted, per C):
- R1: for C = 2 and C = 4, k = 3..6: rho_k CI overlaps [0.8, 1.2] and point estimate in [0.8, 1.2] -> replication PASS.
- R2 (new): k = 7, 8: same rule -> "no new forbidden structures up to 8 points" supported; FAIL with rho < 0.8 -> a missing
  positive term at high k (report); rho > 1.2 -> missing negative term.
- Null: pooled q R_k within 3 se of 0, else VOID.
