# BSD pilot plan B1: quantitative laws linking BSD invariants and Frobenius traces (draft 2026-09-30, register before running)

## Background
Wachs (arXiv 2603.04604, 2026) found on 3.06M Cremona curves that curves grouped by |Sha| have significantly different
murmuration (a_p-average) profiles (p < 0.001), but gave no quantitative law. Heuristic link: for rank 0 the BSD formula
gives L(E,1) = Omega * |Sha| * prod(c_p) / |T|^2, and the Euler product gives log L(E,1) ~ sum_p a_p/p + (smaller terms),
so conditioning on the BSD side should shift a_p by an amount decreasing like 1/p.

## Data (to be approved separately)
Cremona ecdata (github.com/JohnCremona/ecdata, Artistic-2.0): allbsd + aplist blocks for conductor N < 500,000
(about 100 files, about 530 MB). Unit = isogeny class, curve number 1. a_p for good primes p < 100.
Discovery set: N < 250,000. Held-out validation set: 250,000 <= N < 500,000 (not opened until the model is frozen).

## Aim A (control): reproduce Wachs
Within rank 0 and rank 1 separately, group by |Sha| in {1, 4, >=9}; test equality of mean a_p vectors (p < 100) with a
permutation test (10,000 shuffles of Sha labels within conductor bins of width 25,000). Expected: p < 0.001.

## Aim B (primary, pre-registered hypothesis H1: "Euler-product law")
For rank-0 classes, regress a_p on y = log(L(E,1)) (column L^(r)(1)/r!) within conductor bins, pooled:
  a_p = alpha_p + beta_p * y + noise, for each good prime p < 100.
H1: the scaled slopes s_p = p * beta_p are constant in p (no trend).
Test on the HELD-OUT set: fit s_p = c0 + c1 * log(p) by weighted least squares over the 25 primes.
H1 is SUPPORTED if (i) c0 > 0 with 99% CI excluding 0, and (ii) |c1| < 0.25 * c0 (trend small relative to level).
H1 is REJECTED otherwise. (Discovery set is used only for code checks; the H1 test itself is run once on held-out.)

## Aim C (exploratory): AI-assisted model search
On the discovery set only, search formulas Delta_{r,s}(p) = E[a_p | rank r, |Sha| = s] - E[a_p | rank r, |Sha| = 1]
of the form kappa_r * f(s) * g(p) with f in {log s, sqrt s, s, 1/s}, g in {1/p, 1/sqrt p, log p / p, 1}, plus formulas
proposed by an LLM (Groq free tier; prompts contain only public quantities: invariant names, fitted numbers, no new data).
Select one model by BIC on discovery, freeze it (SHA-256 on GitHub), then evaluate once on held-out.
Success for C: held-out R^2 >= 0.5 of the Sha-dependent variance AND better than the Sha-independent null
(permutation p < 0.01).

## Reporting and safety
All three aims reported whatever the outcome. Local computation only (Kaggle only if a step exceeds 2 h).
No heavy work 07:10-07:40. Figures added to the Math Research Dashboard (local, port 8610).
Evidence labels: VERIFIED NUMERICALLY for statistical findings; no claim of proof.
