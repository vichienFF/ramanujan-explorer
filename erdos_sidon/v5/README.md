# erdos_sidon / v5 — supplement to "Dilated Singer sets and the excess in Erdős's Sidon problem", Version 5 (corrective version)

Version 5 corrects Version 4 after two AI referee reports (mathematics; reproducibility). They found no mathematical error in Version 4.
See "Changes in Version 5" at the end of Section 14 of the paper. All drafting and computation were done with AI assistance (Anthropic Claude).
None of the reviews is a human expert review.

## New or changed in v5
- `c9_note_v5.tex`, `c9_note_v5.pdf`, `build_v5.py` (builds v5 from `c9_note_v4.tex`; copy `../v4/c9_note_v4.tex` next to it first; every edit is asserted).
- `kaggle/run_orb.py`: the orbit-reduced program (exact reduction N = Σ over multiplier orbits |O|·T(rep)) that produced the rows q ≥ 4096 of Table 2,
  including the registered blind test at q = 12167, and the later Table 1 caption values. Environment: Kaggle CPU image, Python 3, NumPy, numba (optional; without
  numba the same code runs as pure Python, slowly). Usage: `QS=12167 python run_orb.py` writes `pp_nb.jsonl`. `kaggle/run.py` is the earlier non-reduced version.
  The raw outputs are in `../v3/kaggle_outputs/pp-nbo-*.jsonl` and `pp-nb-*.jsonl`.
- `kaggle/run_nb_top12.py`: the program used for Table 2 rows q = 4096, 4913, 6859 (all triples, no orbit reduction; `run.py` plus the top-12 fields).
- `kaggle_outputs/pp-nbo-i_q16807.jsonl`: raw output for q = 16807 (Table 1 caption). Same output format as `run_orb.py`; that kernel folder itself was not archived.
- Per-row provenance of Table 2 (rows q ≥ 4096) and of the later Table 1 caption values:

| q | program | raw output (folder) | Kaggle runtime |
|---|---|---|---|
| 729, 4096 | `run_nb_top12.py` (QS=729,4096) | `pp-nb-d.jsonl` (v3 `kaggle_outputs`) | 15 s, 3123 s |
| 4913, 6859 | `run_nb_top12.py` (QS=4913,6859) | `pp-nb-c.jsonl` (v3) | 9379 s, 20226 s |
| 12167 (blind Δ) | `run_orb.py` | `pp-nbo-a.jsonl` (v3) | 24502 s |
| 14641 | `run_orb.py` | `pp-nbo-b.jsonl` (v3) | 5363 s |
| 15625 | `run_orb.py` | `pp-nbo-g.jsonl` (v3) | 14810 s |
| 16384 | `run_orb.py` | `pp-nbo-h.jsonl` (v3) | 3051 s |
| 16807 | run_orb format (kernel nbo-i) | `kaggle_outputs/pp-nbo-i_q16807.jsonl` (v5) | 21903 s |
| 19683 | `run_orb.py` | `pp-nbo-f.jsonl` (v3) | 15898 s |

The Kaggle kernels for the `run_orb.py` rows ran byte-identical copies of `run_orb.py` except for the default `QS` line (checked with diff).
- `kaggle/regress_run_orb.py`: regression test. It runs `run_orb.py` for q = 125 and 343 and compares Var(M)/E(M) with an independent brute-force count
  (`../v3/local_probes/probe3.py`, all triples, no orbit reduction) and with Table 1 (1.101, 1.180). Both PASS (identical to 1e-9).
- `scripts/v5_lemma_I3.py`: checks Lemma 1, P(l) − (q−2)² = Σ_μ (I_l(μ))_3, for q = 5..19 and ten l each. Controls: l = 1, where both sides equal q³ − q,
  and l = −1, 2, where both sides vanish. All pass.
- `scripts/v5_prop_gal.py` (+ helpers `n1_sym.py`, `n1_char.py`): checks Proposition 5, C(l) = m²P(l) − ((q−1)m−1)² − (m−1) and P(l) = P(1/l), on all units l for q = 5, 7, 11, 13 (control: P(2) = P(−1) = (q−2)²). `scripts/n1_congr_proof.py` is the older congruence probe (it also lists non-units).
- `N2_PROOF.md`: step 7 corrected. The associate congruent to 1 mod 2 is conj(χ3(2))·J(χ3,χ3); Version 4 wrote χ3(2)·J(χ3,χ3). The conclusion is unchanged.
- `scripts/n2_jacobi.py`: now tests both associates (11/11 primes vs 2/11), skips q ≡ 2 (mod 3) instead of crashing, and exits 1 on failure.
- `review/rv_bruteforce.py`: a dummy check `'P(-2)': True` that always passed was removed.
- `referee_reports/`: the two AI referee reports on Version 4 and the two on the draft of Version 5 (whose findings were applied before release).

## Claim-to-script table (where to reproduce each numbered claim)
| paper item | script / data | folder |
|---|---|---|
| Sec. 2 Bose dilate gaps, log law, blind test, null model | `code/` and `data/` | v1 (`erdos_sidon`) |
| Sec. 3 Proposition (variance, R_3), k=4 blind test, exact R_3 tests, D_mid | `code/`, `plans/`, `data/` | v1, v2 |
| Sec. 4 Proposition 2 (reduction) | proof only | — |
| Sec. 5 Theorem 1 (curves): certificates, genus | `code/irred_cert.py`, `gen_cert.py`, `curve_count.py`, `genus_*.py`, `certificates/` | v2 |
| Sec. 6 identity Σ N² = Σ (I)_3 | `code/identity_I3.py`, `data/v4_v4_identity.jsonl` | v2 |
| Sec. 7 forbidden-structure law (Batch 28/29 blind tests) | `code/b28_*.py`, `b29_*.py`, `ck_pred.py`, `plans/PLAN_BATCH28.md`, `PLAN_BATCH29.md`, `data/b28`, `data/b29` | v2 |
| Sec. 8 variance law (prime q), Table 1 | `code/variance_*.py`, `pp_template.py`, `ppsinger.py`, `data/pp*_pp_v3.jsonl`; `local_probes/probe3.py` | v2, v3 |
| Sec. 9 Proposition 4 (3k ∣ N) | `lean/` (Lean 4 + Mathlib) | v3 |
| Sec. 10 Theorem 2 (resonance) | `sage/*.sage` | v3 |
| Sec. 11 Table 2 rows q ≤ 2197 | `local_probes/`, `kaggle_outputs/` | v3 |
| Sec. 11 Table 2 rows q ≥ 4096, blind test q = 12167 | `kaggle/run_nb_top12.py`, `kaggle/run_orb.py` (+ `regress_run_orb.py`); per-row table above | v5, v3 |
| Sec. 12 Proposition 5 | `scripts/v5_prop_gal.py` | v5 |
| Sec. 12 Lemma 1 and Corollary | `scripts/v5_lemma_I3.py` | v5 |
| Sec. 12 Theorem 3 (a),(b) | `scripts/n1_conic.py`, `n1_cubic.py`, `n1_cubic_proof.py` | v4 (copied here) |
| Sec. 12 Theorem 3 (c), steps 1–7 | `scripts/n2_*.py`, `N2_PROOF.md`, `review/` | v4 (copied, fixed here) |
| Sec. 12 observations | `scripts/n2_hidden.py`, `n2_classes.py`, `n2_height.py` | v4 (copied here) |

## Registrations (self-attested)
Plan files and their SHA-256 hashes were recorded locally before each run. There is no third-party timestamp.
Batch 28 plan (`v2/plans/PLAN_BATCH28.md`) has two amendments, both written before any Batch 28 computation:
(1) Singer sets built with an equivalent faster routine (checked identical at q = 101, 131); (2) NT changed from 1000 to 3000 sampled unit classes.
The ledger therefore records three hashes of that file. `PLAN_PPV3.md` was appended after some outputs existed; only entries dated before a run count as registered for it.

## Requirements
`requirements.txt` lists the versions used for the v5 checks (Python 3.14.3, NumPy 2.4.4, SymPy 1.14.0; SageMath 10.7 for `.sage` files).

`SHA256SUMS`: hashes of every file in this folder.
