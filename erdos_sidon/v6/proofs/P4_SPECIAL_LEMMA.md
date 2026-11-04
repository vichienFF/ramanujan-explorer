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
For p not in {7, 13}, tau is determined by sigma_q = Frob_p^n in G; for p in {7, 13}, by n mod 2.

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
   data depend only on n mod 2.  QED (sketch)

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
  char-p exceptional points, defined over F_{p^2} (L multiquadratic) -> data depend on n mod 2 only.
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
(c) that the data really depend only on sigma (for p in {7, 13} only on n mod 2);
(d) the finite-verification logic.
Char 5 (N3 formula verified at 5, 25, 125, 3125, 15625) is outside this lemma (p >= 7) and needs its own argument.
