# erdos_sidon / v6.2 — supplement for the journal version (added 2026-11-05)

Version 6.2 adds the files cited by the journal manuscript (Theorem on the multiplier 4) that are not in `../v6` or `../v6_1`.
The paper text of Version 6 is unchanged. All files were reviewed by AI referee instances only (no human expert yet).

## Claim-to-file table
| claim | how to reproduce | output |
|---|---|---|
| direct brute-force SPEC equals the class formulas and the target at q = 13^4 = 28561, 11^4, 7^5, 19^3, 17^4 (vectorised GF(p^n) code; its CONTROL compares with the scalar `p4_step5_pp.pieces` at q = 49, 13, 121) | `cd ../v6_1/scripts` then `python ../../v6_2/scripts/p4_step5_vec.py 13^4 11^4 7^5 19^3 17^4` (the script loads `p4_step5_pp.py` from the current folder) | `kaggle_outputs/p4_step5_vec_kaggle.out` (run on Kaggle CPU: 168 s for 28561, 1870 s for 17^4; raw log `kaggle_outputs/c9-spec-pp4.log`) |
| quick local check of the same script | `cd ../v6_1/scripts` then `python ../../v6_2/scripts/p4_step5_vec.py 7^2 13^2 7^3` (a few seconds) | CONTROL PASS and EQUAL lines |
| Livne test set T: 16 primes up to 241 covering all 16 classes of Gal(Q(i, sqrt2, sqrt3, sqrt5)/Q) | `cd ../v6/scripts` then `python livne_T.py` | `scripts/livne_T.out` |
| tr_p = (3/p) b_p and B(p) = 2p + (-1/p)p + tr_p at all primes 7..420 (43 + 35 primes, no failures) | `cd ../v6/scripts` then `python p4_trT.py` and `python p4_trT.py 200 420` | `scripts/p4_trT.out` (both ranges, in this order) |

Every script prints a CONTROL line (a known value from an independent computation) before its result.
Saved outputs were written on Windows (CRLF line endings): compare with `diff --strip-trailing-cr`. Checksums: `SHA256SUMS`.
