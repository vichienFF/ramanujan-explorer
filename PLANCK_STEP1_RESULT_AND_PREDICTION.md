# Planck step 1 result + frozen prediction for step 2 (register BEFORE T4 results are pulled) - 2026-10-06

Amendment a3b8d95, plan e551c1d. Data: rank-1 beta_p (Cremona, N < 500k), fit on even 50k bins, scored on odd bins.

## Step 1 results (weighted held-out error; lower is better)
| model | constants | held-out error |
|---|---|---|
| (a) first-order AFE baseline y = A E1(x) | A = 1.228 | 9.73 |
| (b) y = A [E1(x) - lam e^-x] | A = -2.77, lam = 4.28 | 5.90 |
| (c) PySR, <= 2 constants (WINNER) | see below | 0.53 |

Winner: p * beta_p = log p * ( c1 - (log p)^2 * log(x + c2) ),  x = 2 pi p / sqrt(N),  c1 = 3.992227, c2 = 0.6897002.

Controls (same pipeline): rank 0 -> PySR p*beta = exp(log p - 0.153 x) - 0.480/log p (no sign change in the data range);
shuffled rank 1 -> PySR returns a constant (-0.008), AFE amplitude A = -0.002. Both controls behave as required.

## Disclosure of an error in the registered baseline
The plan wrote the first-order AFE prediction as beta_p ~ A W(x)/p. Since Var(a_p) ~ p, linear response gives
Cov(a_p, log L) ~ W(x), i.e. beta_p ~ A W(x) (no 1/p). Baseline (a) as registered is therefore mis-specified and its
large error is partly an artefact. Step 2 will ALSO report the corrected baseline beta_p = A W_1(x) (fitted on the same
even bins) so that the comparison is fair. The winner selection above is unchanged (it follows the registered rule).

## Frozen prediction for step 2 (T4 height-ordered family, N in [1e6, 1e7), kernel sukjitvi/rama-k4-t4-height)
Sign change where (log p)^2 log(2 pi p / sqrt(N) + 0.6897002) = 3.992227. Predicted p* (kappa = p*/sqrt(N)):
N = 1e6: 85.1 (0.085) | 2e6: 113.7 (0.080) | 4e6: 153.1 (0.077) | 7e6: 195.6 (0.074) | 1e7: 229.0 (0.072).
Alternative hypothesis to beat: constant kappa = 0.100 (median of Cremona bins).
Registered success rule (from a3b8d95): predicted p* within 20% of observed in >= 70% of N-bins, and RMS error of p*beta_p
below that of the first-order AFE baseline. Additional (reported, not decisive): which of {formula, constant 0.100} is
closer to the observed kappa in more N-bins. T4 N-bins: 10 log-spaced bins in [1e6, 1e7), log N partialled out within bin.
