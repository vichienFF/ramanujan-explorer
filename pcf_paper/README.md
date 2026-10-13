# Polynomial continued fractions with factorial reduction: seven hidden low-degree equivalences with proofs, a staged identification pipeline, and eight unidentified candidates

Vichien Fugsukjit, Independent researcher, Bangkok, Thailand (9chienvi9@gmail.com)

Code and data for the preprint `paper/pcf_paper_v3.pdf` (earlier drafts kept: `paper/pcf_paper_v2.pdf`, `paper/pcf_paper_draft.pdf`).
Of fifteen factorial-reduction PCFs with irreducible order-4 operators (labels C0-C14), SEVEN are Mobius transforms of
degree-(1,2) PCFs (ratios of Gauss 2F1 functions), verified to 170+ digits, and ALL SEVEN are PROVEN by coboundaries
M1(n) V(n) = lambda(n) V(n-1) M2(n-s) (C0, C10, C11: `data/identifications/b16_C*.json`; C1, C5, C7, C14:
`data/identifications/b20/`, re-checked by `code/b20_independent_check.py`; the exact Mobius maps follow from
`code/b20_mobius_from_proof.py`). The remaining EIGHT (C2, C3, C4, C6, C8, C9, C12, C13) are
released as well-tested candidates, not as new constants (see Limitations in the paper).

The original candidate list `data/irreducible15.json` was time-stamped before disclosure: its SHA-256
(`f9ea8e6c3e541a4fe311175cbe63829c8fc2de53c5d04796600f0c2e493b644f`) is recorded in `../R2_irreducible15_timestamp.md`.
Every later experiment was pre-registered in this repository (PLAN_BATCH*.md, AMENDMENT_*.md) before it was run.

## Quick start: identify or prove a PCF
`python code/identify_pipeline.py --selftest` (Apery zeta(3) found in stage 1; C0 found and proven; a random real stays unidentified)
`python code/identify_pipeline.py "a0,a1,a2" "b0,b1,b2,b3,b4"` runs the staged pipeline on any PCF.

## Conventions
x = a(0) + b(1)/(a(1) + b(2)/(a(2) + ...)), with P_n, Q_n from u_n = a(n) u_{n-1} + b(n) u_{n-2}, P_{-1}=1, P_0=a(0), Q_{-1}=0, Q_0=1.
Full factorial reduction (FR): S_N = (1/N) log(|Q_N| / gcd(P_N, Q_N)) bounded; numerically |S_800 - S_200| < 0.15 (exact integers).

## Pipeline (scripts in `code/`, results in `data/`)
| Step in the paper | Scripts | Output |
|---|---|---|
| 1. Brute force, about 2.3e9 PCFs (Kaggle runs v2_d24 + v3_ext) | bf_search.py, fr_proxy.py, bf_classify.py, bf_summarize.py, known_catalog.py | data/brute_force/summary_*.json |
| 2. Extended search on the six a(n): 5,274 full-FR PCFs | track_a.py | data/ta_5356.jsonl |
| 3. Filters: Conjecture 1.3, deflation, rational/quadratic, Mobius of 36 constants, clustering | track_a_stage3.py, track_a_const_fix.py, conj13_check.py, lowdeg_match.py | data/stage3.json, data/survivors_constfix.json |
| 3. Cohen databases (arXiv 2409.06086, 2607.06581) | cohen_limits.py, cohen_match.py, sandbox.py | data/cohen_hits.json |
| Gamma(1/3)-type members | track_a_gamma.py, track_a_gamma2.py | data/gamma_hits.json, data/gamma2_hits.json |
| 4. Euler type (Petkovsek's Hyper via ore_algebra) | hyper_check.py, sage_hyper.sage | data/hyper_check.json |
| 5. Order-4 operator: factorisation, Riemann schemes, connection coefficients | sage_factor.sage, sage_classify.sage, sage_scheme15.sage, sage_connect15.sage, sage_cvalues.sage, sage_cvalues500.sage | data/classify.jsonl, data/irreducible15.json, data/scheme15.json, data/connect15.json, data/cvalues*.jsonl |
| Novelty tests on the fifteen | pslq_wide15.py, novelty_euler2ai.py, oeis_check.py, deep_id.py (21,984 constants, 1,000 digits) | data/pslq_wide15.json, data/novelty_euler2ai.json, data/oeis_check.json, data/deep_id/ |
| Gamma-product test of C_P, C_Q (150 and 500 digits, planted controls) | gamma_basis.py, identify_cvalues.py, identify500.py | data/cvalues_identified.json, data/identify500*.json |
| Scheme-guided 4F3 test (failed its own control, not counted) | j3_4f3.py | data/j3_4f3.json |
| Theorem (hidden Euler-type example F1) | sage_f1.sage, symproof.py, padic_f1.py | - |
| Low-degree equivalence search (Batches 12-15) | bf_search_b12a.py (targets mode), b12a_verify.py, b13_verify.py, b15_c1_verify.py | data/identifications/b1*_verify.json |
| Mechanism filter (Batches 17-18) | b17_mechanism.py, b18_mechanism.py, b17_verify_c5.py | data/identifications/b17_controls_result.json |
| Coboundary proofs (Batch 16) | b16_coboundary.py, b19_twostep.py (two-step ansatz; its control failed) | data/identifications/b16_*.json |
| Rational-lambda prover, proofs of C1, C5, C7, C14 (Batch 20A, Amendment 20-1) | b20_rational.py, b20_independent_check.py, b20_mobius_from_proof.py | data/identifications/b20/*.jsonl |
| C12 wide-filter rerun (Amendment 18-2) | b18_mechanism.py | data/identifications/b20/b18A_c12c5_r2.jsonl |
| Prevalence sample, exploratory (Batch 20B; mismatch control above its limit) | b20b_mechanism.py, b20B_analyze.py | data/identifications/b20B_result.json |
| Deformation, monodromy, modular L-values, clustering (Batches 10-11) | b10b_deform.py, b10b1_deform.py, sage_monodromy.sage, b11a_modular.py, b11d_ecosystem.py | data/identifications/b10b*_result.json, b11d_result.json, monodromy11b.json |
| Staged pipeline | identify_pipeline.py | - |

## Requirements
Python 3.10+ with numpy, mpmath, sympy; ramanujantools 0.0.8 (deflation, CMF); SageMath 10 with ore_algebra (`.sage` files).
The brute-force and CMF runs used Kaggle CPU notebooks (no internet, no secrets).

## Rebuild the paper
`cd paper && python make_v3.py && pdflatex pcf_paper_v3.tex` (twice; needs the lmodern fonts; v3 is generated from v2). v1: `python make_paper.py && pdflatex pcf_paper_draft.tex`.

## Licences
Code: MIT (`LICENSE`). Data and paper: CC BY 4.0 (`LICENSE-DATA`).
Third-party databases (Cohen, euler2ai) were read for comparison only and are not redistributed here.

## AI disclosure
Code and analysis were written with Anthropic Claude; OpenAI GPT was used as an independent checker. All claims are
reproducible with the released code.
