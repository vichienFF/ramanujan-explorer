# Independent referee report: STEPB_PROOF.md (Steps 1-4, with brief comments on Step 5)

Reviewer: independent AI referee (Claude), 2026-10-16. No existing files were modified.
Scratch checks (outside the project folder): step1_check.py, lin_check.py and cert_rerun.py in the session scratchpad. Their results are quoted below.

## Verdict: SOUND WITH FIXES (Steps 1-4, per fixed rho)

The core argument is correct: universal curve, twist by a fixed order-3 Moebius map, absolute irreducibility certificate, then Weil/Aubry-Perret. One gap matters for the statement as written. It is proved only for q = p^k with p > p0(rho), and p0 is not explicit (issue 1). Several smaller points need to be written out properly. Step 5 (plan only) contains an arithmetic error that breaks the claimed uniform bound (issue 10).

## What I checked and found correct

**A. Step 1 exponent bookkeeping.**
v(c-a) - u(b-a) = (u-v)a + vc - ub. F_q^* = <g^m>, where m = (q^3-1)/(q-1). So the condition is x^{u-v} z^v y^{-u} in F_q^*. The exponents sum to 0, so this is well defined on P(L). Correct.

**B. Moebius normalisation.**
Let theta_i be the root of l_i. Take mu(s) = [(s-theta_1)/(s-theta_0)] * [(theta_2-theta_0)/(theta_2-theta_1)]. Then:
- l_1/l_0 = c_1 mu(s).
- mu(s) - 1 = (theta_1-theta_0)(s-theta_2) / ((s-theta_0)(theta_2-theta_1)), so l_2/l_0 = c_2 (mu(s)-1).
- The constants cancel because the exponents sum to 0.
- The point s = infinity maps to the finite value mu(infinity) = (theta_2-theta_0)/(theta_2-theta_1), which is not in {0, 1, infinity}.

Correct.

**C. Twist.**
For s in P^1(F_q), S = mu(s) satisfies S^q = sigma(S), with sigma = mu^(q) o mu^{-1}. This sigma sends 0 -> infinity -> 1 -> 0, so sigma(S) = 1 - 1/S. It is defined over Q and independent of q, L and g.
- C is sigma-stable: sigma*E1 = E2/E1 and sigma*E2 = (-1)^{sum} / E1.
- The map S -> 1/S preserves C and conjugates sigma to sigma^{-1}, so the choice of direction does not affect the count.
- No twisted-rational point has a coordinate in {0, 1, infinity}, because sigma has no fixed point there. So boundary points never contribute.

**D. Exact numerical confirmation of Step 1 (step1_check.py).**
Setup: q = 5, 7, 11, 13, L = span{1, w}, including the point s = infinity, and 12 ratios. Three counts agree in every case:
- the Singer count N(u,v) := #{distinct a,b,c in S : v(c-a) = u(b-a) mod m};
- N(rho), whenever gcd(v,m) = 1;
- the twisted count #{(S,R,T) pairwise distinct : S^q = 1-1/S etc., on C}.

The correspondence is therefore exact (no O(1) error) once the diagonal is removed. Example: q = 13, rho = -4/3, all three counts equal 18. This includes the cases 3 | m (q = 7, 13) with v = 3.

**E. Step 2 (forbidden ratios).**
- Take exponents (-2,1,1): rt = s^2 and (r-1)(t-1) = (s-1)^2 give r + t = 2s, so (X-r)(X-t) = (X-s)^2 and r = s = t.
- (1,-2,1) and (1,1,-2) follow by relabelling coordinates; sign is irrelevant.
- These give rho = -1 (v=1, u=-1), rho = 1/2 (v=-2, u=-1) and rho = 2 (v=1, u=2). Correct.
- The argument works in every characteristic, including 2.
- Confirmed numerically: N = 0 for q = 5, 7, 11, 13.

**F. Step 3 (a): k | [K:Q] is correct.**
- G is a Q-irreducible factor (from factor_list over Q), so Gal(Qbar/Q) permutes its geometric components transitively.
- The field of definition of a component F (the fixed field of its stabiliser) has degree exactly k.
- A smooth K-point lies on a unique component, so Gal(Qbar/K) fixes F. Hence Q(F) is contained in K and k | [K:Q].
- The fallback "G irreducible over K implies k = 1" is also correct.
- K is the residue field Q[x]/(f) with f Q-irreducible, so [K:Q] = deg f. Correct.

**G. Step 3 (b): the smoothness test is correct.**
- If gcd(f, G_s|slice) = 1 or gcd(f, G_t|slice) = 1, the gradient is nonzero at every root of f, and G vanishes there.
- A degree drop on the slice only loses points at infinity. It never creates a false smooth point, so no non-degeneracy hypothesis is needed. (The m == 1 filter is redundant but harmless.)
- Points at infinity: if s0 is a simple root of G_d(s,1), then the derivative of the projective closure with respect to s, evaluated at [s0:1:0], equals (G_d)_s(s0,1), which is nonzero. So the point is smooth on the projective closure. Correct.

**H. Step 3 (c)/(d): spurious and missing components.**
1. Every component of C dominates a curve in the (s,t)-plane. The only way to fail is a vertical line in r, which would need beta = 0.
2. For H <= 4, the factors dropped as "linear" are exactly (s-t)^2 (lin_check.py). No s, s-1, t or t-1 factors and no other lines appear.
3. The square comes from the diagonal being a non-reduced (double) component of the scheme C. Along the diagonal the two gradients (alpha, beta, gamma)/s and (alpha, beta, gamma)/(s-1) are proportional, so the Jacobian has rank 1. Off-diagonal points with s = t are finite in number.
4. All non-linear factors have multiplicity 1.

Multiplicity 1 by itself already proves that a unique component of C lies over G, mapping to it birationally. The reason is that ord_G Res_r = sum over components over G of (degree of map) x (intersection multiplicity).

So "G absolutely irreducible + multiplicity 1 + only dropped factor is (s-t)^2" does give "C minus Delta is absolutely irreducible". The subresultant test is also valid: sympy rem by a single polynomial is an exact divisibility test, because {G} is a Groebner basis of (G). But that test is redundant.

**I. Certificates re-run (cert_rerun.py, H <= 4).**
All 5 non-forbidden classes certify, reproducing the claimed results:
- degrees 2 / 4 / 6 / 12 / 28;
- smooth-point field degree gcd = 1, or a quadratic field over which G stays irreducible.

**J. Step 4 normalisation.**
E = (q^3-q)/(q^2+q-1) = q - 1 + (q-1)/(q^2+q-1) = q + O(1). Aubry-Perret (|#X(F_q) - q - 1| <= 2 p_a sqrt(q), for X absolutely irreducible and projective, possibly singular) is the right tool. A twist of a geometrically irreducible curve is geometrically irreducible.

## Issues

**1. [MAJOR] Small characteristic and ineffective p0.**
"Absolutely irreducible over Qbar implies the same over F_p-bar for p > p0" (EGA IV 9.7.7 / Noether forms) is true but ineffective, and it says nothing about q = p^k with p <= p0. For such p, C mod p minus Delta could acquire extra components. That would shift the count by a multiple of q and break N/E - 1 = O(q^{-1/2}) along q = p^k, k -> infinity. The statement "for each fixed non-forbidden rho" over all prime powers q is therefore not yet proved.

Fix, either:
- (a) restrict the theorem to char(F_q) > p0(rho) and say so; or
- (b) make p0 explicit and certify the finitely many small p directly.

For (b): the bad primes are those dividing:
- the leading or bidegree coefficients of G;
- disc(f) and Res(f, G_s|slice) for the certificate points;
- the content of the multiplicity-1 / (s-t)^2 structure, i.e. the discriminant-type integer showing that Res_r mod p = (s-t)^2 * (G mod p) with G mod p squarefree.

Then over each small p, apply the F_p version of the same certificate: G mod p is F_p-irreducible with the same bidegree, plus a smooth F_p-point (or gcd of smooth-point degrees = 1), which gives absolute irreducibility. Alternatively use Ruppert's or Gao's effective criteria.

Also check that the elimination structure (only (s-t)^2 dropped, G of multiplicity 1) survives mod p. Otherwise birationality and uniqueness can fail in characteristic p even when G mod p is irreducible.

**2. [MAJOR] Genus bound uniform in q.**
"2 p_a(rho) sqrt(q)" must use a model whose arithmetic genus does not depend on p. State it explicitly. Recommended version:
- The projection (S,R,T) -> (S,T) commutes with sigma, so it is defined over F_q on the twisted forms.
- Its image G' is a twisted form of G in (twisted P^1)^2, which is isomorphic to (P^1_{F_q})^2.
- Take p_a <= (deg_s G - 1)(deg_t G - 1), which is constant for p > p0.
- Account for the points where C\Delta -> G' is not an isomorphism. There are O(deg^2) of them, by the birationality from multiplicity 1.

Alternatively, use flatness of the closure of C\Delta over Z[1/N] to fix the Hilbert polynomial.

**3. [MINOR, but must be stated] gcd(v,m) = 1.**
The prime divisors of m are 3 (exactly once, when q = 1 mod 3) and primes = 1 mod 3. So for 3 | v, rho = u/v mod m is undefined for every q = 1 mod 3.

The clean fix is to state the theorem for N(u,v) := #{v(c-a) = u(b-a) mod m}. The Step 1 equivalence never uses invertibility of v, and I checked it numerically for q = 7, 13 with v = 3. Then N(rho) = N(u,v) whenever gcd(v,m) = 1.

Also exclude u in {0, v} explicitly: rho = 0, 1 give N = 0, and the exponent triple has a zero entry, so the curve is degenerate. Assume gcd(u,v) = 1, which makes the exponent triple primitive.

**4. [MINOR] Step 1 wording.**
"w in F_q^* iff w = w^q = w^{q^2}": only w^q = w is needed. The curve {Phi_1 = Phi_2 = 1} should be justified as follows:
- Its F_q-points coincide with those of the surface {Phi_1 = 1}, since Frobenius sends Phi_1 to Phi_2/Phi_1.
- The ideal (Phi_1 - 1, Phi_2 - 1) is Frobenius-stable: Phi_1 -> Phi_2/Phi_1 and Phi_2 -> 1/Phi_1.

Also:
- Give sigma explicitly: sigma(S) = 1 - 1/S.
- Do not reuse the letter s for both the F_q-parameter and the new coordinate.
- Replace "N(rho) + O(1) = #C'(F_q)" with the exact statement (fact D above): N(u,v) equals the number of twisted-rational points of C with pairwise distinct coordinates. The O(1) then comes only from the points of the closure of C\Delta that meet the diagonal or another coincidence locus, plus the normalisation/singularity correction.

**5. [MINOR] Define "C minus diagonal" scheme-theoretically.**
The diagonal is a double component of the complete intersection C (fact H.3). Define C^0 as the reduced closure of C(Qbar) \ Delta. Also bound the coincidence points s = r, s = t, r = t on C^0. Each forces (t/s)^gamma = ((t-1)/(s-1))^gamma = 1, giving at most gamma^2 points.

**6. [MINOR] Certificate code should assert, not ignore, the dropped factors.**
irred_cert.py silently drops every factor of total degree <= 1. Add an assertion that the dropped part is exactly (s-t)^2 and that every kept factor has multiplicity 1, and print it in cert_*.txt. Otherwise a genuine linear component of C would go unnoticed. None occurs for H <= 4, but this is not recorded for H = 5, 6.

**7. [MINOR] Status and record-keeping.**
- cert_H6.txt contains only 4 classes (rho = -6/1, -6/5, -5/1, -5/2). The H <= 6 run is incomplete, and there is no saved output file for H <= 4. Save the H <= 4 output (my re-run reproduces it).
- "Degree of G up to 34 already at height 4": I find a maximum of 28 at H <= 4 (rho = -4/3). Correct the number, or explain which elimination order gives 34.
- The docstring of irred_cert.py still describes the old mod-p method. Update it.

**8. [MINOR] The numerical check does not test the theorem's actual object.**
curve_count.py counts the split model #C(F_p), not the twisted form, and not N(rho). It is a consistency check of the genus size only. Add the direct check from fact D (Singer count = twisted count) to the repository.

**9. [MINOR] Sympy as a trusted base.**
The fallback certificate ("G irreducible over a degree-d number field") depends on sympy's algebraic-field factorisation. For publication, either:
- prefer the gcd-of-degrees route, which needs only Q-factorisation and gcds; or
- cross-check with a second system (Pari/Magma/Sage).

At H <= 4 this route is used only for rho = -3/1 (degree 4, quadratic field). That case is also easy to certify by hand: G has degree 4 and a rational smooth point can be searched for.

**10. [MAJOR, Step 5 plan only] The uniformity sum is miscomputed, and large-height rho are not handled.**
With roughly H ratios of height H, weight H^{-3} and error H^2 q^{-1/2} (genus ~ H^2), each height contributes H * H^{-3} * H^2 = H^0. Summing over H <= H_max gives H_max * q^{-1/2}, not q^{-1/2} log q. Since rho = xi2/xi1 mod m ranges over all residues, H_max ~ sqrt(m) ~ q, and the bound becomes trivial.

Also, every residue mod m has a rational representative of height up to about sqrt(m). For those, the genus H^2 ~ q exceeds sqrt(q), and Weil gives nothing.

Step 5 needs one of:
- (i) genus o(H), which is unlikely: deg G grows like H^2 (78 at H = 6);
- (ii) a better weight decay;
- (iii) a separate argument for rho of height greater than q^{1/4} or so, for example a trivial or a large-sieve bound on T(rho) combined with |W| decay.

The current plan does not yet yield a theorem for k = 3.

## What I could not check
- Absolute irreducibility in small characteristics (p = 2, 3, 5, ...) for any rho, and the size of p0(rho).
- The H = 5 and H = 6 certificates beyond the 4 lines in cert_H6.txt. I did not re-run H >= 5.
- Independent verification of sympy's algebraic-field factorisation (used once at H <= 4).
- The genus values themselves: only lower bounds from point counts exist (genus_probe.py).
- The literature novelty claim.
