# C-B: proof draft (2026-11-03), for referee review — INTERNAL, not for release

**Claim C-B.** Let q = p^n with p >= 7, chi = quadratic character of F_q, phi(a) = chi(a), and
H(s,m) = m^3+8m^2-3ms^2+6ms+13m+2s^3+2s^2-10s+6. Then

  B(q) := sum_{s,m in F_q} chi(s m H(s,m)) = 2q + phi(-1) q + chi(3) b_q,

where b_q = alpha^n + beta^n with alpha, beta the Frobenius eigenvalues at p of the Galois representation of the CM newform 12.3.c.a (alpha+beta = b_p, alpha*beta = (-3/p)p^2; b_p = 4x^2 - 2p if p = x^2+3y^2, b_p = 0 if p = 2 mod 3, so then b_q = 2q for even n and 0 for odd n). NOTE: b_q is NOT the newform coefficient a_{p^n} (referee 11-03).
(Equivalent to the earlier form B = G(4) + 2q via the separately checked control 1 + phi(-1) G(4) = q + 1 + b_q, because phi(-1) = chi(3) whenever b_p != 0.)

Labels: [HAND] derived by hand, [EXACT] exact computer check, [NUM] numerical evidence only, [SOURCE] literature, to cite exactly.

## Step 1 — elementary reduction to an elliptic surface [HAND + EXACT]
1. H(1,m) = m(m+4)^2, so the line s=1 contributes sum_m chi(m^2(m+4)^2) = q-2.
2. For s != 1 put m = -4 + k(s-1) (projection from the node (1,-4) of H=0); then H = (s-1)^2 L_k(s), L_k(s) = (k-1)^2(k+2)s - (k-2)(k+3)^2, so
   B = (q-2) + sum_k sum_{s != 1} chi(f_k(s)),  f_k(s) = s (k(s-1)-4) L_k(s).
3. f_k(1) = 16(k^2-5), and sum_k chi(k^2-5) = -1 (Jacobsthal, 5 != 0 in F_q).
4. For A := k(k-1)^2(k+2) != 0, the substitution x = A s gives f_k(s) = A^{-2} x(x-e1)(x-e2), with
   e1 = (k-1)^2(k+2)(k+4), e2 = k(k-2)(k+3)^2, so sum_s chi(f_k(s)) = S_k := sum_x chi(x(x-e1)(x-e2)).
5. k = 0, 1, -2: both sides equal -phi(-2), -1, -phi(-2) respectively (direct evaluation).
   => **B(q) = q - 1 + sum_{k in F_q} S_k.**  [EXACT: q = 7,11,13,19,31,49,121; p4_bookkeep.sage.py. Fails for char 3 (k=1=-2 merge); char 5 holds by cancellation of the two 5-terms.]

## Step 2 — the elliptic K3 surface X [HAND + EXACT]
E_k: Y^2 = X(X-e1)(X-e2) over P^1_k, deg e_i = 4 -> weights of a K3 fibration. e1-e2 = 8(k+1).
Singular fibres: I4 at k=1 (ord e1 = 2), k=-3 (ord e2 = 2); I2 at k=-2,-4 (e1), 0,2 (e2), -1 (e1-e2); I6 at k=infinity (e1'-e2' has order 3 in t=1/k). Euler number 2*4+5*2+6 = 24 -> K3. [HAND]
**Good reduction for p >= 7** [HAND + EXACT, written 2026-11-04; p4_goodred.py, control = char-0 configuration PASS]:
Let W be the Weierstrass model Y^2 = X(X-e1)(X-e2) over P^1_{Z_(p)}, p >= 7 (2 is a unit).
(a) Places. Delta = 16 e1^2 e2^2 (e1-e2)^2; e1, e2 have leading coefficient 1 and e1 - e2 = 8(k+1). The zeros are the 7 integer places
{1,-2,-4,0,2,-3,-1} plus infinity (t = 1/k: e1-e2 -> 8t^3(1+t)). Pairwise differences have prime factors in {2,3,5}, so the 8 places are
Z_(p)-sections with distinct reductions; every other fibre is smooth in both characteristics (the cubic has distinct roots).
(b) Local form. At each place exactly two of the roots 0, e1, e2 meet, with difference t^m g(t); the third root is at distance u from the
node. (m, g(0), u(0)): k=1 (2,15,16), k=-3 (2,15,16), k=-2 (1,18,-8), k=-4 (1,-50,-24), k=0 (1,-18,-8), k=2 (1,50,-24), k=-1 (1,8,12),
inf (3,8,1). All are {2,3,5}-units, so near the node section the equation is Y^2 = unit*(X'^2 - unit*t^{2m}): an A_{2m-1} point along a
Z_(p)-section, fibre I_{2m} in characteristic 0 and p (c4 = 16(e1^2 - e1e2 + e2^2) is a unit at the node). Euler number 24 in both.
(c) Smoothness. W is smooth over Z_(p) away from the 8 node sections (the point [0:1:0] at infinity of each cubic is smooth: in the chart
Y = 1 the equation is Z = X^3 + ..., with dF/dZ = 1). Along each node section Y^2 = w(X'^2 - t^{2m} h^2) with w, h units; etale-locally
(2, w units) this is uv = t^{2m} x Spec Z_(p), independent of p (3 need not be a unit: no m-th root is taken). Blowing up the reduced
singular section m times (commutes with etale base change) resolves generic and special fibre simultaneously, the exceptional chain has
2m-1 components, each a Z_(p)-flat divisor, so component classes and their Frobenius action specialise from characteristic 0. Minimality:
all bad fibres are I_n with ord Delta = n and the Euler number is 24. So X -> Spec Z_(p) is smooth proper, X_Q is the K3 of Step 2, X_{F_p} the minimal resolution of W_{F_p},
and smooth proper base change gives H^2_et(X_Qbar, Q_l) = H^2_et(X_Fpbar, Q_l), Frob_p-equivariant (inertia acts trivially).
(referee MINOR 2 — now written out; for the final referee to re-read.)

## Step 3 — trace formula [HAND]
Point counts of fibres: smooth -> q+1-a_v; split I_n -> nq; non-split I_n (n even) -> 2(q+1); a_v = +-1 for multiplicative fibres (a_v = -sum_x chi(cubic) in all cases). With t_v = trace of Frobenius on non-identity components and H^2 = NS(x)Q_l + T(x)Q_l, Lefschetz gives
   - sum_{v in P^1(F_q)} a_v = q * m(q) + tr(Frob_q | T),  m(q) = trace of Frob_q on MW(X)(x)Q.
a_inf = 1 (node at x=1, sum_x chi(x(x-1)^2) = -1). T(x)Q_l is the orthogonal complement of NS(X_Qbar)(x)Q_l, taken from characteristic 0 via smooth proper base change; it is unaffected by the jump to rho = 22 (supersingular reduction) for p = 2 mod 3 (referee MINOR 3).
**Trace decomposition (written 2026-11-04; referee 5 fixes applied: sign and twist) [HAND]:** by (c) of Step 2,
V := H^2_et(X_Fpbar, Q_l) = H^2_et(X_Qbar, Q_l) (untwisted, weight 2, matching |alpha| = p) as Frob-modules.
The specialization map NS(X_Qbar) -> NS(X_Fpbar) is injective and compatible with cycle classes, so N := NS(X_Qbar)(x)Q_l is a Frob-stable
subspace of V; the cup product is non-degenerate on N (Hodge index), so V = N + T with T := N^perp also Frob-stable. N is spanned by the zero
section, a fibre, the non-identity components of the 8 reducible fibres (all Frob-fixed: the places are rational and the components of
I_n are fixed exactly when the fibre is split; non-split fibres contribute the t_v of the point count) and MW(X)(x)Q. Grothendieck-Lefschetz,
#X(F_q) = 1 + tr(Frob_q | V) + q^2 = (q+1)^2 + q sum t_v + q m(q) + trT(q), against the fibre count sum_v #X_v = (q+1)^2 - sum a_v
+ q sum t_v (split I_n: nq = (q+1) - 1 + q(n-1); non-split I_n, n even: 2(q+1) = (q+1) + 1 + q*1), gives -sum_v a_v = q m(q) + trT(q)
(trT(q) := tr(Frob_q | T), untwisted; referees 1 and 5 re-derived this; numerically B = q - sum a_v holds at p = 7..19). If rho(X_Fpbar) = 22 the extra
algebraic classes lie inside T, which changes nothing above (T is defined from characteristic 0). [Referee re-derived this formula independently: OK.] Combining with Step 1: **B(q) = q - sum_v a_v = q + q m(q) + trT(q).**

## Step 4 — Neron–Severi [EXACT]
- Trivial lattice U + A3^2 + A1^5 + A5, rank 18, |disc| 3072. Torsion contains (Z/2)^2 (no 4-torsion: -e1, -e2, e1, e1-e2, e2 are not squares in Qbar(k)).
- 11 sections X = c*monomial (p4_picard.py); exact Shioda heights over Q(i)(k) (p4_shioda.sage.py; controls: torsion h=0, h(2P)=4h(P), h(P+T)=h(P)): Gram rank exactly 2, Z-span Gram diag(3/2, 1/6). So rho = 20 (singular K3), |disc NS| = 48/n^2 for the index n of our span in the full MW (n unknown, irrelevant below).
- Galois: sections are defined over Q(i); sigma(i -> -i) acts as diag(-1,+1) on the span (p4_mwgal.sage.py, controls sigma fixes Q-rational P1, sigma^2 = 1). Hence **m(q) = 1 + phi(-1)**.
  => B(q) = 2q + phi(-1) q + trT(q). [also NUM: 43/43 primes 7..199, p4_trT.py]

## Step 5 — identify trT [SOURCE + HAND + EXACT]
- T is rank 2 with |disc T| = 48/n^2 in {48, 12, 3}, always 3 * square -> CM field K = End_Hodge(T(x)Q) = Q(sqrt(-3)). det of Frob_p on T(x)Q_l = eps_K(p) p^2 = (-3/p) p^2 = det rho_f for f = 12.3.c.a. Argument (referee sketch, to write out): G_K acts on T_l through SO(T_l) (commutes with the CM action), elements of G_Q \ G_K act by reflections (conjugate the K-action on H^{2,0}), hence det = eps_K * cyclotomic^2. [SOURCE, read 2026-11-03 (arXiv math/0511228 full text): Livne, "Motivic orthogonal two-dimensional representations of Gal(Qbar/Q)", Israel J. Math. 92 (1995) 149-156, Thm 1.3 + Ex. 1.6: a singular K3 over Q is modular, L(T_X,s) = L(f,s) for a weight-3 newform with CM by Q(sqrt(-d)), d = disc T_X (so rho_T is induced from a Hecke character of K and det = eps_K * cyclotomic^2); Schuett, "CM newforms with rational coefficients", Ramanujan J. 19 (2009) 187-205, Prop. 7.1: classification by d up to squares = by newform up to twist = by CM field Q(sqrt(-d)). For us d in 3*squares -> CM by Q(sqrt-3), consistent with 12.3.c.a up to twist; the twist is pinned by the Livne trace comparison below.]
- Parity [HAND]: trT(p) = -sum a_v - p(1+phi(-1)); smooth-fibre a_v = p+1 - #E_k == 0 mod 2 (full rational 2-torsion); 8 multiplicative fibres give 8 terms +-1; so trT is even. b_p = 4x^2-2p is even.
- Livne's criterion [SOURCE: Livne, "Cubic exponential sums and Galois representations", Contemp. Math. 67 (1987), Thm 4.3]: S = {2,3,5}; quadratic characters unramified outside S are generated by -1,2,3,5, test set T = {7,11,13,17,19,23,29,31,41,43,53,61,71,73,83} (livne_T.py) PLUS the identity class, represented by p = 241 (all of -1,2,3,5 squares) — T must be 'non-cubic' in the sense of Livne Prop. 4.11 (cite Thm 4.3 AND Prop 4.11). [SOURCE, read 2026-11-03: Schuett, "Modularity of Maschke's octic and Calabi-Yau threefold", arXiv 1112.0405, §2.7-2.8: for the SAME bad set {2,3,5} and K = Q(i, sqrt2, sqrt-3, sqrt5) the full representative set is exactly our 16 primes, and by [L, Prop 4.11] 83 and 241 may be omitted from the non-cubic set, so equal traces at p <= 73 suffice; reference [L] = R. Livne, Cubic exponential sums and Galois representations, Contemp. Math. 67 (1987) 247-261. Schuett also notes the even-trace hypothesis can be checked at p in {7,11,13,19} via the C3/S3 fields unramified outside {2,3,5} (Jones tables); we prove evenness for all p by hand instead.] Semisimplicity: rho_f is semisimple (Ribet); rho_T is semisimple since its restriction to G_K is abelian (CM) — so isomorphism, not only of semisimplifications. On T, trT(p) = chi(3) b_p holds [EXACT: p4_trT.py 7..199 (43 primes) and 200..420 (35 primes, incl. 241; rerun 11-03 after referee)]. No residual-image hypothesis is needed beyond even traces + equal det (referee). Same det, even traces => rho_T^ss = (rho_f (x) (3/.))^ss, so trT(q) = chi(3) b_q for all q = p^n, p >= 7.

## Conclusion
B(q) = 2q + phi(-1) q + chi(3) b_q for q = p^n, p >= 7. Referee also checked prime powers directly: q = 49, 121, 169, 343 exact.
**Referee 1 (Sonnet, 2026-11-03): no FATAL/SERIOUS; correct for p >= 7 modulo citations; MINOR items 1-6 applied above.**
**Referee 2 (repro, Sonnet, 2026-11-03): every cited computation reproduces exactly; no numeric discrepancy.** Fixes applied: 200..420 run now `python p4_trT.py 200 421` (35/35); Jacobsthal control no longer skipped (a=2 always, a=5 when 5 does not divide q); trivial-lattice |disc| 3072 printed by p4_shioda.sage.py. Theory steps without scripts (by nature): rho <= 20 in char 0 (h^{1,1} = 20), no 4-torsion (non-square check, hand), Kodaira/good reduction, Lefschetz trace formula, det/CM argument, parity — all covered by HAND/SOURCE labels above. Note: p4_char35's control values B(7)=5, B(13)=17 also come from the independent numpy implementation p4_trT.py (mod-p arithmetic), not only from the same Sage evaluator.
**Open:** char 3 (C-B holds numerically at 9..243, needs own proof) and char 5 (C-B FALSE at 5, 25, 125); exact citations (Livne Thm 4.3 + Prop 4.11; det source); full write-up of good reduction + det argument; second referee (repro) before any external use.
