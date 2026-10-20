# PLAN PP-V3 (FROZEN 2026-10-19, before the Kaggle run; smoke test q <= 64 seen and disclosed)
Smoke (q <= 64): V/((#good rho) E) = 7.7 (q=8), 9.0 (27), 13.1 (32), 18.7 (64), 6.1 (25), 4.2 (49), 8.1 (16); N(rho) = 0 mod 3 always.
Hypothesis V3-gen: the multiplier group of a Singer set with q = p^k is {p^j : j < 3k} (order 3k), triples come in multiplier
orbits, so V/((#good) E) = 3k (1 + o(1)) (prime q: 3k = 3, matching V3).
Test (q >= 121 in shards a,b: 121,125,128,169,243,256,289,343,361,512,529,625,729,841,961,1024,1331,1369):
PASS if |V/(#good E) / (3k) - 1| <= 0.10 for >= 80% of these q (allowing small-good-count noise), and N = 0 mod 3 always.
Shard c (2026-10-19, same frozen rule): q = 1681, 1849, 2048, 2187, 2197.
Shard d (2026-10-19, same frozen rule, extension): q = 2209, 2401, 2809, 3125.

## Amendment 2026-10-19 (before running): shard e = q 4913 (17^3, k=3). Purpose: does the k=3 excess (5-18% high) shrink at larger q? Same statistic and pass band as shards a-d. Prediction (registered): ratio/3k in [0.97,1.10]; if <=1.03 the k=3 drift is a small-q effect.

## Amendment 2026-10-19 (before running) rama-lambda-bulk3: q in [1000,1100] with m prime, NL=500. Frozen prediction: bulk sd/(sqrt(18) q) in [0.93,1.07]; kurtosis in [2.7,3.3]; n_dual_forbidden = 9 for every q.

## Amendment 2026-10-19 (before running): shard f = q 6859 (19^3, k=3). Frozen prediction from the q^{-1/2} reading: ratio/3k in [1.012,1.060] (excess*sqrt(q) in [1,5]); outside -> the decay reading is rejected.

## Amendment 2026-10-20 (before running): shard g = q 3481 (59^2), 3721 (61^2), 4489 (67^2) [k=2]; shard h = q 6561 (3^8, k=8, predicted ratio 3k = 24). Same statistic and registered band ratio/3k in [0.97,1.10]. Shard h is the first k=8 test of the "order of the multiplier group" law.

## Amendment 2026-10-20 (before running): shards i = q 1024 (2^10, k=10), 2048 (2^11, k=11); j = q 4096 (2^12, k=12), 729 (3^6, k=6). Large-k test of the 3k law (predicted ratio 30, 33, 36, 18). Registered band ratio/3k in [0.97,1.10] for q >= 121. Local smoke (p=2): q=16 0.68, 32 0.87, 64 1.04 (small q, outside band by design).

## Amendment 2026-10-20 (before running): shard k = q 2187 (3^7, k=7); shard l = q 8192 (2^13, k=13). Same band [0.97,1.10].

## Amendment 2026-10-20 (before running): shard m = q 128 (2^7), 256 (2^8), 512 (2^9): completes k=7..13 ladder for p=2. Band [0.97,1.10].

## HYPOTHESIS H-CUBE (REGISTERED 2026-10-20, BEFORE shards h=6561 and l=8192 finish)
Observation (33 prime powers q>=121): every perfect cube q (125, 343, 512, 729, 1331, 2197, 4096, 4913, 6859) has ratio/3k
in [1.022, 1.180] (all > 1.02); every non-cube q >= 625 (625, 841, 961, 1024, 1369, 1681, 1849, 2048, 2187, 2209, 2401, 2809,
3125, 3481, 3721, 4489) has ratio/3k in [0.996, 1.007]. Small non-cubes (121-529) scatter 0.96-1.09 (small-q noise).
H-CUBE: the "k=3 excess" is a CUBE effect: the variance law sum(N-E)^2 = 3k sum E holds for non-cube q, and has an extra
positive term when q is a perfect cube.
Frozen predictions: shard h q=6561 (3^8, non-cube) ratio/3k in [0.98, 1.02]; shard l q=8192 (2^13, non-cube) in [0.98, 1.02].
Next registered test (to build): cube q with k>3 not yet run, e.g. q = 2^15 = 32768 (too big) -> use q = 5^6 = 15625 only if timing allows.

## H-CUBE refined (REGISTERED 2026-10-20): "q a perfect cube" == "3 | k". Sharper conjecture V3':
sum(N-E)^2 / sum E = 3k + [3 | k]   (one extra unit exactly when 3 divides k).
Fit to existing data: k=9 (512) 28/27=1.037 vs 1.039; k=12 (4096) 37/36=1.028 vs 1.022; k=6 (729) 19/18=1.056 vs 1.042;
k=3 10/9=1.111 vs 1.038..1.180 (mean ~1.08, noisy at small q).
Test kernel rama-pp-v3-n: several independent Singer sets (different primitive polynomials, SEEDS) per q for
q in {343, 512, 729, 1331, 2197} (3|k) and controls {625, 1024, 2187} (3 does not divide k). Frozen predictions:
pooled mean of ratio/(3k) over seeds is within 2 se of (3k+1)/3k for 3|k, and within 2 se of 1 for the controls.
AMENDMENT 2026-10-20 (before pushing): rama-pp-v3-n DROPPED - local smoke shows identical ratio for different seeds (q=27: 0.997/0.997, q=64: 1.036/1.036): all Singer sets of a given q are multiplier-equivalent, so seeds give no new information. V3' can only be tested with new q having 3|k (next feasible: none under the 12 h limit; 23^3 est. ~13.6 h).

## Amendment 2026-10-20 (before running): rama-lambda-bulk4 = q 743, 761 (m prime), NL=500, checkpoint per q (jsonl append). Replaces failed bulk3 (q~1100 exceeded 12 h). Frozen prediction: bulk sd/(sqrt(18) q) in [0.93,1.07]; kurtosis [2.7,3.3]; n_dual_forbidden = 9.
Amendment 2026-10-20: rama-lambda-bulk5 = q 773, 827 (same prediction as bulk4).

## C9-ORB (REGISTERED 2026-10-20, before running): orbit-count histograms. Kernels rama-pp-hist-a (q 512,729,1024,2187,1331,2401) and -b (3125,4096,4913) save M = N/3k histograms. Frozen predictions: (O1) N = 0 mod 3k for every good rho at every q; (O2) for 3 not dividing k, Var M / E M in [0.97,1.03]; for 3 | k, in [1.02,1.12] (overdispersed). Exploratory: shape of the excess (heavy tail vs. mixture).
C9-ORB addendum (before running): rama-pp-hist-c = prime q 1031, 1499, 2003 (k=1). Prediction O1 + Var M/E M in [0.97,1.03].

## C9-ORB-P (registered 2026-10-20, before pp-hist-d/e run)
Local small-q probe (VERIFIED, scratch): cube Var M/E M: q125(p≡2) 1.10, q343(p≡1) 1.18, q1331(p≡2) 1.053, q512 1.039, q729 1.042, q64 1.036.
Non-cube small q noisy (q169 1.089, q289 1.053) -> small-q results NOT used for decisions.
Hypothesis H-P: excess larger when p ≡ 1 mod 3 (cube roots of unity in F_p).
Prediction: q=2197 (13^3) and q=6859 (19^3): Var M/E M >= 1.08 (supports H-P); if both in [1.02,1.07] -> H-P rejected.

## C9-ORB-N (registered 2026-10-20, before pp-nb-a/b run) — numba kernel validated locally (q 27/64/125 reproduce 0.9974/1.0361/1.1013 exactly)
- pp-nb-a q=12167 (23^3, p≡2 mod 3): O1 all_div_3k TRUE; AN1b finite-size hypothesis predicts excess (VoverE-1) < 0.038 (4913 value); if >= 0.038 -> AN1b (shrinking) rejected.
- pp-nb-b q=14641 (11^4, k=4 non-cube): O1 TRUE; VoverE in [0.97,1.03].

## C9-RES (registered 2026-10-20 BEFORE pp-hist-e (q=6859) and pp-nb-a (q=12167) results) — "resonant ratio orbit" law
Local finding (VERIFIED, scratch probe3/probe4): for cube q = r^3 (k=3) the overdispersion is carried by ONE S3-orbit of 6 ratios
with M ≈ r·mu (q=125: 64 vs 13.0; q=343: 177 vs 24.6; q=1331: 1628 vs 147.8). These 6 ratios explain 84-94% of (Var/E - 1).
Law: excess := Var M/E M - 1 ≈ 6 (r-1)^2 mu / n_good, mu = (q+1)q(q-1) P(m) / (3k n_good), P(m) = prod_{l|m} (l-1)(l-2)/l^2,
n_good = prod l^{e-1}(l-2). Retro-check: 1331 pred .0500 obs .0534; 2197 pred .0873 obs .0877; 4913 pred .0368 obs .0377.
PREDICTIONS (PASS if observed excess within ±15% of pred):
- q=6859 (19^3): excess_pred = 0.0631 (Var/E ≈ 1.063). NOTE this implies the earlier H-P test (>=1.08) will FAIL: the apparent p≡1 mod 3 effect = n_good normalisation (3 | m), not a new symmetry.
- q=12167 (23^3): excess_pred = 0.0281 (Var/E ≈ 1.028); also consistent with AN1b (< 0.038).
- Consequence (INFERENCE): excess -> 0 like ~2(r-1)^2/(3k q) ~ q^{-1/3}: H-CUBE is a single-orbit finite-size effect, not a breakdown of the Poisson law in the limit.
Next question: prove that the resonant orbit has M = r·mu exactly-ish (subline PG(1,r) ⊂ PG(1,r^3) geometry?), and identify the extra orbits for k=6,9 (only partial share: 729 .032/.042, 512 .021/.039).

## C9-CUBIC (registered 2026-10-20 before pp-nb-c / pp-nb-d run; kernels output top-12 rho + cubic-root flags; validated locally q=125 exact)
- pp-nb-c q=4913, 6859 (k=3): PREDICT the 6 largest-M ratios are exactly the 3 roots of x^3-3x+1 and the 3 roots of x^3-3x^2+1 mod m, with M/mu in [0.8r, 1.2r] (r=17, 19). FAIL if any top-6 is not a cubic root.
- pp-nb-d q=729 (k=6), 4096 (k=12): EXPLORATORY (local q=64 shows a different orbit above the cubic one for k=6) — record which top orbits are cubic roots; no pass/fail.
## C9-RES-2 (registered 2026-10-20 before pp-nb-e run): q=24389 (29^3, m = 41203·14437)
PREDICT: excess = 0.0214 ±15%; mu = 2709.5 ±1%; top-6 = cubic roots (x^3-3x+1, x^3-3x^2+1); top-6 M ≈ r·mu ≈ 78,576 (±2%); exact-count conjecture N(rho0) ≈ r(q+1)·(unit fraction) -> M ≈ 78,59x.
## pp-nb-f (registered 2026-10-20): q=19683 = 3^9 (k=9, p=3) — EXPLORATORY: p=3 makes x^3-3x+1 ≡ (x+1)^3 degenerate; record top orbits; O1 all_div_3k must be TRUE (Lemma O1 is proved for all p).
## pp-nb-g (registered 2026-10-20): q=15625 = 5^6 = 25^3 (k=6, r=25). PREDICT: the cubic-root orbit (x^3-3x+1 / reversal) appears among top-12 with M/mu in [0.8r,1.2r] = [20,30]. Other k=6 orbits: exploratory.
## Orbit-reduced re-runs (2026-10-20, user approved delete of pp-nb-a/b/e/f): rama-pp-nbo-a (12167, C9-RES pred .0281), -b (14641 control [0.97,1.03]), -f (19683 exploratory p=3), -g (15625 k=6: cubic orbit M/mu in [20,30]). Predictions unchanged from earlier registrations. q=24389 (C9-RES-2) POSTPONED: est. 20 h even with orbit reduction.
## READY controls: rama-pp-nbo-h q=16384 (2^14, k=14 non-cube), rama-pp-nbo-i q=16807 (7^5, k=5 non-cube): PREDICT Var/E in [0.97,1.03]; top orbits exploratory (expected small resonances f=p^{gcd(a,k)}). Est. runtime 1.3 h / 4 h.
## Registered 2026-10-20 (orbit algorithm; runtime calibrated on nbo-b: c = 2.06e-8 s per n^3/(3k) unit)
- rama-pp-nbo-j q=32768 = 2^15 = 32^3 (k=15, est 4.5 h): PREDICT the top-6 orbit = cubic roots, with M/mu in [0.8r, 1.2r] = [25.6, 38.4]; O1 TRUE. Excess formula pred 0.004 (informational only; the sampling noise is comparable).
- rama-pp-nbo-e2 q=24389 = 29^3 (est 9.2 h, < 10 h rule): C9-RES-2 as registered (excess 0.0214 ±15%, mu 2709.5 ±1%, top-6 cubic, M ≈ r·mu ±2%).
