# AI referee report (reproducibility) on the Version 6 release — Claude Sonnet, 2026-11-04
(Condensed by the author; all items listed. The referee edited nothing in the release and ran everything on a copy.)

1. SHA256SUMS: PASS (89 files, 0 failures, complete).
2. Claim-to-script mapping: PASS; every exec()/open() target is found by relative path from scripts/; v6_counts.py reads the Kaggle JSONs.
3. Re-runs: PASS, each with its control: v6_counts.py 400; eval_gf.py on c9-gf-a and ch5_small.json; p4_goodred.py; p4_exc_table.py; livne_T.py (16/16 classes, max 241);
   p4_trT.py 7 421 (78 primes, 0 failures); p4_4zm_c1, p4_4zm_rep, p4_deg_proof, p4_n2_proof, p4_n3_classcover, p4_sab_check, p4_n3_cat_check, p4_picard, p4_steps, p4_step3;
   Sage: p4_scope.sage.py (trimmed: 25, 49, 121 EQUAL), p4_n3_pp.sage.py 7^2 13^2 (2022, 27582 EQUAL); gf_ncount.py at 5^3, 5^5, 5^6, 7^3, 13^3, 7^4, 13^4 (all equal, incl. 28561 and 15625).
4. build_v6.py: PASS, byte-identical rebuild of c9_note_v6.tex (TOT=2259, LOC=666).
5. Traceability: ISSUE — no saved outputs for (N3) at the prime powers, for char 3 at 243/729, and for the step-(4) Sage scripts (heights, rank, Galois action).
6. Paths/secrets/personal data: PASS.
Fixes asked: README "Theorem 6" -> actual number; README build path (ship c9_note_v5.tex); P4_FULL_PROOF.md header and referee count; README "every script prints a CONTROL line" is too strong
(p4_A_proof, p4_Sa_proof, p4_cov_proof, p4_steps, p4_step3, p4_rep_sqrt print boolean identity checks); P4_PROOF.md "15 classes" is historical (now 16);
remark that the test set used (incl. 83, 241) is a superset of the primes <= 73; one more LaTeX pass ("Label(s) may have changed").
