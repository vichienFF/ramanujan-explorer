# Adversarial referee report: C9 note, Version 4 (Zenodo 10.5281/zenodo.23809651)

File reviewed: `D:/Research_FlyBrain/math_explorer/paper_c9/c9_note_v4.tex` (451 lines). Reviewer: AI referee (Claude), 2026-11-01.
All checks were done with my own code, independent of the project scripts. Scratch code is in
`C:\Users\user\AppData\Local\Temp\claude\C--Users-user\c53ce00a-9167-44da-bdf0-c9332628bf16\scratchpad\ref\`
(`fld.py`, `p1.py`, `p2.py`, `cl.py`, `greene.py`, `eta.py`, `res.py`, `var.py`, `mu.py`, `link.py`).

## Verdict
I found **no CRITICAL mathematical error**. Every theorem and every numerical claim I re-checked is correct.
The main problems are about presentation and novelty:
- The paper misses an equivalence. P(l) is the per-dilate third moment of Section 6, so Theorem 2(a) restates a fact the paper already proved.
- The "remaining step" framing overclaims.
- Step 7 relies on a preprint.

## Independent verification (what was recomputed)
| Claim (tex line) | My check | Result |
|---|---|---|
| Prop. gal: C(l)=m^2P(l)-((q-1)m-1)^2-(m-1) (l.327) | Jacobi sums J[a,b] over F_{q^3}, computed by 2-D FFT; q=5 (l=2,-1,3,-2,4,5), q=7 (l=2,-1,-2,4,5) | exact match in all 11 cases |
| Thm gal (a) P(2)=P(-1)=(q-2)^2 | brute force over F_{q^3}, 17 primes 5..67 | all pass |
| Thm gal (b) P(3)=(q-2)(2q-1), q≡2 (3) | q=5,11,17,23,29,41,47 | all pass |
| Thm gal (c) P(-2)=(q-2)(2q-1)+b_q | 17 primes 5..67 (both residue classes) | all pass |
| P(2^{-1})=P(2), P(2q)=P(2) | 13 primes | pass |
| Obs. P(4)=P(-2) (l.398) | primes 5..67 (16 of the 20 claimed; the 71..79 run did not finish) | pass |
| Step 4/7: q^2·3F2(φ,φ,φ;ε,ε\|4)=φ(-1)G(4)=q+b_q | Greene's definition coded directly, all primes 5..109 | pass; imaginary part 0 |
| Step 7: J(φχ3,χ̄3)=χ3(2)·conj J(χ3,χ3); 2Re J(φχ3,χ̄3)=±2x | all q≡1 (3), 7..109 | pass (the sign of ±2x varies, so only its square is used, correctly) |
| T=Σφ((x²-1)(z²-1)(x²+1-2z)) = q+1+b_q | primes 5..59 | pass |
| b_q = a_q(η(2τ)^3η(6τ)^3) | all primes 5..397 | pass, including signs |
| Thm res: r partners per non-fixed point, 0 per fixed point, e by r mod 3 | brute force: q=8 (m prime), 27 (m prime), 64, 125 | pass: N(ρ1)=18, 81, 252, 630 = r(q+1-e) |
| Prop orb 3k∣N(ρ) | q=9, 49, 121, 125, 128 | pass |
| Table pp (ratio, ratio/3k, good ρ) | q=121, 125, 128 (table) and q=9, 49 (caption) | 6.13/1.022/2975; 9.91/1.101/14059; 20.30/0.967/11725; 0.196; 0.693, all as printed |
| Table res row q=125: Δ=0.089, observed 0.101, top-6 M/μ=4.91 | recomputed (μ formula vs empirical μ agree to 1e-4) | pass |
| Thm curve (d) orbit counts: 6 orbits of height ≤4 (5 + forbidden); 22 orbits of height ≤8; 18 settled + 4 listed | enumeration of S3-orbits | pass |
| Sec 3: Var_s Z=qℓ(m-ℓ)/m², R_2=0; ΣA=ℓ(ℓ-1)(ℓ-2)/(m-1); R_3 formula; forbidden contribution -3/(2Cq) | derived by hand | correct |
| Prop red (Bonferroni, N=m-ℓ, excess (C+1)/2) | derived by hand | correct |
| Prop orb proof (order of p is 3k, free action) | by hand | correct |
| Shakan bound 2p/\|A\|-2 | arXiv abstract | correct |
| BK Thm 1.7 hypotheses | library text (Greek letters garbled), lines 220-236 | order of S ≠ 1,3,4, so S=φ is allowed. With S=φ every parameter reduces to (φ,φ,φ;ε,ε), whether the printed "−" is a minus sign or an inverse bar. The prefactor J(S^{-1},S^{-1})/J(S^{-3},S)=1 and S(-16/27)=φ(-3)=1 for q≡1. My numerics confirm the specialised formula B²−1/q. |

---

## MAJOR

### M1. P(l) is the per-dilate third moment of Section 6; Theorem 2(a) repeats a Version 2 result, and the novelty claim needs correcting
**Where:** Sec. `sec:gal` (l.316-337), Thm `thm:gal`(a) (l.343, proof l.349-352), Sec. lim (l.416: "we found no prior statement of Theorem gal or of Proposition gal"), Sec. 6 (l.143-148).

**What is wrong:** The following identity holds:

  P(l) − (q−2)² = Σ_μ (I_l(μ))_3,  where I_l(μ)=|S∩(lS+μ)|.

Proof sketch: (q−2)² counts y∈F_q. Each y∉F_q matches exactly one ordered pair of points (y, 1−y) collinear with 1 in PG(2,q), and the pair has at most one (c,d). The Singer cycle commutes with x↦x^l, so normalising one point to 1 costs a factor m on both sides.

Verified numerically for q=11, 13, 17 and l ∈ {2,−1,−2,4,5,q,3 (q≡2), 7}. Every case with l a unit matches. The one mismatch (q=11, l=7) has 7∣m, where P is not defined.

Consequences:
1. **Theorem 2(a) is the same statement as the Bézout/conic fact of Sec. 6.** Sec. 6 (l.145-146, already in V2) states "(I_λ)_3=0" for λ=−1, and the same holds for λ=2. It is also the classical arc/oval fact [JV, Pi]. Presenting (a) as a new exact evaluation, and claiming no prior statement, is inaccurate.
2. Theorem 2(b) and 2(c) are exact values of the per-λ third moment Σ_μ(I_λ)_3 at λ=3 and λ=−2:
   - (q−2)(q+1) at λ=3;
   - (q−2)(q+1)+b_q at λ=−2.

   This is the natural statement, and it links directly to Sec. 7 (the per-λ errors of size about 4.2q).
3. Combined with the identity of Sec. 6, it gives Σ_ρ N(ρ)² = Σ_λ [P(λ) − (q−2)²]. Hence Conjecture 1 (the variance law) is exactly a statement about the average of P over all λ. This is the precise meaning of "Correlations of this kind are the missing input" (l.321-322). As written, that sentence is asserted without justification.

**Fix:**
- Add the identity as a Lemma.
- Restate Theorem 2 in terms of Σ_μ(I_λ(μ))_3.
- Mark (a) as equivalent to Sec. 6 and [JV, Pi].
- Replace the "missing input" sentence with the exact relation Σ_ρN(ρ)² = Σ_λ(P(λ)−(q−2)²).
- Amend the novelty sentence in Sec. lim.

### M2. Overclaim: "the remaining step ... is a uniform estimate, which we isolate"
**Where:** Abstract l.25-26; Sec. `sec:rem` l.405-408.

**What is wrong:** Proposition `prop:red` needs R_k→0 for **every** fixed k and **every** C, which is essentially a full Poisson limit law for the window counts. The paper itself says that for k≥4 "a different decomposition is needed" (l.406-407). So the missing estimate is formulated only for k=3, through the variance. Section `sec:gal` evaluates 4 of the roughly q² dilations.

Calling this "the remaining step", in the singular, and saying "we isolate" it overstates how close the argument is to the Erdős question. The conditional is correctly labelled, and "the Erdős question remains open" is stated. The problem is the framing, not a false theorem.

**Fix:** Say instead: "a negative answer would follow from Poisson convergence of all fixed-order factorial moments. For k=3 this reduces to a variance bound (Conj. 1, equivalently an average of P(λ) over λ). For k≥4 we do not have such a reduction."

---

## MINOR

### m1. Step 7 rests on a preprint, although a published source exists
**Where:** l.375-378, l.416. The paper cites Barman–Kalita arXiv:1208.0495 (Thm 1.7) and says Ono's full text was not read. The q-prime case of the evaluation 3F2(4) is Ono, Trans. AMS 350 (1998).
- Read Ono and cite his theorem number.
- Check whether BK appeared in a journal (I could not verify this).
- Optionally, since the extracted BK text is garbled, state the specialised identity (φ,φ,φ;ε,ε|4) explicitly with its normalisation, as N2_PROOF.md does.

The identity itself is correct: I verified it numerically for all primes 5..109.

### m2. Proof of Prop. `prop:gal`: the "swap" wording is unclear
**Where:** l.330-331. The pair set is counted by P(l) when y′ is the free variable, and by P(l⁻¹) when y is. This is one set counted two ways, not a swap. Also note that y^l depends on the integer representative of l only up to an F_q^× factor, which is absorbed into (c,d). Make both points explicit.

### m3. Proof of (b): the case c=d is omitted
**Where:** l.355. The factorisation (c−d)g(y) needs c≠d. When c=d the polynomial has degree 2 and contributes nothing. Add one sentence.

### m4. b_q as a modular coefficient is a theorem, not just a numerical fact
**Where:** l.26, l.341, l.387. η(2τ)³η(6τ)³ is the weight-3 CM newform of level 12. Its coefficients 2Re(π²) = 4x²−2q follow from the Hecke character of Q(√−3). Cite this (e.g. LMFDB 12.3.c.a, or Schütt's work on CM newforms) instead of "numerically". I verified it for all primes below 400.

### m5. Section hypotheses are inconsistent
**Where:** l.317 vs l.340. The section says "q an odd prime" while Thm `thm:gal` needs q≥5. State which hypothesis applies where. Also say explicitly that l=3 (and l=−3) is a unit only for q≡2 (mod 3).

### m6. The geometric explanation is asserted, not proved
**Where:** l.391-394. The facts are consistent:
- Beauville's Γ1(6) pencil has fibres I6 I3 I2 I1.
- The quadratic base change gives 3I6+3I2 with Euler number 24.
- disc diag(2,6) = 12 corresponds to Q(√−3).

But the link "level sets of Tr(α)Tr(α⁻¹) form this pencil, hence b_q" is only asserted. It is labelled "not used", which is fine; add "heuristic" or give a reference.

### m7. "Blind" and "registered" labels are self-attested
**Where:** abstract l.21-25, Table `tab:res` (q=12167 "Δ registered (blind)"). The paper discloses that registration times are self-attested (l.290). Repeat that caveat in the abstract, or drop the word "blind" there.

### m8. Table `tab:pp`: q=125 is a borderline miss
ratio/3k = 1.1013 (I recomputed this exactly). Its classification as a "miss" depends on the third decimal place. State the exact rule (|ratio/3k − 1| ≤ 0.10).

### m9. Theorem `thm:res` versus Table `tab:res` for composite m
For composite m the table's M uses the unit-restricted count; for example q=125 gives N(ρ1)=576. The theorem's count r(q+1−e)=630 counts all triples. Both are correct, but note the difference: the table's M/μ≈r is approximate for this reason, not only because of noise.

### m10. Observation l.398 coverage
I confirmed P(4)=P(−2) on primes 5..67; my run for 71..79 did not finish. The phrase "not explained by such a map" is fine. In the light of M1, consider restating it as Σ_μ(I_4)_3 = Σ_μ(I_{−2})_3.

---

## Items checked and found correct (no action needed)
- Prop. Sec. 3: the variance formula, R_2=0, the R_3 decomposition and ΣA.
- Prop `prop:red`: Bonferroni step, N=m−ℓ, and the excess (C+1)/2+O(1/q).
- Thm `thm:curve`: (b) diagonal for exponents (−2,1,1); (c) Weil and Aubry–Perret logic; (d) orbit bookkeeping (5, 17, 22, 18).
- Prop `prop:orb`: the order argument and the free action.
- Thm `thm:res`: brute force for q=8, 27, 64, 125, and the formula ρ0=r⁴+r⁻⁴=(r+1)r⁴.
- Δ formula and Table `tab:res` row q=125.
- Table `tab:pp`: rows 121, 125, 128 and caption values for q=9, 49.
- Abstract: "within 0.8%" is consistent with the range [2.979, 3.019]; "21 of 23" is consistent with the table.
- Shakan citation.
- The paper does not claim to solve the Erdős problem: it is stated as open (l.26) and the reduction is labelled conditional (l.412).

## Not checked
- The Sage identities in Thm `thm:res`(ii): I used brute force instead.
- Theorem `thm:curve`(d) certificates.
- Sec. 2 numbers (Bose gaps, Zhang control).
- Sec. 3-5 Monte Carlo and blind-test numbers.
- The Hulek–Schütt Example 3.1 statement.
- The full Ono 1998 paper.
