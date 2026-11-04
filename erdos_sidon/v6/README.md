# erdos_sidon / v6 — supplement to "Dilated Singer sets and the excess in Erdős's Sidon problem", Version 6

Version 6 adds Section "The multiplier 4" with Theorem 4 (label thm:four): for q = p^n, p >= 7,
sum_mu (|S ∩ (4S+mu)|)_3 = (q-2)(q+1) + b_q, where b_q = alpha^n + beta^n (alpha + beta = b_p, alpha*beta = (-3/p) p^2).
The proof is computer-assisted. It was reviewed by AI referee instances only (Anthropic Claude Sonnet; the author's drafts were written with Anthropic Claude Opus); it has NOT been reviewed by a human expert.
Everything from Versions 1-5 is unchanged and stays in the earlier folders (../v1 ... ../v5).

## Files
- `c9_note_v6.tex`, `c9_note_v6.pdf`, `build_v6.py` (builds v6 from `c9_note_v5.tex`, a copy of the Version 5 source shipped here; every edit is asserted; the verification counts are parsed from `scripts/v6_counts.out`).
- `proofs/P4_FULL_PROOF.md` (overview with labels), `proofs/P4_PROOF.md` (historical step log), `proofs/P4_CB_PROOF.md` (the K3 surface, good reduction, Livné), `proofs/P4_SPECIAL_LEMMA.md` (special classes, exceptional-point table).
- `scripts/`: every script used in the proof (`p4_*.py`, `p4_*.sage.py` run with Sage 10.7), helpers (`livne_T.py`, `singer3.py`, `gf_ncount.py`, `eval_gf.py`), saved outputs (`*.out`, `*.json`), the referee's own scripts (`scripts/referee4/`).
  Scripts that load other scripts do so by relative path; run them from inside `scripts/`.
- `kaggle/run_*.py`: the Kaggle programs; `kaggle_outputs/*.json`: their outputs (c9-n3-huge-a/b: primes 5000..19999; c9-gf-a: q = 3^10, 5^7).
- `referee_reports/`: AI referee report 5 on the proof in full (referees 1-4 are summarised inside the proof files) and the two AI referee reports on the Version 6 draft (math, repro).

## Claim-to-script table
| paper item | script / data |
|---|---|
| (N3) at all primes 7..19999 (count printed) | `scripts/v6_counts.py` -> `scripts/v6_counts.out` (local 7..4999 + `kaggle_outputs/c9-n3-huge-*`) |
| (N3) at prime powers 49, 121, 169, 343, 2197, 2401, 28561; char 5 at 5^n, n <= 7 | `scripts/v6_pp.py` -> `scripts/v6_pp.json`, `scripts/v6_pp.out` (evaluated by `eval_gf.py`); `scripts/ch5_small.json`; `kaggle_outputs/c9-gf-a_gf_ncount.json`; also `scripts/p4_n3_pp.sage.py` |
| step (1): N1, N2, degenerate and repeated-root corrections | `scripts/p4_steps.py`, `p4_step3.py`, `p4_deg_proof.py`, `p4_n2_proof.py`, `p4_n3.py` |
| step (2): main-term identity, categories of E | `scripts/p4_n3_assembly.py` (`.out`), `p4_n3_cat_check.py` (`.out`), `p4_boundary*.py`, `p4_cd0_points.py`, `p4_c1class.py` |
| step (3): substitution, A, A', B' | `scripts/p4_cov_proof.py`, `p4_A_proof.py`, `p4_Sa_proof.py`, `p4_sab_check.py` |
| step (3)-(4): B and the K3 surface (reduction, heights, Galois action, traces, good reduction) | `scripts/p4_bookkeep.sage.py`, `p4_picard.py`, `p4_shioda.sage.py`, `p4_mwgal.sage.py` (saved outputs `*.out`), `p4_trT.py` (argv LO HI), `livne_T.py`, `p4_goodred.py` |
| step (5): special classes, conics, exceptional sets, class cover | `scripts/p4_loci.py`, `p4_loci_genus.sage.py`, `p4_4zm_c1.py`, `p4_4zm_rep.py`, `p4_rep_sqrt.py`, `p4_exc_table.py`, `p4_n3_classcover.py` |
| direct third moments from Singer sets (q = 25, 49, 121, 125) | `scripts/p4_scope.sage.py` (`p4_scope.out`) |
| char 3 observation | `scripts/singer3.py` (`singer3_243.out`: controls q = 9, 27, 81 and q = 243; q = 729 is `python singer3.py 6`, run 2026-11-03, result 530712 recorded in the plan log, no saved output), `p4_ch3.sage.py`, `p4_ch3_counts.sage.py` |

Most scripts print a CONTROL line (a known value from an independent computation or theory) before their result; `p4_A_proof`, `p4_Sa_proof`, `p4_cov_proof`, `p4_steps`, `p4_step3` and `p4_rep_sqrt` instead print the exact identity checks (True/False) that they verify.
The Livné test set used by `livne_T.py` (16 Frobenius classes, primes up to 241) contains the primes <= 73 that suffice by Schütt (arXiv:1112.0405, Sect. 2.7-2.8); `p4_trT.py` checks all primes 7..420, which covers both.
Registrations ("registered", "blind") are self-attested: a plan line with a timestamp was written before the computation; there is no third-party timestamp.
