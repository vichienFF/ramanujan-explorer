# C9 step (b): N(rho)/E - 1 = O_rho(q^{-1/2}) via a universal curve (draft, 2026-10-16)

Status labels: [PROVED-SKETCH] argument written, needs referee-level check; [CERT] machine certificate (sympy, exact arithmetic).

## Setup
Singer set S = {i mod m : g^i in L}, m = q^2+q+1, n = q+1, g generates F_{q^3}^*, L a 2-dim F_q-subspace.
rho = u/v mod m (gcd(v,m) = 1). N(rho) = #{(a,b,c) in S^3 distinct : c - a = rho (b - a)}.
Put (alpha, beta, gamma) = (u - v, v, -u), sum 0. With x = g^a, y = g^b, z = g^c (points of P(L)):
  v(c-a) = u(b-a) mod m  <=>  x^{u-v} z^{v} y^{-u} in F_q^*.

## Step 1 [PROVED-SKETCH]: reduction to a universal curve
Choose an F_q-basis so P(L) = P^1(F_q), x = l(s) := e + s f. The three conjugate linear forms l_i(s) = e^{q^i} + s f^{q^i}
(i = 0,1,2) have distinct roots (e/f not in F_q). w in F_{q^3}^* lies in F_q^* iff w = w^q = w^{q^2}. Since the expression is
homogeneous of degree 0, after a Moebius change of coordinates over F_{q^3} sending the three roots to infinity, 0, 1, the
condition becomes, with (s, r, t) the coordinates of (x, z, y):
  C_{alpha,beta,gamma}:  s^alpha r^beta t^gamma = 1,   (s-1)^alpha (r-1)^beta (t-1)^gamma = 1.
The F_q-structure becomes Frob(P) = sigma(P), sigma the order-3 Moebius map permuting {0, 1, infinity}. So N(rho) + O(1) =
#C'(F_q) for a twisted form C' of C (diagonal removed). C does not depend on q, L or g.

## Step 2 [VERIFIED by hand]: forbidden ratios
rho = -1, 2, 1/2 (exponents a permutation of (-2,1,1) up to sign): the equations force r + t = 2s, rt = s^2, so r = s = t:
C is the diagonal only, N = 0. This is the -3/(2Cq) main term of the note.

## Step 3 [CERT for height <= 4; height <= 6 running]: absolute irreducibility
Eliminate r (smallest |exponent|) by resultant -> plane curve G(s,t) (drop linear factors). Certificate: smooth points of G over
number fields K_i; the geometric component through P_i is defined over a subfield of K_i, so the number k of geometric
components divides every [K_i:Q]; gcd = 1, or G irreducible over the smallest K_i, gives k = 1. Birationality C -> G: r is a
rational function on C (|exponent| = 1, or the first subresultant does not vanish identically on G).

## Step 4 [PROVED-SKETCH]: Weil bound
C absolutely irreducible over Q-bar => absolutely irreducible over F_p-bar for all p > p0(rho). Aubry-Perret:
|#C'(F_q) - q - 1| <= 2 p_a(rho) sqrt(q). Excluded points (diagonal, coincidences, points at 0/1/infinity) are O_rho(1).
E = (q+1)q(q-1)/(q^2+q-1) = q + O(1). Hence N(rho)/E - 1 = O_rho(q^{-1/2}).

## Numerical check [VERIFIED]
curve_count.py: split model over F_p, p = 101..3001, all ratios of height <= 6: (count - p)/sqrt(p) in [-3.6, 5.9]; forbidden = 0.

## What this does NOT give
Uniformity in rho (constants grow with the height: degree of G up to 28 already at height 4 (corrected per review)), all k-th moments, hence not C9.
Literature: the per-rho statement is natural; a careful search is needed before calling it new (LITERATURE_B26 pass 1 found
nothing in this exact form).

## Step 5 (next, PLAN): from per-rho bounds to the third moment R3 uniformly
Fourier on Z/m: averaging over dilates u, the third factorial moment of window counts is a sum over (xi1, xi2, xi3), sum 0, of
W(xi1)W(xi2)W(xi3) * T(xi2/xi1), with T(rho) = sum_u S^(u) S^(u rho) S^(-u(1+rho)) = m * (point count of C_rho) and
|W(xi)| << 1/|xi| (window transform). Small xi1, xi2 <=> LOW-height rho, so weights decay like H^{-3} per representation.
If (i) C_rho is absolutely irreducible for every non-forbidden rho and (ii) genus g(rho) << H(rho)^2, the total error is
sum_H H * H^{-3} * H^2 * q^{-1/2} = sum_H 1 * q^{-1/2}  -> DIVERGES linearly in H_max (review 2026-10-16 caught the earlier
'log q' slip). Per-rho Weil bounds with genus ~ H^2 are NOT enough; need either genus o(H) (unlikely) or cancellation ACROSS rho
(family/Katz-type bound for sum_rho w(rho)(N(rho)-E)), plus a separate treatment of high-height rho.
Genus probe (genus_probe.py, 25 primes 151..~700, LOWER bounds max|a_p|/2sqrt p): H=3..10 -> 2.1, 2.2, 5.1, 2.2, 5.1, 5.7, 6.6, 12.2
(consistent with polynomial growth; not a proof). Needed: general irreducibility proof (not per-rho certificates) + genus formula
(Riemann-Hurwitz / Euler characteristic of a torus-translate intersection with (P^1 - 3 pts)^3).
Then k >= 4: varieties of relations among k points of a line (dimension k-2), Deligne/Lang-Weil in place of Weil.

## Independent review 2026-10-16 (INDEPENDENT_REVIEW_STEPB.md): SOUND WITH FIXES
- Step 1 verified by hand + exact Singer counts q = 5,7,11,13 (incl. s = infinity): twist sigma(S) = 1 - 1/S, no O(1) discrepancy.
- Step 2 verified for all permutations and characteristics. Step 3 certificate logic verified (k | [K:Q]; smoothness test OK;
  dropped factor is (s-t)^2 from the diagonal; kept factor multiplicity 1 gives birationality).
- FIXES ADOPTED: (1) theorem stated for q PRIME (or char p > p0(rho), p0 not explicit) - small characteristic open [MAJOR];
  (2) genus bound must use a p-independent model (projective closure of G of degree d: p_a <= (d-1)(d-2)/2) [MAJOR];
  (3) Step 5 sum corrected above [MAJOR]; (4) state counts as N(u,v) = #{v(c-a) = u(b-a) mod m} (no gcd(v,m) issue) [MINOR].

## Step 5 evidence (2026-10-16, exploratory on already-seen data: Batch 27 + Lane B1, q 41..2969, exact R3)
delta = R3 / (-P3(Cq)) - 1 (exact finite-l forbidden-AP prediction): rms(delta)*sqrt(q) ~ 5.4-6.3, flat across q bands, for C = 2, 4, 8;
log-log slope -0.41 / -0.49 / -0.47. [VERIFIED numerically] the TOTAL relative error is ~ 6 q^{-1/2}, i.e.
R3 = -P3(Cq) (1 + O(q^{-1/2})) ~ -3/(2Cq) + O(q^{-3/2}): square-root cancellation ACROSS rho (no growth with the height cutoff).
So the target statement for Step 5 is a family bound |sum_rho w(rho)(N(rho) - E)| << sqrt(q) * sum w, not per-rho Weil.

## Genus of C_{a,b,c} (2026-10-16, genus_mono.py: Riemann-Hurwitz + numerical monodromy; validated on Fermat n=3..6)
(-3,1,2): 0 | (-4,1,3): 0 | (-5,2,3): 1 | (-5,1,4): 1 | (-6,1,5): 3 | (-7,2,5): 7 | (-7,3,4): 16 | (-8,3,5): 22  [(-9,4,5) not reached]
Family (-n,1,n-1): g = (n-3)(n-4)/2 fits n=3..6 -> QUADRATIC in the height; balanced exponents grow faster.
[VERIFIED numerically] per-rho Weil bounds cannot give the uniform R3 theorem (need g = O(H)); the observed ~6/sqrt(q) total error
must come from cancellation ACROSS rho. Next idea [INFERENCE]: with additive Fourier on Z/m, |S^(xi)|^2 = q (perfect difference
set) and the u-average of S^(u xi1) S^(u xi2) S^(-u(xi1+xi2)) is a sum of Gauss/Jacobi-sum products -> Fermat-quotient curves;
cancellation over (xi1, xi2) may follow from Deligne/Katz equidistribution of Jacobi sums. Literature needed: Evans-Hollmann-
Krattenthaler-Xiang (Gauss sums of Singer difference sets), Katz "Gauss sums, Kloosterman sums and monodromy".

## Step 5 reformulation (2026-10-16) [SOURCE: Singer character values chi(D) = -G(chi)/q, EHKX arXiv math/9807029 background]
With G(psi1)G(psi2)G(psi3) = psi3(-1) q^3 J(psi1,psi2) (psi1 psi2 psi3 = 1, Gauss/Jacobi sums over F_{q^3}), the u-average in F3
becomes sum_{alpha,beta} W^(alpha) W^(beta) W^(-alpha-beta) * #{x in F_{q^3}: x^alpha (1-x)^beta in F_q^*}. Recombining the window
transforms: the R3 deviation = joint distribution of (log x, log(1-x)) in SHORT intervals of the cyclic group F_{q^3}^*/F_q^*
(length ~ q in a group of size ~ q^2). [INFERENCE] completing with |J| = q^{3/2} loses a factor sqrt(q) * log^2 q: the needed
bound is BEYOND square-root (Weil/Deligne) cancellation for each character pair - a "discrete logs of x and 1-x in short
intervals" problem (Paley-graph / sum-product type). The data (error ~6/sqrt q) says it is true, but a proof likely needs a
genuinely new idea. Status: rigorous uniform R3 = OPEN research problem; per-rho theorem stands.

## Route V (2026-10-16): R_k -> 0 for FIXED k suffices for C9 (Bonferroni), not the rate
- For k = 3: R3 = sum_rho (N/E - 1)(w - w_bar) (uniform part cancels exactly), so by Cauchy-Schwarz
  |R3| <= (sqrt(V)/E) * ||w - w_bar||_2 with V = sum_rho (N(rho) - E)^2 and ||w - w_bar||_2 ~ sqrt(log q)/(Cq) (lattice counting).
  If V << q^3 then R3 = O(sqrt(log q / q)) -> 0.  [INFERENCE]
- variance_identity2.py [VERIFIED numerically, q = 5..137]: V / (#good rho * E) = 1.9 .. 3.1 (prime m: 2.65, 2.77, 3.06, 3.10, 2.87)
  -> V ~ 3 * #rho * E ~ 3 q^3: Poisson with clumps of 3 (multiplier q maps triples to triples of the same ratio).
- Fourier view: N(rho) = #{x in F_{q^3}: [x][1-x]^rho = 1 in G = F_{q^3}^*/F_q^*}; V = line-count variance of the point set
  M = {(log x, log(1-x))} in (Z/m)^2. Expanding gives diagonal (|J|^2 = q^3 exactly) x 3 (Frobenius/multiplier c in {1,q,q^2})
  PLUS off-diagonal sums over c of sum_zeta J(zeta) conj J(c zeta) = point counts of curves of growing complexity in c ->
  the SAME uniformity obstacle reappears. Not closed.
- k >= 4: plain Cauchy-Schwarz loses (counts per ratio vector -> 0); needs a different decomposition.
Status: C9 via moments reduces to ONE uniform estimate (off-diagonal Jacobi-sum correlations); data strongly supports it.

## Variance law (2026-10-16) [VERIFIED numerically, m prime, q = 167..1373, 20 q]
N(rho) = 0 mod 3 for EVERY rho and every q tested (multiplier-q orbits of triples), and
V / ((m-2) E) = 2.94, 3.04, 3.01, 3.02, 2.99, 2.98, 2.99, 2.99, 2.99, 2.99, 3.00, 3.00, 3.00, 3.00, 3.01, 2.99, 3.00, 3.01, 3.00, 2.98
-> CONJECTURE V3: sum_rho (N(rho) - E)^2 = 3 (m-2) E (1 + o(1)), i.e. T(rho) = N(rho)/3 has Poisson variance (= mean) across rho.
V3 => R3 = O(sqrt(log q / q)) (Route V, Cauchy-Schwarz). Proof target: off-diagonal Jacobi-sum correlations sum_c sum_zeta
J(zeta) conj J(c zeta) over c not in {1, q, q^2} are o(q^3 m) in total.

## Exact identity (2026-10-16) [VERIFIED exactly, q = 5, 17, 41, 59; PROVED-SKETCH: pairs of same-ratio triples <-> unique affine map]
sum_{rho != 0,1} N(rho)^2 = sum_{lambda unit} sum_mu (I_lambda(mu))_3,  I_lambda(mu) = |S cap (lambda S + mu)|.
Multipliers lambda in {1, q, q^2}: lambda S = S + shift, so one mu gives I = n -> contributes exactly 3 (n)_3 = 3 (m-2) E,
which IS the variance term of Conjecture V3. Hence V3 <=> for NON-multiplier lambda the 3rd factorial moment of intersection
sizes |S cap (lambda S + mu)| over mu is Poisson-exact up to a total error o(q^3) (per-lambda counts ~ q^2, needed error o(q)
on average; random-sign heuristic gives q per lambda -> total q^2). Also: sum_mu (I_lambda)_2 = m - 1 EXACTLY for every lambda
(perfect difference set), i.e. second moments are exactly Poisson; the third moment is the first non-trivial one.

## Dual picture of dilate intersections (2026-10-16) [PROVED-SKETCH]
In the F_{q^3} model, lambda S + mu = log of g^mu * {x^lambda : x in L}. If lambda = sum e_i q^i (base-q digits, e_i >= 0) has
digit sum s, then x -> x^lambda maps the line L into a curve of degree s (Frobenius-twisted monomial), so by Bezout
I_lambda(mu) <= s (or the curve contains L). Examples: lambda in {1,q,q^2} (s=1): multipliers, I in {1, n}; lambda = -1 = q+q^2 mod m
and other s = 2 values: image is a CONIC -> I <= 2 -> (I)_3 = 0 (a deficit, the dual of the forbidden ratios).
Typical lambda has s ~ 3q/2 -> no Bezout control; the per-lambda Lang-Weil error O(q^{3/2}) is too weak (needed o(q) on average).
So the remaining step is a genuine "averaging over lambda" (family) estimate. Status: open; data (V3) strongly supports it.

## Kaggle 2026-10-19: V3 and per-lambda errors to q = 2969 [VERIFIED numerically, 37 q]
V/((m-2)E) = 3.000 +- 0.007 (all 37 q, 293..2969); N(rho) = 0 mod 3 always. Per-lambda 3rd-moment error (X_lambda - random
expectation): mean/q ~ 0 (|.| < 0.2, consistent with zero), sd/q = 4.14..4.35 CONSTANT in q (one outlier q=1181: 21.9, a special
lambda - to inspect). [CONJECTURE] sd(X_lambda - E) = sqrt(18) q (4.243 q). Random-sign over ~q^2 lambda then gives total o(q^3).
stepb-cert2: the 4 hard orbits (-5/3,-7/3,-7/4,-7/5) did not finish in 10 h each (no failure; sympy too slow).
- rama-lambda-all (ALL non-multiplier lambda, q = 167, 173, 293): the largest errors are exactly -(q-2) q = -pred, i.e.
  (I_lambda)_3 = 0 identically: the "dual-forbidden" lambda class (base-q digit sum 2 and its multiplier/inverse images,
  e.g. digit sums 2, (q+3)/2, q+1, 2q+1...). They make the error distribution heavy-tailed (kurtosis 300-1000); the bulk has
  sd ~ 4.24 q (sampled runs). Next: count the dual-forbidden class exactly and test bulk sd = sqrt(18) q.
- Smoke (q = 41, 59, all lambda): the dual-forbidden class has EXACTLY 9 elements = {-1, 2, 1/2} x {1, q, q^2} - the mirror of
  the forbidden ratios {-1, 2, 1/2} (Step 2) under the identity sum N^2 = sum (I)_3. Excluding them, the per-lambda errors are
  ~Gaussian (kurtosis 3.0 at q=59), sd 3.9-4.1 q. Kernel rama-lambda-bulk (q 300-460) READY to measure the bulk sd precisely.

## v4-identity (Kaggle 2026-10-19, ALL lambda, q = 41..383, m prime) [VERIFIED numerically]
Non-multiplier totals vs random-set expectation: ratio3 = 1.0001 (q=293, 383), ratio4 = 1.0002, 1.0003; deviation / multiplier
contribution: dev3/mult +0.008, +0.009 and dev4/mult +0.0001 at q = 293, 383 (shrinking with q). => the k=4 analogue
sum N(rho1,rho2)^2 = sum (I)_4 is Poisson-exact up to the multiplier term even more precisely than k=3: CONJECTURE V4.

## Prime-power q (2026-10-19, smoke q <= 64) [OBSERVATION]: V/(#good E) ~ 3k for q = p^k (27 -> 8.98, 64 -> 18.65, 25 -> 6.07)
=> variance law = order of the multiplier group {p^j} (clumps of size 3k). Registered test PLAN_PPV3 (q 121..1369) queued.
