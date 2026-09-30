# BSD pilot B1 - amendment 1 (2026-09-30), written BEFORE the held-out set (250k <= N < 500k) was opened

Aim A (control, discovery set N < 250,000, 10,000 permutations):
 rank 0: n = 179,670 / 15,611 / 9,286 (|Sha| = 1 / 4 / >=9), p = 0.0001 -> Wachs effect reproduced.
 rank 1: n = 259,714 / 597 / 45, p = 0.0158 -> above the pre-registered 0.001 threshold (very small Sha>1 groups).

Code check of Aim B on the discovery set: s_p = p*beta_p grows roughly linearly in p (1.4 at p=2 ... 79 at p=97),
i.e. beta_p is roughly constant (about 0.7-1.2), not proportional to 1/p.
Reason (our error in the plan's heuristic): Cov(a_p, sum_q a_q/q) ~ Var(a_p)/p and Var(a_p) ~ p (Sato-Tate),
so the Euler-product heuristic predicts beta_p ~ constant, not ~1/p.

Decision:
- H1 stays exactly as registered and will be tested ONCE on the held-out set and reported (expected: REJECTED).
- New hypothesis H2 (corrected heuristic), registered now, tested once on the same held-out run:
  H2: beta_p is constant in p. Fit beta_p = d0 + d1 * log(p) by WLS over the 25 good primes p < 100
  (same estimator and SE inflation as H1). H2 SUPPORTED iff d0 > 0 with 99% CI excluding 0 AND |d1| < 0.25 * d0.
- Nothing else in BSD_PILOT_PLAN.md changes.
