# erdos_sidon / v3 — supplement to "Dilated Singer sets and the excess in Erdős's Sidon problem", Version 3 (21 Oct 2026)
- `c9_note_v3.tex`, `v3_new.tex`, `build_v3.py`: source of Version 3. `build_v3.py` builds it from the v2 source plus the new sections.
- `lean/C9Orbit.lean`, `lean/C9Order.lean`: Lean 4 + Mathlib proofs for the freeness step and order 3k (Proposition "Orbits of the multiplier group"). Standard axioms only.
- `sage/`: computer-algebra verification for the Resonance Theorem.
  - `identity_check.sage`: N(A)+N(B) ≡ 0.
  - `cond2_check.sage`: adj(Dickson)·(C, C^r, C^{r^2}) ≡ 0.
  - `A_factor.sage`: factorisation of A.
  - `sym_charp.sage`: the identities over GF(2), GF(3), GF(5), GF(7).
  - `bridge_check.sage`, `brute.sage`, `exceptions.sage`, `resonance_lemma.sage`: exhaustive checks for r ≤ 13.
  Run with SageMath 10.7: `sage <file>.sage <args>`.
- `kaggle_outputs/`: raw outputs (top-12 ratios, cubic-root flags, M histograms) of the blind tests and controls.
- `plans/PLAN_PPV3.md`: pre-registrations (C9-RES, C9-CUBIC, C9-RES-2, ...), written before the runs.
- `INDEPENDENT_REVIEW_RES.md`: independent review of the theorem's proof (verdict ACCEPT WITH FIXES; the fixes are included in the paper).
- `SHA256SUMS`: hashes of every file.
- `kaggle_outputs/pp*_ / hist*_` (added after review): raw outputs behind Table tab:pp "later runs" and the q=6859 pp-v3 run (ppf).
- `local_probes/`: local scripts behind the q=125/343/1331 numbers (probe3/4/8), the subline cross-ratio check, and the Singer-set builder (ppsinger.py).
- `INDEPENDENT_REVIEW_C9_V3.md`: pre-publication review of this version (verdict PUBLISH AFTER FIXES; all FAIL items fixed in the released .tex).
- Registration timing: PLAN_PPV3.md is an append-only file; its timestamps are self-attested (the ledger hashes are in the main repository).
