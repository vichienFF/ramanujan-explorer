# Large gaps in dilates of Bose / Singer sets and the excess h(N) - sqrt(N) (Guy C9; related to Erdos problem #30)

Note on the problem: Guy C9 / Erdos (USD 500) asks whether h(N) = sqrt(N) + O(1). erdosproblems.com #30 (USD 1000) asks the weaker
question h(N) = sqrt(N) + O(N^eps). The evidence here concerns the O(1) question only. Section-3 material (Singer moments, 2026-10-15)
is in the subfolder addendum_2026-10-15/.

Vichien Fugsukjit, Independent researcher, Bangkok (9chienvi9@gmail.com). Numerical evidence, NOT a proof.
All experiments were pre-registered in this repository before they were run (plans/ and the repository root).

## What is here
- `code/b22c_gaps.py` - Bose sets (q prime) and Singer sets; for every multiplier t (one per class {+-t, +-tq}) the largest
  cyclic gap of tA; G*(q), the excess of the best cut, null model (random subsets). `b23a_gaps.py` = same with configurable ranges.
- `code/b22c_analyze.py` - registered bounded-vs-log test on q <= 2003.
- `code/b23b_branch.py` - counts of 3-term relations e1 L1 + e2 L2 + e3 L3 = 0 mod m (discrete logs), Bose vs random.
- `code/b22d_multipliers.py` - structure of record multipliers (Amendment 22-5; that test was void, kept for completeness).
- `code/b25m_moments.py` - factorial moments of interval counts in dilates of Singer sets (averaged over shifts and dilations).
- `data/b22c_run.jsonl`, `data/b22c_result.json` - Bose q 101..2003, Singer q 31..211, null sets (Amendment 22-4).
- `data/blind_q2011_5881/` - blind test, Bose q 2011..5881 (Batch 23 A; prediction frozen before computing).
- `data/relations_k3/` - 3-term relation counts (Batch 23 B).
- `data/moments/` - Singer moments q 31..397 (Batch 25 M2-a, Batch 24 M-b) and blind q 409..601 (Batch 25 M2-b).

## Main numbers (from the files)
- q = 829: excess 10.2797 (positive control; Zhang, Math. Comp. 63 (1994): K(p_145) > 10.279).
- g*(q) = G*/q ~ -6.92 + 3.63 ln q on 279 Bose sets (q <= 2003); blind on 48 new q (2011..5881): RMSE 1.52 (log) vs 7.34 (bounded).
- Bose / random 3-term relation ratio 0.983 (95% CI 0.962-1.000).
- Singer: 2nd factorial moment exactly random; R_k ~ c_k(C)/q, blind on q 409..601 (k = 4, C = 2: RMSE 0.0028 vs 0.0238).

## Related work
Green (comments on Gowers's blog, 2012) - dilation idea; Martin-O'Bryant (arXiv math/0408081) - gap criterion for C9; Shakan
(arXiv 2004.14828) and Green's open problem 32; Zhang 1994; Lindstrom 1998; Rokicki-Dogon tables (cube20.org/golomb), which go
much further in size (rulers up to 40,000 marks); our addition is the direct dilate-gap statistic, blind tests and the moment route.

## Licences
Code: MIT. Data: CC BY 4.0. Code and analysis written with AI assistance (Anthropic Claude); reproducible from the files above.
