# Adversarial referee report: reproducibility, computation, presentation
Paper: "Dilated Singer sets and the excess in Erdos's Sidon problem", Version 4 (Zenodo 10.5281/zenodo.23809651)
Files: `paper_c9/c9_note_v4.tex` (+ PDF), `paper_c9/release_v4/`, `erdos/stepb/`, logs `RESULTS_DIGEST.md`, `PROOF_STATUS.md`
Reviewer: Claude subagent (AI, local, read-only; this file is the only write). Date: 2026-11-01.
Environment used for re-runs: Python 3.14.3, SymPy 1.14.0, NumPy 2.4.4, SageMath 10.7 (WSL). All runs were done on a scratch copy
of the release, not in the project folders.

## What was actually re-run (facts, for context)
- `sha256sum -c SHA256SUMS` inside `release_v4`: all 33 listed files OK; every file in the folder is listed (except SHA256SUMS itself).
  `release_v4/c9_note_v4.tex|pdf` are byte-identical to `paper_c9/c9_note_v4.tex|pdf`; `upload/v4` is identical to `release_v4`.
- Section 12 (Prop. gal, Thm. gal): every release script re-run. n2_types / n2_pairs / n2_lines / n2_assemble on all primes 5..31:
  all CONTROL PASS, N(-2) = ((q-2)(q+1)+b_q)/3 MATCH on all 9 primes. rv_bruteforce on 5..53: ALL PASS (14/14). rv_symbolic: PASS.
  n2_bk1 / n2_jacobi on q = 1 (mod 3), 7..97: 11/11 MATCH. n2_greene_norm 5..97: identity (i) MATCH on all 23 primes, BK value 1/q
  on all q = 2 (mod 3). n2_greene: T = q+1+b_q on all 23 primes. n2_eta: 44/44 primes 5..199. n1_conic / n1_cubic / n1_cubic_proof:
  P(2)=P(-1)=(q-2)^2, P(3), P(-2) values as stated. n2_cm 8/8 HIT; n2_k3, n2_kloost CONTROL PASS. n2_surface.sage: discriminant
  k^3(k+1)^2(k-8), i.e. I3, I2, I1 (+ I6 at infinity), as stated. n2_height (47..79): sd 1.09 (l=-2) and 4.46 (l=7), as stated.
  n2_classes H=12 (11..41): classes {-2,-1/2,1/4,4}, {-1,1/2,2}, as stated. n2_hidden (11..23): only identity and l -> 1/l survive.
- Prop. gal (no release script exists for it): checked independently from Jacobi sums for q=5 (l=2,-1,3,-2,4,5) and q=7
  (l=2,-1,-2,4,5): C(l) = m^2 P(l) - ((q-1)m-1)^2 - (m-1) holds exactly.
- Table 1 / Table 2 small rows: with `release_v3/local_probes` (probe3.Nvec + my own wrapper) q = 121, 125, 128, 169, 243, 343
  reproduce good-rho counts, ratio, ratio/3k, Delta-formula, observed excess and top-6 M/mu exactly as printed.
- Table 2 large rows (729, 4096, 4913, 12167, 15625, 19683; caption controls 14641, 16384): agree with the released raw Kaggle
  outputs `release_v3/kaggle_outputs/*.jsonl` (M/mu, second orbit, excess). They cannot be regenerated: see C1.
- Prime-set counts quoted in Sections 2, 3, 7, 8 recounted (279, 48, 129 = 65+64, 18 + 17 (+1427, 1487) = 37, p_145 = 829): correct.
- Resonance algebra: rho0 = (r+1)r^4 = r^4 + r^-4 lies in the S3-orbit of r + r^-1 and the orbit = roots of the two cubics, for
  r = 5, 7, 8, 11, 13, 17, 23: correct.

---------------------------------------------------------------------------------------------------------------------------
## CRITICAL

### C1. The code that produced Table 2 (rows q >= 4913), the only "blind" excess test (q = 12167), and the Table 1 caption
"later runs" is not released in any version.
- Evidence: the orbit-reduced kernel `kaggle_prize2/rama-pp-nb/run_orb.py` (RESULTS_DIGEST.md:723, "Fixed code run_orb.py uses
  exact multiplier-orbit reduction") is not in `release_v4`, not in `release_v3` (SHA256SUMS lists only build_v3.py, lean/*,
  local_probes/*, sage/*, outputs, plans) and not in `release/erdos_sidon_v2/code`. `release_v3/kaggle_outputs/pp-nbo-*.jsonl`
  are raw outputs only. The released `ppsinger.py`/`pp_template.py` path needs >12 h per cube q >= 12167 (RESULTS_DIGEST.md:723,
  736, 742), so a reader cannot regenerate the headline blind number (Delta = 0.0281 at q = 12167) or rows 4096..19683.
- Why critical: the abstract's only pre-registered blind test of the cube excess, and the Table 2 status column, rest on
  unreleased code. A referee checking reproducibility would stop here.
- Fix: release `run_orb.py` (and the pp-nb / pp-hist kernels) with the exact Kaggle environment, a README line per Table 2 row
  (script, q, runtime), and a small-q regression test showing run_orb reproduces probe3 for q = 125, 343 (already done locally per
  RESULTS_DIGEST.md:723; release it). Add the files to a v4.1 supplement and SHA256SUMS.

---------------------------------------------------------------------------------------------------------------------------
## MAJOR

### M1. The released "full proof" of Theorem gal(c) states a false intermediate fact in Step 7 (q = 1 mod 3).
- Location: `release_v4/N2_PROOF.md:64-65` ("the associate chi3(2)J(chi3,chi3) is the one congruent to 1 mod 2"); same claim in
  the docstring of `release_v4/scripts/n2_jacobi.py:3-4`; the pre-publication review repeats it
  (`INDEPENDENT_REVIEW_C9_V4.md:36`). The paper text (`c9_note_v4.tex:378`) only says "the cubic character of 2 makes the real
  part +-x", which hides the slip.
- Evidence (own computation, same character conventions as n2_jacobi.py): writing z = a + b*omega, chi3(2)*J(chi3,chi3) has
  b odd for q = 7, 13, 19, 37, 61, 67, 73, 79, 97 (9 of 11 primes; it is 1 mod 2 only when chi3(2) = 1, q = 31, 43).
  The associate that is 1 mod 2 for all 11 primes is conj(chi3(2))*J(chi3,chi3). This is what the argument needs anyway,
  because Re(chi3(2) * conj J) = Re(conj(chi3(2)) * J). With chi_pi(2) = pi (mod 2) (cubic reciprocity), conj(chi_pi(2))*pi = 1
  (mod 2), while chi_pi(2)*pi = pi^2 (mod 2).
- Consequence: the theorem is not wrong (all numerics match), but the written proof of a "proved" statement contains a false
  sentence, and neither the script nor two AI reviews tested it (n2_jacobi checks only the HD identity and (qB)^2 = 4x^2).
- Fix: replace with "conj(chi3(2)) J(chi3,chi3) is congruent to 1 mod 2, so Re(chi3(2) conj J) = +-x". Add an explicit test
  to n2_jacobi.py (b-coordinate even for that associate; also print that it fails for chi3(2)J). Give exact Ireland-Rosen
  proposition numbers (cubic reciprocity supplement for 2; Prop. 8.3.4) instead of chapter numbers only.

### M2. The independent-review statement for Theorem gal does not cover Step 7, and the required disclosure was not made.
- Location: `c9_note_v4.tex:389` ("An independent AI review (local, with its own code) found no error"), README line
  "INDEPENDENT_REVIEW_N2.md ... no errors found".
- Evidence: INDEPENDENT_REVIEW_N2.md (PROOF_STATUS step 12, 19:06) predates the q = 1 (mod 3) step (PROOF_STATUS step 14, 19:31)
  and says the proof "currently depends on an unread citation for both residue classes" (INDEPENDENT_REVIEW_N2.md:88-92).
  The pre-publication review's required fix 1 (`INDEPENDENT_REVIEW_C9_V4.md:75-76`) said: have it reviewed "or say it was added
  after the independent review". Neither was done in the paper. M1 shows the step really needed review.
- Fix: in the Verification paragraph state "Step (7) for q = 1 (mod 3) was written after the independent review and was
  checked only numerically and by the pre-publication review". Better: have a human number theorist check Step 7.

### M3. "Registered / blind / pre-registered" labels rest only on self-attested files, and plan amendments are not disclosed.
- Location: abstract (`c9_note_v4.tex:21,25`), Section 2 (line 49), Section 3 (lines 74-83), Section 7 (line 155 "plans frozen
  with a recorded SHA-256 before computing"), Section 11 (lines 284-290).
- Evidence: `math_explorer` is not a git repository; `lane_b/LEDGER.md` hash lines for Batch 28/29 carry no date. The ledger
  records three different hashes of PLAN_BATCH28.md (883ffc38..., 4e83e332..., 0c9318f7...); the file has two amendments
  (`erdos/b28/PLAN_BATCH28.md:16-17`, one changes NT to 3000). File mtimes are consistent with the claimed order (plan 10:58,
  outputs 13:46 on 2026-10-16), but mtimes are not evidence for a reader. `PLAN_PPV3.md` was last modified 2026-10-21 04:41,
  after the q = 12167 output (04:22); it is "append-only" by self-declaration only. Only Section 11 says "Registration times are
  self-attested"; the abstract and Sections 2, 3, 7 do not.
- Internal inconsistency (logs, not paper): RESULTS_DIGEST.md:710 and :735 call 6859 and 15625 "pre-registered"/"blind tests
  passed" for the excess; the paper (Table 2) correctly calls these retrospective/not registered. The paper is the more
  conservative version, but the public record (digest, plans) disagrees with it.
- Fix: one sentence in Section 1 or 14: "All registrations are self-attested: plan files and their SHA-256 were recorded locally
  before the runs; no third-party timestamp exists." List the Batch 28 amendments. For future tests, commit the plan to the
  public GitHub repo (or OSF) before launching the kernel, and cite the commit hash.

### M4. Abstract overstates the scope of the higher-moment blind tests.
- Location: abstract `c9_note_v4.tex:23` "for k <= 8 (up to k=7 at C=2, k=8 at C=4) on 129 primes".
- Evidence: Section 7 (lines 156-158): the first test (65 primes) covers C = 2, k = 3..6 only; the second test (64 primes) covers
  C = 2, k = 3..7 (k = 8 void) and C = 4, k = 3..8. So k = 7 and k = 8 and all of C = 4 rest on 64 primes, not 129.
- Fix: "k = 3..6 at C = 2 on 129 primes; k = 7 (C = 2) and k = 3..8 (C = 4) on 64 of them".

### M5. Novelty claim for the reduction ignores expert feedback received before Version 4.
- Location: `c9_note_v4.tex:105-106` ("what we add is the reduction ... We did not find it in the literature"), line 414.
- Evidence: erdos/OUTREACH_V3.md:79-81 (21 Oct): K. O'Bryant replied that this reduction is "folk wisdom", known informally,
  probably never written down. Version 4 (30 Oct) did not change the claim.
- Fix: "The reduction is regarded as folklore by experts (private communication); we did not find a written proof." (Name the
  source only with permission.)

### M6. release_v4 does not let a reader reproduce most of the paper, and its README does not say so.
- Location: `release_v4/README.md`.
- Evidence: release_v4 contains code only for Section 12 (and the Theorem gal proof). Sections 2, 3, 5-9, Table 1 and Table 2 need
  the v1/v2/v3 folders (and C1 code that is in none). `build_v4.py` reads `c9_note_v3.tex`, which is not in release_v4, so the
  stated build path fails stand-alone. No dependency versions are pinned.
- Fix: add a claim-to-script table to the README covering every numbered claim/table of the paper (with the version folder that
  holds it), include `c9_note_v3.tex` or say where it is, and add a `requirements.txt` (versions above work).

---------------------------------------------------------------------------------------------------------------------------
## MINOR

1. README claim "Each prints a CONTROL line (known answer) before results" is false for `n1_char.py`, `n1_conic.py`,
   `n1_cubic.py`, `n1_cubic_proof.py` (control only described in the docstring or absent), and `n2_surface.sage` (prints the Hesse
   control but asserts nothing). Most controls print FAIL but never exit non-zero. Fix: assert, and exit(1) on failure.
2. `review/rv_bruteforce.py:150` has `'P(-2)': True` - a dummy check that always passes and is counted in "ALL PASS". Remove it or
   compute P(-2) over F_{q^3} (n2_height already does this; its CONTROL passed for 5..79).
3. `scripts/n2_jacobi.py:18` crashes (StopIteration) for any q = 2 (mod 3), although README usage says `python <script> q1 q2 ...`
   with primes. `n2_bk1.py` silently skips them. `n2_types.py:29` CONTROL is vacuous for q not in {5,11,17} (only the type
   total is checked). `n2_lines.py:6` comment "n2_pairs runs its own CONTROL at import" is stale (import is guarded).
   `n2_bk1.py:3` docstring is garbled ("= q + b_q + q...").
4. Verification paragraph (`c9_note_v4.tex:385`) "step (7) on 7 <= q <= 97": the Jacobi-sum part was checked on q = 1 (mod 3)
   only; the q = 2 (mod 3) value on "5 primes" (N2_PROOF.md:61). State both ranges. (I re-ran both on all primes to 97: pass.)
5. Proposition gal has no verification script in any release (only n1_char checks C(q)/C(1)). The proof is short and I verified
   it numerically (q = 5, 7), but add the script (`n1_congr_proof.py` is cited in PROOF_STATUS.md:18 and not released).
6. Geometric explanation (`c9_note_v4.tex:391-394`) is stated as fact ("is the singular K3 surface ... transcendental lattice
   diag(2,6) [HS]") and "identified ... by exact computation". Per PROOF_STATUS.md:34 the explicit isomorphism with the
   Hulek-Schuett model was a TODO and never done; n2_surface.sage only gives the fibre types (I3, I2, I1, I6), which do not fix
   the transcendental lattice (the torsion of the Mordell-Weil group also matters). Write "should be" / "we expect" or do the
   isomorphism. The conclusion "CM by Q(sqrt(-3))" is safer than "diag(2,6)".
7. Height-growth observation (`c9_note_v4.tex:400`): the window 47 <= q <= 79 (n = 4-8 values per l) was chosen after the
   pre-publication review found sd 12.3 at l = 7 on 5..79. On 5..43 I get sd 14.8 (l = 7) and 6.4 (l = 5); within 47..79 the
   growth is not monotone (l = 6: 1.95; l = 3: 0.006; l = 3/2: 2.98). Say "rough" and give n per l, or drop the claim.
8. Section 11 text (line 309) "55-100% (lowest at q = 512)": from the table, 0.021/0.039 = 54%. Use the unrounded values.
9. Table 1 caption lists 11 later non-cube q but omits q = 16807 (Var/E 1.0020, RESULTS_DIGEST.md:741). It fits the stated range;
   list it for completeness.
10. Abstract item (iii) omits the hypothesis "m prime" that Section 6 (line 139) uses.
11. Hard-coded cross-references: line 401 "Sections 4--9" for the Poisson-type laws (they are Sections 7-9; Section 4 is the
    reduction, 5 the curves). Line 88 "Sections 4--8" is fine but should use \ref. Use \ref throughout.
12. Notation overload: L (2-dim subspace in Sections 5/10 vs discrete log in Section 12), phi (q-Frobenius in Section 10 vs
    quadratic character in Section 12), psi (phi(x)/x vs a character of order m), C (window constant, curve C_{u,v},
    autocorrelation C(l), coefficient C in Section 10), E (mean triple count vs E_1, E_2, E_3), S (Singer set vs S = phi in [BK]),
    N (triple count vs field norm). A referee will ask for one notation table.
13. LaTeX: overfull boxes of 43.9 pt and 12.4 pt in the proof of Proposition 2 (source lines 98-104, visible in the margin) and
    18.6 pt in "Data and code" (lines 419-421); two hyperref "Token not allowed in a PDF string" warnings.
14. Date: title page says Version 4 of 31 October 2026; PROOF_STATUS.md:16 says "V4 PUBLISHED 2026-10-30" and the build/upload are
    30 Oct 21:13-21:36 (+0700). Make the Zenodo date and the title-page date agree.
15. Bibliography: [Guy] is cited for the USD 500 prize, but Limitations (line 415) says "Guy's C9 entry ... not checked". [BK]
    is cited as arXiv; check whether a journal version exists (the pre-publication review suggested IJNT 2012, unverified). [Gr]
    "manuscript, updated 2026" has no URL. [Ke] is an REU report. Exact theorem numbers missing for [IR].
16. The rv_* "independent review" scripts are by the same AI system family as the author pipeline; the paper says so ("not a
    human expert review"), which is correct, but "independent" should be "separate AI instance".

---------------------------------------------------------------------------------------------------------------------------
## Item 3 of the brief: "for all primes q >= 5" claims resting only on numerics
- Theorem gal (a), (b), Proposition gal: complete hand proofs; numerics are confirmation only. OK.
- Theorem gal (c): Steps 1-6 are hand-proved in N2_PROOF.md (I re-derived Step 2, the three excluded-line values 2q-4, 2q-6, -3
  of Step 3, and Step 5); the paper itself only lists the values (line 369) without derivation, so the paper alone does not
  prove Step 3. Step 7 depends on [BK] Thm 1.7 (preprint, statement read) plus textbook facts, and its written form contains
  the false sentence of M1. No step rests on numerics alone, but Step 7 is the weak link.
- "b_q = a_q(eta(2t)^3 eta(6t)^3)": correctly labelled numerical (44 primes); not used in the proof.
- Theorem res (Section 10): uses Sage identities over Q (stated); not re-run here (v3 scope).
- Theorem curve (d): certificates claimed released in v2; not re-run here.

## Item 5: what a journal referee would object to at once
1. C1 (unreleased code behind the key blind test) and M3 (self-attested registration) for the empirical half.
2. M1/M2 for the one new "proved" theorem of Version 4.
3. Format: a 14-section, 5-part-title cumulative "version" note mixing theorems, conjectures, heuristics, blind tests and
   anomaly logs. A journal would ask to split it (e.g. (i) Theorem gal + Prop gal as a short finite-field paper; (ii) the
   resonance theorem; (iii) the reduction + numerics), each with its own clean proof and data section.
4. The abstract is ~450 words and contains registration bookkeeping; trim to the proved results and one line of evidence.
