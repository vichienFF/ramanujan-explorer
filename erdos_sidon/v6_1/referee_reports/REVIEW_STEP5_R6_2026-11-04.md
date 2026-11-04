## Referee 6 (Sonnet, 2026-11-04) on the explicit step 5: no FATAL/SERIOUS; MINOR a-d applied here
Referee re-derived the c = 1 weights, checked all three closed forms against its own GF(p^n) brute force at q = 49, 121, 169, 289, 343, 361, 529, 841,
1331, 1369, 2197 (all equal; SPEC = target), and confirmed the total.py logic is a valid proof given the class formulas; q = 125 (char 5) fails as expected.
(a) rep class: the pair (r1, r2) may itself be singular (Y(Y^2-Y-1) = 0 for t1 + t2 = 0; (Y^2-3Y+1)(Y^2+Y-1)(Y^2+Y+1) = 0 for t2 = +-i t1). This does
    not change C(Y): with r = 3 a singular pair contributes (r-2) = 1 and a nonsingular pair with D4 = 0 contributes 1 + 0 = 1 as well.
(b) Lemma (general form of the chi(-D4) statements) [SYM, verified by us 11-04]: for a member with c != 1 and a pair (t1, t2) of its roots, -D4(t1+t2, t1 t2)
    equals (1/4) disc of the residual quadratic (quotient of the member's numerator polynomial by (t-t1)(t-t2)), so chi(-D4) = chi(disc residual):
    1 if the other two roots are distinct and in F_q, 0 if they coincide, -1 if they are conjugate. This covers the per-class statements for every q = p^n.
(c) Docstring of p4_step5_rep.py corrected (leading coefficient of Q is 3Y^2-3Y+1; the code always divided symbolically).
(d) p = 7, 13: for beta in F_{p^2}, chi_{p^n}(beta) = chi_{p^2}(beta) if n/2 is odd and 1 if n/2 is even, so the classes are n odd, n = 2 mod 4, n = 0 mod 4
    (not 'n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6]'). Since the q-coefficient is exactly -1, one point per class fixes the constant: 7 | 49 | 2401 and 13 | 169 | 28561 (all verified).
    Referee also evaluated the set formulas for n = 2, 4, 6, 8 at p = 7, 13, 11: SPEC = -q + target in all 12 cases.
ERRATUM to record for the next paper version: V6 (Section 13, step (5)) says the data depend 'only on n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6]' for p = 7, 13; correct is n odd / n = 2 mod 4 /
n = 0 mod 4; the verification points used (7, 49, 2401; 13, 169, 28561) cover all three classes, so the theorem is unaffected.

## Note on q = 28561 (2026-11-04, v6.1 repro referee item B)
For p = 13, n = 0 mod 4 the evidence at q = 28561 is: (N3) by exact counting (../v6/scripts/v6_pp.json) and the class formulas evaluated over F_{13^4} (scripts/p4_step5_p713.out, EQUAL to the target). A brute-force evaluation of SPEC itself at 13^4 was not run (too slow locally).
