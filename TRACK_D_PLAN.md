# Track D plan: LLM-guided evolutionary search for PCF families (draft 2026-09-30, to be registered before any run)

## Question
Can an LLM that writes *generator programs* (FunSearch / AlphaEvolve style: propose -> evaluate -> feed back -> iterate)
find polynomial continued fractions (PCFs) with full factorial reduction (FR) outside known families more efficiently
than (a) a random generator and (b) plain brute force, under the same candidate budget?

## Design
- LLM: gpt-oss-120b via Groq free tier (no paid usage). Temperature 1.0. 2 independent seeds.
- The LLM writes a Python function `generate(rng) -> list[(a_coeffs, b_coeffs)]` returning <= 200 PCFs,
  a(n) degree <= 2, b(n) degree <= 4, integer coefficients |c| <= 200.
  Programs run in our existing AST-whitelisted sandbox (sandbox.py) with a 20 s timeout. No file/network access.
- One iteration = 1 LLM call -> 1 program -> <= 200 candidates. Pilot: 50 iterations per seed (10,000 candidates per seed).
- Feedback to the LLM: ONLY aggregate numbers of its own program (how many candidates converged / passed FR /
  were duplicates / fell in the Conjecture 1.3 family) and its best-scoring previous programs (code only).
  Never any PCF formula, limit value or our unpublished lists.

## Evaluation of each candidate (local, deterministic)
1. convergence (depth 300 vs 600, float) ; 2. FR proxy (p^2 divides P_240 and Q_240 for >= 3 of p in {127,131,137,139});
3. exact S_N test |S_800 - S_200| < 0.15 ; 4. not in Ben David et al. Conj. 1.3 (index shifts -2..2);
5. limit not rational/quadratic, not Mobius (coeff <= 10^5) of our 36 constants ;
6. deduplicate by Mobius relation (PSLQ [1,x,y,xy], coeff <= 10^4) against everything found so far in that arm.
Score of a program = number of NEW clusters passing 1-6. Final top clusters additionally get: Euler-type test
(hypergeometric solution, ore_algebra), operator factorization, Cohen 2024/2026 and euler2ai comparison.

## Baselines (same budget: 10,000 candidates per seed)
- B1 random: uniform random a, b in the same coefficient box.
- B2 brute force: uniform sample from the Track A space (factored b, 1 <= k <= 6, |t| <= 10).

## Pre-registered criteria (primary)
Track D "succeeds" if, summed over the 2 seeds, the LLM arm finds
 (i) at least 2x as many new FR clusters (passing 1-6) as B1, AND
 (ii) at least 1 cluster NOT reachable by the Track A space (b not a product of 4 linear factors with k <= 6, |t| <= 10).
Secondary: number of clusters whose operator is irreducible of order 4; cost per cluster (LLM calls).
A negative result is reported in full.

## Safety and rules
- Prompts contain only the generic task and aggregate scores; keys from environment/D:\Secrets, never printed.
- Stops on Groq rate limits (waits; never pays). No heavy work 07:10-07:40. Local only (Kaggle not needed).
- All outputs stored under bf_runs/track_d/ ; any hit is timestamped (SHA-256 on GitHub) before disclosure.
- Separate from trading bots, FlyBrain simulator and phase2d.

## Timeline
Day 1: code + unit tests on known cases (positive control: the generator "Track A space" must reproduce known hits).
Day 2-3: pilot run (2 seeds x 3 arms). Day 4: analysis and report.
