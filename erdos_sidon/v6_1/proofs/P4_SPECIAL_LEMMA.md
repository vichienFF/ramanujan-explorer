# P4 last piece: the special-class term by structural lemma + finite verification (draft 2026-11-04, for referee)

Labels: [HAND] derived by hand, [SYM] sympy/Sage identity, [EXACT] exact computer check, [INF] inference to be scrutinised.

## Setting
N3(q) = q^2 + phi(-1)(S_a+S_b) + E(q) (Step 4w). All parts of E are proved [HAND] except the
special-class term SPEC(q) = sum_{X in {c=1, c+d=0, rep}} (N3'[X] - M[X]) (Steps 4zc-4zh), and the target is

  SPEC(q) = -q + 10 + 5 phi(-1) + 6 phi(-2) + 2 phi(-3) - 2 chi(-7)        (*)

[EXACT: equivalent to the N3 formula, verified at all 2259 primes 7..19999 (43 + 623 + 1593; corrected 11-04, E97) and at q = 49, 121, 125, 169, 343, 2197, 2401, 28561, 3125, 15625].

## Lemma (structure)
Let L = Q(i, sqrt2, sqrt-3, sqrt-7), G = Gal(L/Q) = (Z/2)^4. For every prime power q = p^n with p >= 7 there are integers
A(tau), B(tau), depending only on tau = (Frobenius of q acting on the finite exceptional sets below), with SPEC(q) = A(tau) q + B(tau).
For p not in {7, 13}, tau is determined by sigma_q = Frob_p^n in G; for p in {7, 13}, by n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6].

### Proof sketch
1. **Pairs.** SPEC is a sum over ordered pairs (t1, t2) of distinct F_q-roots (t = y/(1-y)) of members (c, d) in a special class
   (plus, for c = 1, the pairs containing the root y = 1), of an integer weight w = act - main, where act = number of further
   F_q-roots and main = 1 + chi(-D4(t1+t2, t1 t2)); singular pairs t1^4 = t2^4 are excluded (already counted, Step 4za).
2. **Each class is a conic** [SYM, Steps 4zf, 4zm part 3]:
   - c = 1: pairs lie on v = u^2 + 3u/2 + 1 (u = t1+t2, v = t1 t2); pairs with sum u number 1 + chi(-3(u+1)^2 - 1).
   - c + d = 0: with s = 2y - 1 the members are g(s) = s(s^2+1)/2 = 1/c; pairs lie on the conic s1^2 + s1 s2 + s2^2 = -1.
   - rep: members (y0^-3, (1-y0)^-3); partner roots exist iff the residual discriminant -8 y0^2 (y0-1)^2 (y0^2-y0+1)
     is a square, i.e. on the conic w^2 = -2(y0^2 - y0 + 1).
   All three conics are smooth over F_p for p >= 5 (their discriminants involve only 2 and 3).
3. **Weights are constant off a finite set.** On each conic the third/fourth roots are rational functions of the point
   (c = 1: t3 = -3/2 - u; c+d=0: residual roots {-1, t3}; rep: {t1, t3}), and -D4 restricted to the conic is a constant times
   a square [SYM: c = 1: 4u^2(u+1)^2(u+2)^2]. Hence w equals a fixed integer w_X except on a finite exceptional set Z_X
   (coincidences t3 in {t1, t2, -1}, zeros of the square factor, members lying in two classes, points at infinity).
4. **Counting.** A smooth conic over F_q has q + 1 points, so the class-X sum is w_X (q + 1 - #Inf_X(F_q) - #Z_X(F_q)) + sum over
   z in Z_X(F_q) of w(z). #Inf_X(F_q), #Z_X(F_q) and the w(z)-sum are permutation-character values of Frobenius on finite sets
   of algebraic points.
5. **Field of definition.** Every exceptional point is a root of one of: t+1, 2t+1, t, 2t+3, t^2+1, t^2+2t+2, 2t^2+2t+1,
   2t^2+t+1, 3t^2+3t+1 (c = 1, p4_4zm_c1.py), s - 1, s^2+s+2, 3s^2+1 (c + d = 0), y0^2-y0+1, y0^3-1, 3y0^2-3y0+1 (rep) [INF:
   list to be completed in the final write-up]. All splitting fields lie in L; pairwise collisions mod p occur only for
   p in {2, 3, 5, 7, 13} (resultants, p4_4zm_c1.py). For p not in {2,3,5,7,13} the exceptional configuration is the reduction
   of the characteristic-0 one, so its Frobenius data depend only on sigma_q.
   For p = 7, 13 the configuration is a fixed degenerate one over F_p whose points lie in F_{p^2} (L is multiquadratic), so the
   data depend only on n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6].  QED (sketch)

## Finite verification
(*) has the same shape: right side R(sigma) q + S(sigma) with phi(-1), phi(-2), phi(-3), chi(-7) characters of G.
For fixed tau, A(tau) q + B(tau) = R q + S at two distinct q forces equality for all q with that tau.
- p not in {2,3,5,7,13}: all 16 elements of G occur among verified primes with >= 2 primes each
  (minimum class = identity: 193, 337, 457, 673; p4_n3_classcover.py) [EXACT]; prime powers have sigma = Frob_p^n in G -> covered.
- p = 7: n odd {7, 343}, n even {49, 2401} [EXACT]. p = 13: n odd {13, 2197}, n even {169, 28561} [EXACT].
Hence (*) and the N3 formula hold for all q = p^n, p >= 7, given the Lemma.

## Referee 4 (Sonnet, 2026-11-04): no FATAL; valid proof for p >= 7 once the items below are written out
Scripts archived in referee4/ (perclass.py, fit.py, dev.py, bad2.py, sq*.py, cd0.py).
- **Per-class linearity [EXACT, referee]**: each of N3'[X]-M[X] is exactly A(sigma) q + B(sigma) on all 16 classes (primes 11..691, 4-5+ per class),
  A = +2 (c=1), -1 (c+d=0), -2 (rep); no hidden character (5, 11, 13, ...).
- **Q-rational square roots (step 3) [SYM]**: c=1: -D4 = (2u(u+1)(u+2))^2; c+d=0: -D4 = [4(s1^3+6s1+5s2)/((1-s1)^2(1-s2)^2)]^2 on
  s1^2+s1s2+s2^2 = -1 (re-verified 11-04 by us, sympy remainder 0); rep: -D4 = ((alpha + beta w')/den)^2 on w'^2 = -2(y0^2-y0+1),
  alpha = (2y0-1)(3y0^4-6y0^3+6y0^2-3y0+2), beta = 3y0^4-6y0^3+9y0^2-6y0+1 (referee sq3.py; to re-verify in the write-up).
- **Complete exceptional lists in unordered-pair coordinates (replaces the step-5 list)**:
  c=1 (u = t1+t2): 3u^2+6u+4, 2u^2+5u+4, 2u+1, 4u^2+8u+5, u+1, 12u^2+24u+13, u, u+2.
  c+d=0 (sigma = s1+s2): 3s^2+4 (diagonal), 3s^2+1, s^2-s+2, s+1, s^2+1, s, s-2, s+2 (incl. e=0 pairs, singular pairs, diagonal).
  rep (y0): y0, y0-1 (invalid members), y0^2-y0+1, y0^2+y0+1, 3y0^2-3y0+1, singular 2y0^2-2y0+1, y0^2+1, y0^2-2y0+2.
  All roots, and the full root sets of their members, lie in L. Discriminants + pairwise resultants -> bad primes {2,3,5,7,13}.
  Generic weights: +2 (c=1; y=1 pairs = same conic points doubled), -1 (c+d=0), -2(1+chi(disc)) (rep). Affine conic counts
  q - chi(-3), q - chi(-3), q - chi(-2). Every numerical deviation (75 primes 7..397) lies in these lists. Overlaps only (1,-1), y0^3=1, 3y0^2-3y0+1;
  only double-counted member y0^2-y0+1 (c=d).
- **p = 7, 13 genuinely degenerate per class** (e.g. p=13 c=1 gives 8 vs generic 4): only the total matches, so the direct checks at
  7, 343, 49, 2401, 13, 2197, 169, 28561 are ESSENTIAL. Exceptional sets are zero-dimensional schemes over Z[1/6]; their reductions are the
  char-p exceptional points, defined over F_{p^2} (L multiquadratic) -> data depend on n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6] only.
- Member roots at exceptional points lie in L (r and w(z) fixed by char-0 data); rep members have no triple root (1/(y0(1-y0)) != 0).
- Remaining write-up: table of the lists with defining conditions; resultant table; re-verify the rep identity; char 5 separately;
  note that the non-special parts of E are proved uniformly incl. p = 7, 13 (hand proofs are field-uniform; checked numerically at 49, 169).

## Exceptional-point table (generated by p4_exc_table.py, 2026-11-04; control PASS)
| class (coordinate) | squarefree discriminants of the exceptional polynomials | collision / leading-coefficient primes |
|---|---|---|
| c=1 (u) | -7, -3, -1 | 2, 3, 5, 7, 13 |
| c+d=0 (sigma) | -7, -3, -1 | 2, 3, 5, 7, 13 |
| rep (y0) | -3, -1 (plus -2 from the conic w^2 = -2(y0^2-y0+1)) | 2, 3, 5, 7, 13 |
All fields lie in L = Q(i, sqrt2, sqrt-3, sqrt-7); the only primes >= 7 where exceptional points collide are 7 and 13 (handled by direct
checks at n odd/even). The rep-class square-root identity is confirmed by p4_rep_sqrt.py (norm is a square; zeros = referee's singular points).

## What a referee must check
(a) completeness of Z_X and Inf_X (step 5 list) and that no exceptional point needs a field outside L;
(b) smoothness of the three conics for p >= 7 and the 'constant weight off Z_X' claim (step 3), including the y = 1 pairs
    for c = 1 and the class-priority overlaps;
(c) that the data really depend only on sigma (for p in {7, 13} only on n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6]);
(d) the finite-verification logic.
Char 5 (N3 formula verified at 5, 25, 125, 3125, 15625) is outside this lemma (p >= 7) and needs its own argument.

## Class c = 1 in full (2026-11-04; replaces the sketch for this class) [HAND + SYM + EXACT: p4_step5_c1.py]
Members (c, d) = (1, d), d in F_q^*, char >= 5. y = 1 is a root of y^4 + d(1-y)^4 = 1 for every d; the other roots are t = y/(1-y), t != -1, with
g(t) := (1+t)^4 - t^4 = 4t^3 + 6t^2 + 4t + 1 = d. For a member, SPEC-contribution = sum over ordered pairs of distinct roots of: (r-2) for pairs
containing y = 1; 0 for singular finite pairs (a^4 = b^4); (r-2) - 1 - chi(-D4(a+b, ab)) for the other finite pairs (r = number of roots).
(i) Distinct a, b with g(a) = g(b) <-> 4(a^2+ab+b^2) + 6(a+b) + 4 = 0 <-> v = ab = u^2 + 3u/2 + 1, u = a+b. For given u the ordered pairs number
    1 + chi(Delta(u)) when Delta(u) := u^2 - 4v = -(3u^2+6u+4) != 0, and 0 when Delta(u) = 0.
(ii) The third root of g(t) = d is t3 = -3/2 - u, and d = d(u) = -(u+1)(4u^2+8u+5). The pair is a pair of a member iff d(u) != 0 and a, b != -1
    (<-> 2u^2+5u+4 != 0). t3 gives a new valid root iff t3 not in {a, b} (<-> 12u^2+24u+13 != 0) and t3 != -1 (<-> 2u+1 != 0).
(iii) Singular pairs: a^4 = b^4, a != b <-> b = -a (u = 0) or a^2 + b^2 = 0 (<-> u^2 = 2v <-> (u+1)(u+2) = 0). On the conic,
    -D4 = (2u(u+1)(u+2))^2, so chi(-D4) = 1 exactly on the nonsingular pairs.
(iv) Pairs containing y = 1 contribute sum_d 2|T_d|(|T_d|-1) = 2 * (number of ordered finite pairs). Hence
    SPEC_c1(q) = sum_{u: E(u) != 0} (1 + chi(Delta(u))) * (2 + N(u)(I(u) - 1)),
    E = (u+1)(4u^2+8u+5)(2u^2+5u+4)(3u^2+6u+4), N(u) = [u(u+1)(u+2) != 0], I(u) = [(12u^2+24u+13)(2u+1) != 0];
    and since sum_u chi(-(3u^2+6u+4)) = -chi(-3):
    SPEC_c1(q) = 2(q - chi(-3)) - 2 sum_{u in Z_E} (1 + chi(Delta(u))) - sum_{u in Z_I \ (Z_E u {0, -2})} (1 + chi(Delta(u))),
    Z_E, Z_I = the roots in F_q of E and of (12u^2+24u+13)(2u+1).
This is an explicit formula for every q = p^n, p >= 5 (no finite verification needed for this class). Checks: all symbolic identities (SymPy) and
equality with the referee's independent brute force at all 75 primes 7..397 (incl. p = 7, 13).

## Class c + d = 0 in full (2026-11-04) [HAND + SYM + EXACT: p4_step5_cd0.py]
Members (c, -c), c != 0, 1 (c = 1, d = -1 belongs to class c = 1). With s = 2y - 1, c[y^4 - (1-y)^4] = 1 <-> s^3 + s = 2e, e = 1/c in F_q \ {0, 1};
y = 1 (s = 1) is never a root, so every root is finite in t = y/(1-y) = (s+1)/(1-s), and t != -1 always.
(i) Distinct roots s1, s2 <-> s1^2 + s1 s2 + s2^2 = -1 <-> pi = s1 s2 = sigma^2 + 1, sigma = s1 + s2; ordered pairs per sigma: 1 + chi(Delta),
    Delta = -(3 sigma^2 + 4) (none if Delta = 0). Third root s3 = -sigma, e = -sigma(sigma^2+1)/2.
(ii) e != 0 <-> sigma(sigma^2+1) != 0; e != 1 <-> (sigma+1)(sigma^2-sigma+2) != 0; s3 in {s1, s2} <-> 3 sigma^2 + 1 = 0.
(iii) On the conic -D4 = [4 sigma(sigma-2)(sigma+2)/(sigma^2-sigma+2)^2]^2 and the singular pairs are exactly sigma = +-2 (given e != 0);
    so chi(-D4) = 1 on all nonsingular pairs.
(iv) Per ordered nonsingular pair the weight is (r-2) - 1 - 1 = I - 2 with I = [3 sigma^2 + 1 != 0]; singular pairs give 0. Hence
    SPEC_cd0(q) = sum_{sigma: E != 0} (1 + chi(Delta)) N (I - 2),  E = sigma(sigma^2+1)(sigma+1)(sigma^2-sigma+2)(3 sigma^2+4), N = [sigma^2 != 4],
    = -(q - chi(-3)) + sum_{Z_E} w + sum_{sigma = +-2, not in Z_E} w - sum_{Z_I \ (Z_E u {+-2})} w,  w = 1 + chi(Delta), Z_I = roots of 3 sigma^2 + 1.
Checks: symbolic identities (SymPy) and equality with the referee's independent brute force at all 75 primes 7..397.

## Class rep in full (2026-11-04) [HAND + SYM + EXACT: p4_step5_rep.py]
Y = y0 not in {0, 1}; member (c, d) = (Y^-3, (1-Y)^-3) has the double root Y: f = c y^4 + d(1-y)^4 - 1 = (const)(y - Y)^2 Q(y) with
disc Q = -8 Y^2 (Y-1)^2 (Y^2-Y+1), Q(Y) = 6 Y^2 (Y-1)^2 != 0 (no triple root), Q(1) != 0 (c != 1). Excluded (other classes): Y^3 = 1 (c = 1),
3Y^2-3Y+1 = 0 (c + d = 0). Ordered pairs: (Y, r) has residual roots {Y, r'}, distinct, so chi(-D4) = 1; (r1, r2) has residual roots {Y, Y}, D4 = 0.
Singular (Y, r): r = Y/(2Y-1) (t -> -t) is a root of Q iff 2Y^2-2Y+1 = 0; r = eps Y/(eps Y - Y + 1), eps^2 = -1 (t -> eps t), iff Y in {eps, 1+eps}
(norm (Y^2+1)(Y^2-2Y+2)). Two residual roots in F_q (chi(-2(Y^2-Y+1)) = 1): C(Y) = 6 - (4*2 + 2*1) + s(Y) = -4 + s(Y), s(Y) = 2 * #singular r.
Y^2-Y+1 = 0: Q has the double root 1-Y (member c = d = -1, reached from both Y and 1-Y, counted once), always nonsingular, C = -4.
  SPEC_rep(q) = -2(q - chi(-2)) + 2 sum_{Y in X} (1 + chi(-2(Y^2-Y+1))) + 2 #(Z_s \ X) - 2 #Z(Y^2-Y+1),
  X = {0, 1} u Z(Y^2+Y+1) u Z(3Y^2-3Y+1) u Z(Y^2-Y+1), Z_s = Z((2Y^2-2Y+1)(Y^2+1)(Y^2-2Y+2)).
Checks: symbolic identities; per-Y and fully explicit formula both equal to the referee's brute force at all 75 primes 7..397.
Collision primes of the rep loci: {2, 3, 5, 7, 13}.

## Step 5 CLOSED without finite verification (2026-11-04) [SYM + EXACT: p4_step5_total.py]
Adding the three explicit class formulas: the q-coefficient is 2 - 1 - 2 = -1, and every correction is a sum over the roots of an explicit
polynomial P of 1 + chi(h); on the roots of P, h is a rational constant or a rational constant times a square (e.g. on 2u^2+5u+4: Delta = (u+2)^2,
on sigma^2-sigma+2: Delta = (sigma-2)^2, on Y^2+Y+1: -2(Y^2-Y+1) = -4/3 (Y-1)^2), so each correction is a function of chi(-1), chi(2), chi(3), chi(7).
For p not in {2,3,5,7,13} (loci disjoint) the evaluator gives SPEC = -q + const with const equal to 10 + 5chi(-1) + 6chi(-2) + 2chi(-3) - 2chi(-7)
in ALL 16 sign classes (control: evaluator = brute force at 9 generic primes). This PROVES (*) for those q = p^n (n odd and even), replacing the
finite-verification argument. For p = 7, 13 the set-valued class formulas still hold (their derivation is field-uniform) and all loci have roots in
F_{p^2}, so SPEC depends only on n mod 2 [corrected 11-04: n odd / n = 2 mod 4 / n = 0 mod 4, see Referee 6]; the direct checks at 7, 343 | 49, 2401 and 13, 2197 | 169, 28561 fix it.
(Bug caught by the control before any report: the evaluator truncated the rational -4/3 to -1 via sp.Integer; fixed to sp.Rational.)

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
