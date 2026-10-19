# PLAN Batch 28 (FROZEN before any computation at these q) - 2026-10-16
Question: do dilated Singer sets' factorial-moment deficits follow the first-order "forbidden structure" model
  R_k ~ -[ C(k,3) P3(l) + C(k,4) P4(l) ]  (3-APs and nontrivial parallelograms are impossible in a Sidon / 3-AP-free set; ck_pred.py)
  asymptotically q R_k ~ -[(3/2)C(k,3) + 2C(k,4)]/C: C=2 -> k=3..6: -0.75, -4, -12.5, -30.
Prior (already SEEN, q <= 601, Batch 25 pooled c_k at C=2): -0.61, -3.21, -9.58, -20.6 (ratios 0.81, 0.80, 0.77, 0.69).
Data (BLIND for k >= 4): Singer sets (b22c_gaps.singer_set, seed 1000003 q), every 2nd prime q in [607, 1499], C = 2, NT = 1000
random unit classes (seed 5 q), all shifts; null = random (q+1)-subsets (seed 91 q + 1) at every 8th listed q. Estimator =
b25m_moments.moments (b28_moments.py is a verified-identical fast version).
Tests (inverse-variance pooled ratio rho_k = sum w q R_k / sum w q pred_k, w = 1/(q se)^2):
- T1 positive control k=3: rho_3 in [0.75, 1.05] (Lane B: 0.94-0.98 at larger q; Batch 25: 0.81).
- T2 main, k = 4, 5, 6 separately: PASS if rho_k in [0.80, 1.20] with its 95% CI overlapping 1 or inside [0.8, 1.2].
- T3 descriptive: rho_k on upper vs lower half of q (finite-size trend toward 1?).
- N null control: pooled q R_k of null sets within 3 se of 0 for every k, else VOID.
Interpretation fixed in advance: T2 PASS -> c_k model (k^4 growth) supported as the leading term; T2 FAIL with rho < 0.8 for all
k -> the first-order model misses a positive term (report; next = second-order inclusion-exclusion / redistribution).
AMENDMENT (2026-10-16, before any Batch 28 computation): Singer sets built with singer_fast (c3r_fast.py; identical set to b22c_gaps.singer_set, m instead of q^3 steps) - checked equal at q=101,131.
AMENDMENT 2 (before any computation): NT = 3000 (timing 0.2 s/unit at q=1493 allows 3x more units -> smaller se).
