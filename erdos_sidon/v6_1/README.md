# erdos_sidon / v6.1 — supplement to Version 6 (added 2026-11-04)

Version 6.1 adds programs and outputs written after the Version 6 release, in preparation of a journal version of the theorem on the multiplier 4
(Theorem 4 of Version 6). The paper text of Version 6 (../v6) is unchanged. All files were reviewed by AI referee instances only (no human expert yet).

## What is new
- Step (5) of the proof written out by explicit formulas (no finite verification): `proofs/P4_SPECIAL_LEMMA.md`, sections "Class c = 1 in full",
  "Class c + d = 0 in full", "Class rep in full", "Step 5 CLOSED", "Referee 6" and "Note on q = 28561". Erratum to Version 6: for p = 7, 13 the
  relevant classes are n odd / n = 2 mod 4 / n = 0 mod 4, not "n mod 2" (older lines of the file are marked "[corrected 11-04 ...]"); the
  verification points used cover all three classes, so the theorem is unaffected.
- `proofs/P4_CB_PROOF.md`, `proofs/P4_FULL_PROOF.md`: current versions (good reduction and trace decomposition written out).

## Claim-to-script table (new items)
| claim | script (run from `scripts/`) | output |
|---|---|---|
| class c = 1 closed form (brute force at all 75 primes 7..397) | `python p4_step5_c1.py` | `p4_step5_c1.out` |
| class c + d = 0 closed form | `python p4_step5_cd0.py` | `p4_step5_cd0.out` |
| repeated class closed form | `python p4_step5_rep.py` | `p4_step5_rep.out` |
| sum over the 16 sign patterns = target | `python p4_step5_total.py` | `p4_step5_total.out` |
| class formulas and SPEC by brute force at prime powers 49, 121, 169, 289, 343, 361, 529, 841, 1331, 1369, 2197, 2401 (own GF(p^n) code) | `python p4_step5_pp.py 7^2 11^2 13^2 7^3 17^2 19^2 23^2 29^2 11^3 37^2 13^3 7^4` (without arguments it prints only the CONTROL line) | `p4_step5_pp.out` |
| p = 7, 13: class formulas at 7, 49, 2401, 13, 169, 28561 (n odd / 2 mod 4 / 0 mod 4) | `python p4_step5_p713.py` | `p4_step5_p713.out` |
| determinant of Frobenius on T: B(p^2) = 5p^2 at the 8 test primes p = 2 mod 3 (about 10 min) | `python p4_det_check.py` (reads `p4_ppB.out`) | `p4_det_check.out` |
| residual-discriminant identity disc(R) = -4 D4 / (u^2 (t1^2+t2^2)^2) | `python p4_resid_identity.py` | `p4_resid_identity.out` |
| explicit sections P1, P2, heights 3/2, 2/3, pairing 0 (Sage 10.7) | `sage -python p4_k3_cert.sage.py` (loads `p4_shioda.sage.py`; its reference values are in `p4_shioda.out`) | `p4_k3_cert.out` |
| char 3: q = 729, F3(4) = 530712 (Kaggle; about 93 min locally) | `kaggle_outputs/run_c9-ch3-729.py` (its BENCH comment refers to `../v6/scripts/singer3_243.out`) | `kaggle_outputs/singer3_729.out` |

The scripts load `referee4/perclass.py` (the independent brute-force definition of the per-class terms) by relative path.
Every script prints a CONTROL line (a known value from an independent computation) before its result.
Saved outputs were written on Windows (CRLF line endings): compare with `diff --strip-trailing-cr`.
