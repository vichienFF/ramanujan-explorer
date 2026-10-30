# erdos_sidon / v4 — supplement to "Dilated Singer sets and the excess in Erdős's Sidon problem", Version 4 (31 Oct 2026)
- `c9_note_v4.tex`, `v4_new.tex`, `build_v4.py`: source of Version 4 (`build_v4.py` builds it from the v3 source plus the new Section "Galois autocorrelation of Jacobi sums: exact values"; every edit is asserted).
- `c9_note_v4.pdf`: compiled with pdfTeX (TeX Live).
- `N2_PROOF.md`: full proof of Theorem (c) (N(−2) and P(−2)), seven steps, with the fixes from the review.
- `INDEPENDENT_REVIEW_N2.md`: independent (AI, local-only, own code) review of the proof: no errors found, 6 exposition fixes (applied). Not a human expert review.
- `review/rv_bruteforce.py`, `review/rv_symbolic.py`: the reviewer's independent checks (theorem brute-forced on all primes 5..53).
- `scripts/`: verification scripts (Python 3 + SymPy/NumPy; `n2_surface.sage` needs SageMath 10.7). Each prints a CONTROL line (known answer) before results. Usage: `python <script> q1 q2 ...` (primes).
  - Theorem (a),(b): `n1_conic.py`, `n1_cubic.py`, `n1_cubic_proof.py`.
  - Theorem (c), proof steps: `n2_types.py` (step 1 + type census), `n2_pairs.py` (steps 2–3), `n2_disc.py` (residual discriminant), `n2_lines.py` (excluded lines), `n2_greene.py` + `n2_greene_norm.py` (step 4), `n2_double.py` (step 5), `n2_assemble.py` (step 6), `n2_bk1.py` + `n2_jacobi.py` (step 7), `n2_eta.py` (eta-product coefficients).
  - Geometric explanation (not used in the proof): `n2_kloost.py`, `n2_k3.py`, `n2_cm.py`, `n2_surface.sage`.
  - Observations: `n2_hidden.py`, `n2_classes.py`, `n2_height.py`.
  - Helpers: `fq3.py`, `n1_char.py`.
- `SHA256SUMS`: hashes of every file.
Status labels follow the paper: "proved" = complete proof (one step cites Barman–Kalita Thm 1.7 / Ono 1998 and two textbook facts); "observed" = exact computation on the stated ranges only. Drafting and computation were done with AI assistance (Anthropic Claude).
