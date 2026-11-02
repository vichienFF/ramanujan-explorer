# Adversarial referee report: C9 note, Version 5 (mathematics)

File reviewed: `D:/Research_FlyBrain/math_explorer/paper_c9/c9_note_v5.tex` (488 lines), compared with `c9_note_v4.tex` and the edit list `build_v5.py`.
Reports checked against: `REVIEW_C9_V4_MATH_2026-11-01.md`, `REVIEW_C9_V4_REPRO_2026-11-01.md`.
Reviewer: AI referee (Claude), 2026-11-02. All numbers below come from my own code, written from scratch and independent of the project scripts:
`C:\Users\user\AppData\Local\Temp\claude\C--Users-user\c53ce00a-9167-44da-bdf0-c9332628bf16\scratchpad\ref5\` (`fld.py`, `lem.py`, `cor.py`, `eta.py`).
No project file was modified.

## Verdict
No CRITICAL or MAJOR problem. The new Lemma (lem:I3) is true, and its written proof is correct. It is terse in three places (see m1-m3), but it has no real gap.
The new Corollary is correct and agrees with Section 6. One sentence after the Corollary overstates what it gives (m4).
There is one new typesetting bug (m5). One line in "Changes in Version 5" is slightly inconsistent (m6).
Every MAJOR item of both Version 4 reports has been fixed. Several MINOR presentation items of the reproducibility report were dropped silently (see "Items fixed").

## What I recomputed
| Claim | My check | Result |
|---|---|---|
| Lemma lem:I3: P(l)-(q-2)^2 = sum_mu (I_l(mu))_3 | P by brute force over F_{q^3} (all y, all c, d determined by solving); third moment from S = logs of span{1,t} mod m. q = 5,7,11,13,17,19,23: l in {1,2,-1,3,-3,-2,4,5,7,q,q+2,1/2} plus 4 random units each (non-units skipped). q = 29, 31: l in {-2,4,5,6,10} | all units match (about 120 cases) |
| Lemma: y^l does not depend on the integer representative of l | P(l) = P(l+m), same cases | pass |
| Lemma needs l to be a unit | non-units q=7,l=3; q=13,l=3; q=11,l=7 | identity FAILS (18 vs 54; 108 vs 180; 54 vs 234), so the unit condition is essential |
| Controls: l=1 gives q^3-q; l=2,-1 give 0 | same runs | pass (e.g. 120, 336, 1320 for q=5,7,11) |
| Corollary: sum_{rho!=0,1} N(rho)^2 = sum_lambda (P(lambda)-(q-2)^2), m prime | N(rho) from all ordered distinct triples; P over all m-1 units. q=5 (m=31), q=17 (m=307) | 720 = 720; 91584 = 91584 |
| Multipliers 1,q,q^2 contribute 3(n)_3 (Section 6) | sum of P(lambda)-(q-2)^2 over lambda in {1,q,q^2} | 360 = 3(n)_3 (q=5); 14688 = 3(n)_3 (q=17) |
| sum(N-E)^2 = sum N^2 - (n)_3^2/(m-2) (the link to Conjecture 1) | q=5, 17 | pass |
| Thm 3(a) P(2)=P(-1)=(q-2)^2; (b) P(3)=(q-2)(2q-1) for q=2 mod 3; (c) P(-2)=(q-2)(2q-1)+b_q | q = 5..23 (7 primes) | all pass |
| Restated values (q-2)(q+1) at 3 and (q-2)(q+1)+b_q at -2 | from the third-moment side directly | pass (e.g. q=17: 270 = 15*18) |
| Observation P(4)=P(-2) | q = 71, 73, 79 (the range the V4 referee could not finish) | pass; with V4 report, now 5..79 fully confirmed |
| b_q = a_q(eta(2t)^3 eta(6t)^3) | eta product expanded to q^399; all 76 primes 5..397 | pass; a_p = 0 for p = 2 mod 3 |
| LMFDB label 12.3.c.a | weight (3+3)/2 = 3; level 12 from the eta-quotient rule; character from -(2^3 6^3) = -3*24^2, i.e. chi_{-3}; expansion q - 3q^3 + 2q^7 + 9q^9 - 22q^13 | consistent with 12.3.c.a; I did not open LMFDB to confirm the label letter |
| Proof of (b), case c=d | by hand: c(3y^2-3y+1)-1, degree 2 since q>=5 | correct |
| Prop. gal proof (V5 wording) | by hand | conclusion correct; labels of the two counts are swapped (m7) |

## CRITICAL
None.

## MAJOR
None.

## MINOR

### m1. Lemma proof: the "normalise the first point to 1" step is a double count, not a normalisation
The proof says the count is the same for every line, and then "normalising the first point to 1". Moving the first point to 1 moves the line S to another line. The step that is really used is this:
m·T = #{ordered distinct collinear triples whose l-th powers are collinear}, and each of the m possible first points contributes the same number U, by multiplicative invariance. So T = U.
This is correct, but it should be written in one sentence.

### m2. Lemma proof: the representative step is asserted without its one-line reason
"There are unique representatives with 1 = y + (1-y)" is true. The reason: if x2 = [y2] and x3 = [a + b y2] with a, b nonzero, then 1, y2 are F_q-independent. This forces y = -(b/a) y2. Also, every y in K\F_q gives such a pair, and different y give different pairs. So the map y -> ([y],[1-y]) is a bijection from K\F_q onto the pairs. The proof should say "bijection", because the count depends on it.

### m3. Lemma proof: say where the unit condition is used
The unit condition is used once. It makes x -> x^l injective on points. That gives three things: |lS| = q+1; the points 1, y^l, (1-y)^l are distinct; and so (c,d) is unique and both c and d are nonzero. The proof says "maps distinct points to distinct points" but does not say this needs l to be a unit. My runs show that the identity fails for non-units (table above), so the dependence is real. Also, the proof never uses that q is prime. The lemma holds for every prime power q. You may say so.

### m4. Sentence after the Corollary overstates
"So Conjecture 1, and with it the order-3 case of the hypothesis of Proposition 1, is a statement about the average of P(lambda)."
- For Conjecture 1 this is right. sum(N-E)^2 = sum N^2 - (n)_3^2/(m-2), and the Corollary rewrites sum N^2 as a sum of P.
- For the order-3 hypothesis (R_3 -> 0) it is not right. R_3 is a weighted linear statistic of the N(rho) (Section 3). It is not determined by sum N^2. The variance bound is a *sufficient* condition for R_3 -> 0, through the conditional Proposition of Section 8. It is not equivalent.
Fix: "...and hence a sufficient condition for the order-3 case...". The abstract and "What remains" use "reduces to", which is acceptable in the sufficient sense.
Suggestion: state the precision needed. Conjecture 1 says that the average of P(lambda)-(q-2)^2 over the m-1 units equals (n)_3^2/((m-1)(m-2)) + 3(n)_3/(m-1) + o(q). That is a quantity of size q^2, known to o(q). R_3 -> 0 needs only o(q^2/log q).
Small point: "Theorem 3 evaluates four of the roughly q^2 terms" understates. With P(l)=P(1/l)=P(ql), each value covers an orbit of up to 6 units.

### m5. New typesetting bug in Section 1 (line 45)
The source reads ``registered and ``blind mean ...; the closing quotes are missing, so the PDF shows "registered and "blind. Cause: in `build_v5.py` the text `''` sits inside a single-quoted raw Python string. Python therefore reads it as the end of one string literal followed by the start of another, and the quotes disappear. Fix the build string (use a double-quoted raw string) and rebuild.

### m6. "Changes in Version 5" says "no mathematical error was found"
Item (4) in the same paragraph corrects a false sentence in the released proof of Theorem 3(c) (the choice of associate). Write "no error in any stated result was found" instead.

### m7. Proof of Proposition gal: the two counts are attributed the wrong way round
The pair set {(y,y'): L(y)=lL(y'), L(1-y)=lL(1-y')} has P(l) elements when y' is the free variable, because then y = c y'^l. It has P(l^{-1}) elements when y is free. The text writes "= m^2 P(l^{-1})" and then "with y instead of y' as the free variable gives P(l^{-1}) = P(l)". This assigns the counts the wrong way round. The conclusion is symmetric, so nothing breaks, but swap y and y' in the sentence.

### m8. Novelty search should be redone in the new form
Version 5 still says "we found no prior statement of Theorem 3(b),(c)" (search of 30 October). That search was made for the P(l) form. After the Lemma, (b) and (c) are statements about |D ∩ (tD+s)| for a planar difference set D and t = 3, -2. The difference-set literature on intersections of D with its dilates (beyond the conic and oval case of [JV, Pi]) should be searched under that form before novelty is claimed. Otherwise state the date and the form searched.

### m9. Minor wording
- Section 12 still opens with "q an odd prime". The Lemma and Proposition gal do not need q prime. This is harmless.
- The b_q sentence calls b_q = a_q "the standard Hecke-character description". This is true, but the sign and normalisation of the Hecke character are not given. Since it is "not used below", this is fine.

## Items fixed (Version 4 reports)
**Math report V4**
- M1 (P(l) is the per-dilation third moment): FIXED. Lemma added. Theorem 3 restated. (a) marked as the conic fact. Corollary added. Novelty sentence amended. Remaining nuance: m4, m8.
- M2 ("remaining step ... we isolate"): FIXED in the abstract and in "What remains". The residual overstatement is m4.
- m1 (read Ono, cite a theorem number, state the specialised identity): STILL OPEN. It is disclosed: Limitations says the full text of Ono was not checked, and BK is labelled a preprint. The specialised identity (phi,phi,phi;eps,eps | 4) is still not written in the paper.
- m2: FIXED (but see m7). m3: FIXED. m4: FIXED (LMFDB cited). m5: FIXED. m6: FIXED (hedged). m7: FIXED. m9: FIXED (table caption). m10: FIXED. I also confirmed the range 71..79.
- m8 (q=125 borderline, 1.101): NOT ADDRESSED. The caption states the 10% rule but does not say that q=125 misses by 0.001. Silently dropped (cosmetic).

**Reproducibility report V4**
- C1 (`run_orb.py` not released): FIXED as stated. `release_v5/kaggle/run_orb.py` and `regress_run_orb.py` exist. I did not run them.
- M1 (associate sentence): FIXED in `release_v5/N2_PROOF.md` l.64-67 and in `scripts/n2_jacobi.py`.
- M2: FIXED (Verification paragraph). M3: FIXED (Section 1, abstract, Sec. 7, README lists the Batch 28 amendments). M4: FIXED. M5: FIXED.
- M6: MOSTLY FIXED. There is now a claim-to-script table and `requirements.txt`. `build_v5.py` needs `../v4/c9_note_v4.tex`, which the README says.
- Minor 1 (CONTROL lines, non-zero exit): PARTLY. The README claim is gone. But `n1_char.py`, `n1_conic.py`, `n1_cubic.py` and `n1_cubic_proof.py` still print no CONTROL line, and none of them, nor `n2_types.py`, exits non-zero on failure.
- Minor 2: FIXED. Minor 3: FIXED for `n2_jacobi.py` (now skips q = 2 mod 3). I did not check the `n2_types` control, the stale comment or the docstring. Minor 4, 5, 6, 7, 8, 9, 10, 16: FIXED.
- Minor 11 (hard-coded section references): PARTLY. "Sections 7--8" is fixed. Hard-coded "Sections~4--8" and others remain (l.93).
- **Silently dropped** (not fixed and not marked open):
  - Minor 12: no notation table, and the overloads remain (L, phi, psi, C, E, S, N).
  - Minor 13: LaTeX overfull boxes remain (43.9 pt and 12.4 pt in Prop. 1, 18.6 pt in Data and code, plus a new 5.6 pt at l.70), and so do the two hyperref warnings (`c9_note_v5.log`).
  - Minor 14: the date conflict. The title page still says "Version 4: 31 October 2026"; the repro report says it was published on 30 Oct.
  - Minor 15 (partly): [Gr] has no URL, [IR] has no proposition numbers, [Guy] is still cited for the prize but marked not checked. The BK journal-version caveat was added.
  - Item 5.3/5.4: splitting the paper and shortening the abstract. These are editorial and optional.

## Not checked
- I did not run `run_orb.py` or its regression test, nor any release script.
- The claim that the two Batch 28 amendments predate all computation.
- Theorem curve (d) certificates, the Sage identities of Theorem res, Sections 2-5 and 7-8 numerics, and Tables 1-2 (unchanged from V4, except one caption number).
- The label letter of LMFDB 12.3.c.a, checked online. Only the q-expansion, weight, level and character were checked offline.
- The full text of Ono (1998) and of Barman-Kalita.
- The literature for intersections of a difference set with its dilates (m8).
