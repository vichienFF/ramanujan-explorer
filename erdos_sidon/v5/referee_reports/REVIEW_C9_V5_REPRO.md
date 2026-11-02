# Adversarial referee report: reproducibility and presentation, C9 note Version 5
Release reviewed: `D:/Research_FlyBrain/math_explorer/paper_c9/release_v5/` (paper `c9_note_v5.tex/.pdf`, README, `kaggle/`, `scripts/`, `review/`, `N2_PROOF.md`).
Compared against: `REVIEW_C9_V4_REPRO_2026-11-01.md`, `REVIEW_C9_V4_MATH_2026-11-01.md`, releases v1-v4, `c9_note_v4.tex`, `build_v5.log`.
Reviewer: AI referee (Claude subagent), 2026-11-02. All runs were done on a scratch copy
(`C:/Users/user/AppData/Local/Temp/claude/C--Users-user/c53ce00a-9167-44da-bdf0-c9332628bf16/scratchpad/repro5/`). No project file was changed.
Environment: Windows 10, Python 3.14.3, NumPy 2.4.4, SymPy 1.14.0, numba NOT installed (so run_orb.py ran in its pure-Python fallback).

## Verdict
Version 5 fixes the critical item of the V4 report. `kaggle/run_orb.py` is released, its regression test passes, and a local run at q = 729
reproduces the released Kaggle record exactly. All five scripts I was asked to run pass and exit 0. Where I checked, they exit 1 on a
real error (mutation tests). The paper rebuilds byte-identically from `c9_note_v4.tex` with `build_v5.py`. It has no undefined references or
citations, and the theorem/section numbers in the README match the compiled PDF.
No CRITICAL problem remains. One MAJOR documentation issue remains: the provenance of Table 2 rows q = 4096, 4913, 6859 is stated
wrongly or loosely. Several MINOR README/paper issues remain: a missing SHA256SUMS file, missing "Version 5 reports", a q = 16807 value
with no released data, two scripts that can still pass vacuously or never exit non-zero, and overfull boxes. Several old minor items
(notation, hard-coded refs, IR theorem numbers, V4 date) are still open.
Recommendation: accept as a corrective release after the README/caption fixes in M-A and m1-m5. None needs new computation.

## What was run (facts)
| script | arguments | result | runtime | exit |
|---|---|---|---|---|
| `kaggle/regress_run_orb.py` | v3 `local_probes` copy | q=125: V/E 1.101252 = independent 1.101252, table 1.101, 3k\|N PASS; q=343: 1.179755 = 1.179755, table 1.180, PASS | 10.5 s | 0 |
| same, mutated run_orb (weight w replaced by 1) | | both FAIL | | 1 |
| `kaggle/run_orb.py` | QS=729 (pure Python) | V/E 1.0421904548302134, all_div_3k true; every field except sec/numba identical to v3 `kaggle_outputs/pp-nb-d.jsonl` (incl. M_hist, top12) | 33 s | 0 |
| `scripts/v5_lemma_I3.py` | 5 7 11 13 17 19 | CONTROL PASS and lemma MATCH for all 6 primes | 1.7 s | 0 |
| same, mutated ((q-2)^2 -> (q-3)^2) | 5 7 | MISMATCH | | 1 |
| `scripts/v5_prop_gal.py` | 5 7 11 13 | CONTROL PASS; Prop 5 MATCH on all 30/36/108/120 units (= phi(m)) | 1.2 s | 0 |
| same, two mutations (shift in C formula; P(l)=P(2l) instead of P(1/l)) | 5 / 7 | FAIL | | 1 |
| `scripts/n2_jacobi.py` | all primes 7..97 | 11/11 primes q = 1 mod 3: CONTROL PASS, HD MATCH, (qB)^2 = 4x^2 = 2q+b_q, v5 associate 1 mod 2 on 11/11, v4 associate on 2/11 (q = 31, 43, where chi3(2) = 1); 12 primes q = 2 mod 3 skipped | 0.1 s | 0 |
| same | 11 (q = 2 mod 3 only) | "skipped", no crash | | 0 |
| same | no arguments | prints nothing | | 0 (vacuous, see m4) |
| `review/rv_bruteforce.py` | 5 7 11 13 17 19 23 29 31 | ALL PASS on 9/9 | 0.2 s | 0 |
| `build_v5.py` | with `c9_note_v4.tex` copied next to it | "32 edits, all asserted"; output byte-identical to released `c9_note_v5.tex` | <1 s | 0 |

Other checks: `release_v5/c9_note_v5.tex|pdf` are byte-identical to `paper_c9/c9_note_v5.tex|pdf`; the PDF and aux are newer than the tex.
All 27 bibitems are cited and every citation has a bibitem. Labels in the aux: Prop 2 (reduction, Sec 4), Thm 1 (curves, Sec 5),
Prop 4 (3k\|N, Sec 9), Thm 2 (resonance, Sec 10), Table 2 (Sec 11), Prop 5 and Lemma 1 (Sec 12), Thm 3 (Sec 12). These match the README table.
Every file and folder named in the README claim-to-script table exists in v1 (`erdos_sidon/code`, `data`), v2 (`code/irred_cert.py`,
`gen_cert.py`, `curve_count.py`, `genus_family.py`, `genus_mono.py`, `identity_I3.py`, `b28_*`, `b29_*`, `ck_pred.py`, `variance_*.py`,
`pp_template.py`, `ppsinger.py`, `certificates/`, `data/v4_v4_identity.jsonl`, `data/b28`, `data/b29`, `data/pp*_pp_v3.jsonl`,
`plans/PLAN_BATCH28.md`, `PLAN_BATCH29.md`), v3 (`local_probes/probe3.py`, `lean/`, `sage/`, `kaggle_outputs/`) and v5.
Table 1 caption and Table 2 numbers checked against v3 raw outputs: cube ratios 1.022/1.038/1.064 (4096/4913/6859); 12167 V/E 1.0281
(Delta 0.0281); 15625 1.0261; 19683 1.0092; later non-cube range [0.9980, 1.0026] matches 2209..16384 (0.99796 at 3481, 1.00262 at 4489).
The new "54%" equals 0.021/0.039 = 0.538; the other rows are 76-100%. Body: 37 primes 293..2969, mean 2.998, range [2.979, 3.019]
(max deviation 0.7%, consistent with V4's "0.8%"). The 65 + 64 = 129 primes and the C = 2 / C = 4 cells of Section 7 now match the abstract.

---------------------------------------------------------------------------------------------------------------------------
## CRITICAL
None.

---------------------------------------------------------------------------------------------------------------------------
## MAJOR

### M-A. Table 2 provenance for q = 4096, 4913, 6859 is stated as run_orb.py, but the released data say otherwise.
- Paper, Table 2 caption (tex line 315): "Rows q >= 4096 were computed with the orbit-reduced program run_orb.py". README says the same
  ("the orbit-reduced program ... that produced the rows q >= 4096"). Changes item (4) says the same.
- Evidence: the raw records for 4096 (`pp-nb-d.jsonl`) and 4913, 6859 (`pp-nb-c.jsonl`) are "pp-nb" files, not "pp-nbo". The README itself
  calls `run.py` "the earlier non-reduced version". Those records contain `top12` and `top12_cubic_roots`, which the released `run.py`
  does not write. So they came from a third, unreleased variant: non-reduced count plus top-12 output. Only 12167, 14641, 15625,
  16384, 19683 are in pp-nbo files. Also, the docstring of `regress_run_orb.py` says "Table 2 rows q >= 4913", which contradicts the caption.
- Why it matters: the numbers are almost certainly right. run_orb at q = 729 reproduces the pp-nb-d record field by field, and the
  orbit reduction is exact. But the paper's provenance sentence is the item that resolves C1, so it should be literally true.
- Fix (text only): "Rows q >= 12167 (and the controls 14641, 16384) were computed with run_orb.py. Rows 4096, 4913, 6859 were computed with
  the non-reduced kernel (run.py with top-12 output). run_orb.py reproduces these records exactly where we re-ran them (q = 729 locally)."
  Add a per-row table to the README: q, output file, program, runtime. The V4 report asked for this, and the data are in the jsonl "sec" fields.
  Either release the top12 variant of run.py, or say that run.py differs from it only in output fields.

---------------------------------------------------------------------------------------------------------------------------
## MINOR

m1. **README names files that are not in the release.** "`SHA256SUMS`: hashes of every file in this folder": there is no SHA256SUMS
    in `release_v5/`. "`referee_reports/`: the two AI referee reports on Version 4 and the reports on Version 5": only the two V4 reports
    are there. Generate SHA256SUMS last, or remove those lines.

m2. **README paths do not match the scripts.** (a) README: "build_v5.py (builds v5 from c9_note_v4.tex, which is in ../v4)". The script
    reads `c9_note_v4.tex` from its own folder and fails otherwise (FileNotFoundError). It works once the file is copied next to it. (b)
    `regress_run_orb.py` defaults to `../../release_v3/local_probes`, which is the local layout. The README and GitHub layout use `v3`, so on
    GitHub the default path is wrong and the argument is mandatory. Say so in the README usage line, or try both paths.

m3. **q = 16807 (added to the Table 1 caption in V5) has no released raw output.** It is not in v3 `kaggle_outputs`. It exists only at
    `math_explorer/erdos/stepb/kaggle_nbo_i/pp_nb.jsonl` (RESULTS_DIGEST.md:740: Var/E 1.0020, 6.1 h). Copy it into the v5 release.
    The same applies to the pending q = 24389, 32768 runs once they finish.

m4. **Vacuous pass and missing exit codes.** `n2_jacobi.py` with no arguments, or with only q = 2 mod 3 primes, tests nothing and exits 0.
    Add a default prime list, or exit 1 when zero primes were tested. `review/rv_bruteforce.py` prints "ALL PASS" or the failing checks but
    always exits 0 (only its asserts can fail the run). The README fix "dummy check removed" is correct, but the script is still not CI-safe.
    The v4 scripts `n1_char/n1_conic/n1_cubic/n1_cubic_proof/n2_types/n2_lines/n2_bk1/n2_surface.sage` are unchanged from v4
    (byte-identical), so V4 minor items 1 and 3 remain for them.

m5. **"No mathematical error was found" (paper Sec 14, README line 3) sits next to a correction of a false sentence in the released proof.**
    The V4 repro report (M1) found exactly that. Suggested wording: "no error in any stated result; one false intermediate sentence in the
    released proof file (step 7) was corrected."

m6. **README docstring details.** README and paper: v5_lemma_I3 uses "ten l each". In fact the list has 8-10 values after the unit filter,
    with duplicates (q = 5: l = 5 twice; q = 7: 7 twice; q = 11: 8 values). The script default is q = 5, 7, 11, 13; the paper's 5 <= q <= 19
    needs explicit arguments. Likewise v5_prop_gal defaults to 5, 7, 11, while the README says 5, 7, 11, 13. Give the exact command lines in
    the README.

m7. **run_orb.py does not verify that S is a Singer (Sidon) set.** It checks only |S| = q+1 and p-orbit closure. An O(q^2) difference check
    would cost seconds. The regression test shares the Singer-construction lineage with `ppsinger.py`, so it validates the orbit reduction
    and counting, not the construction. The numba version used on Kaggle is not recorded (`requirements.txt` says only "numba optional").

m8. **"Changes in Version 5" omits several real changes:** the new disclosure that step (7) was written after the separate AI review (V4 M2);
    the Table 2 caption note on composite m (unit-difference count, N(rho1) = 576 vs 630 at q = 125); the LMFDB citation and the "weight-3
    newform of level 12" wording; the "Sections 7-8" fix; the "separate AI" wording. None is misleading, but a "changes" list should be complete.
    The list items that are claimed (Lemma 1, Corollary, folklore wording, 129/64 abstract, run_orb, step-7 sentence, c = d case, Prop 5 proof
    wording, hedges, 54%, 16807) were all verified in the v4 -> v5 diff.

m9. **Abstract (v) defines b_q only as "the q-th coefficient of the CM newform".** In the body, the proved form is b_q = 4x^2 - 2q
    (0 for q = 2 mod 3). The newform identification is "standard Hecke-character description ... checked for 5 <= q <= 199, not used below".
    Give the elementary definition in the abstract too, so the "Proved" item does not rest on an unproved identification.

m10. **LaTeX (build_v5.log):** no undefined references or citations. Seven overfull boxes: 43.9 pt and 12.4 pt (proof of Prop 2, source
    lines 103-109; unchanged from V4), 18.6 pt and 6.9 pt (Data and code URLs, lines 455-457), 5.6 pt (line 70), 2.5 pt (lines 298-315,
    Table 2). Two underfull boxes in the Gowers bibitem. Two hyperref "Token not allowed in a PDF string" warnings (line 229, the "$q$" in a
    section title; use \texorpdfstring). Two "h float specifier changed to ht".

m11. **Hard-coded cross-references remain:** 11 occurrences of "Section~<digit>" (for example "Section~6 in another form", "Section~1",
    "Section~3") instead of \ref.

m12. **Self-attested registration statements: consistent.** Abstract, Section 1, Section 7 (amendments), Section 11 and Section 14 now all
    say "self-attested". The README lists the two Batch 28 amendments, which match `PLAN_BATCH28.md` lines 16-17 and the three ledger hashes
    (SHA256_LEDGER.md lines 16, 19, 21), and the PLAN_PPV3 caveat. The RESULTS_DIGEST.md lines that call 6859/15625 "pre-registered" for the
    excess are not corrected, but they are logs, not part of the release.

---------------------------------------------------------------------------------------------------------------------------
## V4 repro items: status in Version 5
| item | status | note |
|---|---|---|
| C1 unreleased run_orb.py | FIXED (substance) / PARTLY (documentation) | released; regression passes and fails under mutation; q = 729 reproduces the Kaggle record exactly; output format identical to the pp-nbo files. Per-row provenance and runtime table missing; rows 4096-6859 misattributed (M-A); numba version not pinned |
| M1 false sentence step 7 | FIXED | N2_PROOF.md and n2_jacobi.py corrected; both associates tested (11/11 vs 2/11). Exact Ireland-Rosen proposition numbers still not given in N2_PROOF.md (only "ch. 8/9") or in [IR] |
| M2 review coverage disclosure | FIXED | paper says step (7) for q = 1 mod 3 was written after the separate AI review |
| M3 self-attested registration | FIXED | abstract, Sec 1, 7, 11, 14 and README; amendments listed |
| M4 abstract scope 129/64 | FIXED | |
| M5 folklore | FIXED | abstract, Sec 1 and Changes |
| M6 release usability | FIXED (mostly) | claim-to-script table, requirements.txt, build note. But SHA256SUMS is missing (m1) and the build path is wrong (m2) |
| minor 1 CONTROL/exit codes | PARTLY | README no longer claims CONTROL lines for all; new v5 scripts exit 1; v4 scripts unchanged; rv_bruteforce has no exit code |
| minor 2 dummy P(-2) | FIXED | removed (comment points to n2_height / v5_lemma_I3, both of which check l = -2) |
| minor 3 n2_jacobi crash etc. | PARTLY | n2_jacobi fixed (but vacuous with no args, m4); n2_types vacuous control, n2_lines stale comment, n2_bk1 garbled docstring unchanged |
| minor 4 step (7) ranges | FIXED | |
| minor 5 Prop gal script | FIXED | v5_prop_gal.py, n1_congr_proof.py released |
| minor 6 K3 claim | FIXED | "we expect ... have not written down the isomorphism" |
| minor 7 height observation | FIXED | n per l given; "rough", "not monotone" |
| minor 8 55% -> 54% | FIXED | |
| minor 9 q = 16807 | PARTLY | listed, but its raw output is not released (m3) |
| minor 10 "m prime" in abstract (iii) | FIXED | |
| minor 11 hard-coded refs | PARTLY | "Sections 4-9" changed to "7-8"; 11 hard-coded "Section~N" remain |
| minor 12 notation table | OPEN | |
| minor 13 LaTeX boxes/warnings | OPEN | same 43.9/12.4/18.6 pt boxes plus new small ones; hyperref warnings remain |
| minor 14 V4 date 30 vs 31 Oct | OPEN | title page still says "Version 4: 31 October 2026" |
| minor 15 bibliography | PARTLY | [BK]: "did not confirm a journal version" added; [Gr] still has no URL; [IR] chapters only; [Guy] still "not checked" |
| minor 16 "independent" -> "separate AI" | FIXED | remaining "independent" uses refer to brute-force counts, which is fine |

---------------------------------------------------------------------------------------------------------------------------
## Not checked
- Kaggle runs for q >= 4096 were not re-run (hours each). q = 1331 was not run locally (estimated > 15 min in pure Python). Only q = 125,
  343 (regression) and 729 were run. numba was not installed, so the numba code path was not exercised locally. Equality at q = 729 with a
  numba-produced record is indirect evidence that the two paths agree.
- v1-v3 scripts behind Sections 2-11 (curves certificates, Batch 28/29, Lean, Sage) were checked for existence only, not re-run.
- `scripts/n2_*` other than n2_jacobi, `review/rv_symbolic.py`, `n1_*` were not re-run (byte-identical to v4, which the V4 report re-ran).
- No visual inspection of the PDF pages. Consistency was checked from the tex source, the aux labels and the build log.
- The GitHub `erdos_sidon/v5` folder cited in the paper was not inspected (no internet use).
- Mathematical correctness of Lemma 1's proof and the Corollary is the math referee's scope. Numerically, both pass here.
