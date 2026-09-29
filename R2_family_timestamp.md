# Timestamp record: PCFs with full factorial reduction outside a known family (2026-09-29)

This file records only a cryptographic fingerprint. The list itself is not published yet.

- Content: 24 polynomial continued fractions (a(n) of degree 2, b(n) a product of 4 rational linear factors)
  selected from our 239 unidentified candidates (see R2_candidates_timestamp.md) such that
  1. the reduced convergents grow only exponentially: S_N = (1/N) log(|Q_N| / gcd(P_N, Q_N))
     changes by less than 0.15 between N = 200 and N = 800 (full factorial reduction, numerical evidence),
  2. they are NOT members of the family of Conjecture 1.3 in Ben David et al.,
     "On the Connection Between Irrationality Measures and Polynomial Continued Fractions"
     (Arnold Mathematical Journal, 2024; arXiv 2111.04468), even allowing index shifts of -2..2,
  3. ramanujantools PCF.deflate_all() does not reduce their degree.
- Status: candidates only (evidence label: proposed). Not claimed as new.
- File: bf_runs/test_fr/outside_conj13.json
- SHA-256: 824221a7daf62aa1ae35821f78f6935d872d41a564dd06602c10ce6494e5d9f9

Author: Vichien Fugsukjit (Independent Researcher, Bangkok)
