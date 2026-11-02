# Independent review of N2_PROOF.md (N(-2), l = -2 family) — referee report, 2026-10-30

Reviewer: independent Claude subagent (skeptical referee). Work done locally only; nothing sent to any external service.
Own scripts (no reuse of the authors' code): `review_n2/rv_bruteforce.py` (brute force over all (c,d), Greene 3F2 from the
definition with complex characters), `review_n2/rv_symbolic.py` (sympy re-derivation of Steps 1, 3, 5). Both have CONTROL
known-answer asserts; both PASS.

## Brute-force test of the theorem
For every q in {5,7,11,13,17,19,23,29,31,37,41,43,47,53}, `rv_bruteforce.py` counts the factorisation type of
Q_{c,d} for every (c,d) in (F_q*)^2 by direct root finding + multiplicities (one simple root and no other root <=> (1)(3)),
and checks 3N = (q-2)(q+1) + b_q, plus every intermediate claim (root total, P by the definition AND by enumerating root pairs,
S2 by explicit polynomial division, T by the direct (u,v) sum, T = 1+phi(-1)G(4), T = q+1+b_q, E, C, D, the three type
identities, q^2 3F2(4) = phi(-1)G(4), and 3F2(4) = 1/q for q = 2 mod 3). **ALL PASS on all 14 primes.**
N values: 6, 14, 36, 44, 90, 122, 168, 270, 294, 452, 546, 594, 720, 918. No factorisation types with a triple or
quadruple root ever occur; the only other type is "no F_q-root" (rest degree 4).

## Step 1 — correct and proved (minor gaps in exposition)
* Expansion of Q, det, c, d: re-derived with sympy (rv_symbolic) — correct.
* Root lines: Q(y)=0 <=> c(1-y)^2 + d y^2 = y^2(1-y)^2, intercepts (y^2,0), (0,(1-y)^2), distinct and nonzero for y in S,
  so q-2 points with cd != 0. Correct.
* Admissibility: c = 0 <=> u = 2, d = 0 <=> u = 0 (given y1 != y2), det = 0 <=> 2v = u. **Missing sentence:** when det = 0
  the two lines are parallel and *distinct* (normalised forms c/y^2 + d/(1-y)^2 = 1 coincide only if y1 = y2), so there is
  no (c,d) at all — this must be said, otherwise "admissible iff det != 0" is unjustified. Also worth stating: any two
  distinct roots of Q_{c,d} with cd != 0 form an admissible pair (needed in Step 6).
* Edge cases: y = 1/2 is fine (2v = u has no partner for it, handled in Step 2); characteristic 3 excluded by q >= 5;
  q = 5 gives P = 0 (checked). No missed cases.

## Step 2 — correct and proved
Partners -y, 2-y, y/(2y-1): checked by hand that they are pairwise distinct for y in S (-y = y/(2y-1) => y = 0;
2-y = y/(2y-1) => (y-1)^2 = 0), each lies in S\{y} except exactly at y = -1, 2, 1/2 respectively, and these three
exceptional y are distinct for q >= 5. Relations symmetric. (q-2)(q-3) - [3(q-2) - 3] = (q-3)(q-5). Correct.
Brute force confirms P_definition = P_pairs = (q-3)(q-5)/2.

## Step 3 — correct; one point needs to be written out
* s = 2-u, p = -c/v and disc = u(u-2)(2v-u+2)/(2v-u): re-derived symbolically, correct; chi(disc) = chi(D) since
  2v-u != 0 on admissible pairs.
* Weighting (1+chi(u^2-4v))/2: 1 on split distinct, 0 on irreducible, 1/2 on u^2 = 4v; the doubled sum is
  1 + T and the diagonal enters with weight 1 in the doubled sum. Correct.
* sum chi(D) = (-1)(-1) = 1: correct (w = 2v-u bijective in v).
* Exclusions (in the doubled sum): v = 0: weight 2, chi(D) = chi(u^2(u-2)^2) = 1 for u != 0,2 -> 2(q-2).
  v = u-1: same value, 2(q-2) **including u = 1**; the point (u,v) = (1,0) (roots {0,1}) lies on both lines, so the
  authors' 2q-6 = 2(q-3) is exactly the inclusion–exclusion correction. **Not double counted** — but the draft should say
  "(u = 1 already removed on v = 0)" in the write-up itself (it is only in PROOF_STATUS). Diagonal meets v=0 only at
  u=0 and v=u-1 only at u=2, both with D=0 — no further overlaps. Diagonal: D = u^2(u-2)^2((u-1)^2+3)/4,
  sum = -1 - 1 - 1 = -3. Correct.
* det/c/d = 0 lines: factors of D, contribute 0. Correct. Also correct that the root-0/root-1 lines are the only
  further restriction (roots must lie in S).
* Result S2 = (T - 4q + 14)/2: confirmed by brute force (14 primes).

## Step 4 — correct and proved
Redone by hand: x = u-1, z = 2v-u+1 gives u(u-2) = x^2-1, (2v-u)(2v-u+2) = z^2-1, u^2-4v = x^2+1-2z (bijective, q odd).
z = 1-2t: z^2-1 = 4t(t-1), x^2+1-2z = x^2-1+4t. sum_x f(x^2) = sum_s (1+chi(s)) f(s) is correct also at s = 0
(1+0 = 1 = #{x: x^2 = 0}). With r = 1-s: summand chi(-r) chi(t(t-1)(4t-r)) (the 4 is a square). "1"-part:
sum_t chi(t(t-1)) sum_r chi(r(r-4t)) = -sum_{t != 0} chi(t(t-1)) = 1. chi(1-r) part:
chi(-1) chi(r(1-r)) chi(t) chi(t-1) chi(4t-r) = chi(-1)·[G(4) summand] (two sign flips cancel). T = 1 + phi(-1)G(4). Correct.

## Step 5 — correct; two sentences missing
* Square-of-quadratic case forced to m = 1, (c,d) = (-1,-1): verified (symbolic + hand). For q = 2 (mod 3) this point
  is of type **(2)^2**, which is not in the Step 6 type list; it has 0 roots so it does not affect any identity, but the
  list should mention it (along with (2)(2), (4)).
* Double root: the 2x2 linear system has det = -a(1-a) != 0 => unique (c,d) = (a^3, -(a-1)^3); Q = (y-a)^2 R_a,
  disc R_a, R_a(a) = 3a(a-1) != 0 (q != 3) => no (1)^3(1), (1)^4. Also R_a(0) = -a, R_a(1) = a-1 nonzero, so roots of
  R_a lie in S (should be stated). All verified symbolically.
* Injectivity: a -> (c,d) is injective except that the two roots of a^2-a+1 map to (-1,-1) (the (1)^2(1)^2 point);
  an E or C point has exactly one double root (two double roots force the square case). The draft uses this implicitly
  in "D = z0/2" — should be stated. sum_{a in S} chi(a^2-a+1) = -1-1-1 = -3, E = (q+1-z0)/2, C = (q-5-z0)/2,
  D = z0/2: correct and confirmed by brute force.

## Step 6 — correct and proved
Per type (roots, pairs, sum of chi(disc) over its pairs): N (1,0,0); E (1,0,0); A (2,1,-1); B = four distinct simple roots
(4,6,+6); C = (1)(1)(1)^2 with double root a: pairs {a,b1},{a,b2} residual (y-a)(y-b) split -> +1 each, {b1,b2}
residual (y-a)^2 -> chi(0) = 0: (3,3,2); D (2,1,+1); (2)^2,(2)(2),(4): (0,0,0). Matches the draft. Elimination redone by hand:
N = (q-2)^2 - E - 4P/3 + 2S2/3 - C/3 - 4D/3, and substitution gives (q-2)(q+1)/3 for q = 2 (mod 3) and the extra
+1 + 1/3 - 4/3 + b_q/3 = b_q/3 for q = 1 (mod 3). Correct. (Notation: "(1)^4 split" should read (1)(1)(1)(1); the letter D
is used both for the type count and the polynomial in Step 3 — rename one.)

## Step 7 — [G] correct and can be proved in 6 lines; [BK] not verifiable here
* My own implementation of Greene's definition ((A over B) = B(-1)/q J(A, B-bar), J(A,B) = sum A(x)B(1-x), chi(0)=0 for
  all chi incl. eps, 3F2 = q/(q-1) sum_chi ...) gives q^2 3F2(phi,phi,phi;eps,eps|4) = phi(-1)G(4) on all 14 primes.
* **Hand proof (recommended to replace the citation [G]):** expand each binomial: (phi chi over chi) =
  chi(-1)/q · sum_{y != 0,1} phi(y) chi(y/(1-y)). Orthogonality over chi gives
  q^2 3F2(4) = sum_{y1,y2,y3 in S, (1-y1)(1-y2)(1-y3) + 4y1y2y3 = 0} phi(y1y2y3). Solve y3 = K/(K-4M), K = (1-y1)(1-y2),
  M = y1y2 (automatically in S; no solution if K = 4M): sum phi(y1y2) phi(K(K-4M)). With t_i = y_i/(1-y_i) and then
  t_i = -x_i: q^2 3F2(4) = sum_{x,y} phi(x(1-x)y(1-y)(1-4xy)). Finally x -> 1/x in G(4) gives
  G(4) = phi(-1) sum phi(x(1-x)y(1-y)(1-4xy)). Hence q^2 3F2(4) = phi(-1)G(4). (Checked consistent with numerics.)
* Value: numerically q^2·3F2(4) = q + b_q for all 14 primes (so 3F2(4) = 1/q when q = 2 mod 3, matching the quoted
  -phi(-3)phi(16)/q). I could **not** check Barman–Kalita Thm 1.7's exact statement or hypotheses (no web access by
  constraint); whether "order not 1,3,4" admits S = phi must be read from the paper. **Caution:** the q = 1 (mod 3)
  closed form often quoted from Ono 1998 is of the shape (4x^2-2p)/p^2, i.e. b_q/q^2, whereas Greene's normalisation here
  gives (q + b_q)/q^2. My memory of Ono's exact statement is not reliable, but a 1/q discrepancy of this kind is a classic
  normalisation trap: read the theorem and its normalisation line by line before citing. The proof of the theorem
  therefore currently depends on an unread citation for both residue classes.

## Verdict table
| Claim | Verdict |
|---|---|
| Step 1 formulas det, c, d | (a) proved, correct |
| Step 1 admissibility u != 0, 2, 2v != u | (b) correct; add "det = 0 => parallel distinct lines, no solution" |
| Step 2 P = (q-3)(q-5)/2 | (a) proved, correct |
| Step 3 disc formula, chi(disc) = chi(D) | (a) correct |
| Step 3 weighting, line contributions, S2 = (T-4q+14)/2 | (a) correct; overlap (1,0) handled correctly but only explained in PROOF_STATUS — add to draft |
| Step 4 T = 1 + phi(-1)G(4) | (a) proved, correct (incl. s = 0) |
| Step 5 repeated roots, E, C, D | (b) correct; state (2)^2 case, injectivity/one-double-root fact, R_a roots in S |
| Step 6 type identities and algebra | (a) correct (fix notation (1)^4, D clash) |
| Step 7 [G] q^2 3F2(4) = phi(-1)G(4) | (a) correct — elementary hand proof given above; no citation needed |
| Step 7 [BK]/Ono value of 3F2(4) | (b) numerically exact (14 primes) but citation unread; hypotheses on S unverified; normalisation caution |
| Theorem N(-2) = ((q-2)(q+1)+b_q)/3 | true on 14 primes 5..53 by independent brute force; proof complete modulo the 3F2(4) value |
| Nothing found to be (c) wrong. |  |

## Required fixes
1. Step 1: add the parallel-lines argument for det = 0, and the remark that any two distinct roots with cd != 0 are admissible.
2. Step 3: write the v=0 / v=u-1 overlap at (u,v) = (1,0) explicitly (that is why it is 2q-6 not 2q-4); note diagonal overlaps only at D = 0.
3. Step 5: mention the (2)^2 type for q = 2 (mod 3) (and (2)(2), (4)) as contributing 0; state that E/C points have a unique double root and the a -> (c,d) map is 2-to-1 only onto (-1,-1); R_a(0), R_a(1) != 0.
4. Step 6: rename "(1)^4 split" to (1)(1)(1)(1); rename either type D or polynomial D.
5. Step 7: replace citation [G] by the hand proof above; obtain and read Barman–Kalita Thm 1.7 (hypotheses on S, normalisation) and/or Ono 1998 before any claim; verify that the cited value equals (q + b_q)/q^2 in Greene's normalisation, not b_q/q^2.
6. Status line: "q = 2 (mod 3) complete" should read "complete modulo one citation (value of 3F2(4))", since [G] is now elementary.
