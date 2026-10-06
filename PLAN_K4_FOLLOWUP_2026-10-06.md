# K4 follow-up plan (register before running) - 2026-10-06

## Observation being tested (from K4, exploratory, Cremona N < 500,000)
beta_p = within-bin slope of a_p on log L^(r)(E,1). Rank 1: beta_p changes sign at p* ~ 0.09-0.12 sqrt(N) in all 10 bins,
then stays clearly negative (about -1 to -1.7). Rank 0: beta_p > 0 for all p < 500 when N >= 100k.

## Literature check (done 2026-10-06, 5-rule protocol)
- Murmurations (He-Lee-Oliver-Pozdnyakov 2204.10140; Zubrilina; Cowan 2408.12723, 2504.09944; Sutherland): mean a_p by
  rank / root number, scale p ~ N. Different statistic (not correlation with the size of L), different scale.
- Wachs 2603.22807: rank 0 only, N < 100k; Cov(a_p, Omega | L(E,1)=c) ~ C(c)/sqrt(p), sign change in c, not in p.
- Wachs 2603.04604: Sha-stratified mean a_p, crossover near p ~ 200, rank 0 only; rank 1 explicitly left open (Sec. 9).
- Twisted first moments (classical): sum_f w_f lambda_f(p) L(1/2,f) has main term ~ p^(-1/2) V(p/sqrt(N)) > 0.
Not found: per-prime correlation of a_p with L'(E,1) for rank 1 with a sign change at p ~ c sqrt(N).
Not searched: MathSciNet/zbMATH (no access). Evidence level of novelty: weak (absence in searched sources only).

## Theory prediction (step 2, computed before any new data analysis)
First-order approximate functional equation: L(E,1) = 2 sum a_n/n e^(-x_n), L'(E,1) = 2 sum a_n/n E1(x_n), x_n = 2 pi n / sqrt(N).
Linear response: Cov(a_p, L^(r)) proportional to (1/p) Var(a_p) W_r(2 pi p/sqrt(N)), W_0 = e^(-x), W_1 = E1(x).
Both weights are POSITIVE for all x; they fall to half at p ~ 0.11 sqrt(N) (W_0) and p ~ 0.09 sqrt(N) (W_1).
=> First-order theory explains the sqrt(N) SCALE and the decay, but predicts NO sign change for either rank.
The observed strongly negative rank-1 beta for p > 0.1 sqrt(N) is therefore unexplained at first order.

## Tests (step 3)
T1 Confound control (Cremona data, already computed ap500.npz): add log N as a covariate within each 25k bin, and repeat
   with 5k bins. Rationale: mean a_p depends on p/N (murmurations) and log L' depends on N.
   Prediction P1: rank-1 sign change persists, p*/sqrt(N_mid) stays in [0.07, 0.15] in >= 8 of 10 bins.
T2 Shuffle control: permute log L within (rank, 5k-bin), 20 permutations. Prediction P2: no bin has a consistent sign
   change; |beta_p| <= 3 SE for >= 95% of (bin, p).
T3 Mechanism decomposition (Cremona allbsd columns): regress a_p separately on log Omega, log Reg (rank 1), log prod c_p,
   log Sha, -2 log #tors. Report which component carries the negative part for p > 0.1 sqrt(N). No pass/fail (exploratory).
T4 Independent family (Kaggle, PARI): random Weierstrass curves ordered by naive height (not by conductor), conductor
   1e6-1e7, analytic rank 0/1 and L^(r)(E,1) by PARI (ellanalyticrank), about 100k curves, a_p for p < 1000.
   Prediction P4: rank-1 p*/sqrt(N) in [0.07, 0.15] (median over N-bins); rank 0 no sign change below 0.3 sqrt(N).
Positive control (all tests): the small-p positive beta (p <= 7) must be reproduced (beta_5 > 0 in every bin).

## Decision
"Rank-1 sign change at ~0.1 sqrt(N) is real and not a conductor artefact" = SUPPORTED iff P1 and P2 and P4 hold.
If P1 fails: the effect is a murmuration/conductor artefact -> report as such.
Any outcome is reported. T1-T3 run locally (no upload); T4 on Kaggle (private, no secrets, internet only for pip if needed).
