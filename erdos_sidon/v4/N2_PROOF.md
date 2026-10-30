# N(−2) for the l = −2 family — proof write-up (draft 2026-10-30; internal independent review 2026-10-30: no errors, 6 fixes applied — INDEPENDENT_REVIEW_N2.md)

**Setting.** q ≥ 5 prime, χ = φ the quadratic character of F_q. For c, d ∈ F_q* put
Q_{c,d}(y) = y²(1−y)² − c(1−y)² − d y² = y⁴ − 2y³ + (1−c−d)y² + 2cy − c.
N(−2) := #{(c,d) ∈ (F_q*)² : Q_{c,d} = (linear)·(irreducible cubic) over F_q}.
b_q := 0 if q ≡ 2 (mod 3); b_q := 4x² − 2q if q = x² + 3y² (q ≡ 1 mod 3)  [= a_q(η(2τ)³η(6τ)³), checked 44 primes].

**Theorem.** N(−2) = ((q−2)(q+1) + b_q)/3. In particular for q ≡ 2 (mod 3): N(−2) = (q−2)(q+1)/3 and
P(−2) = (q−2)² + 3N(−2) = (q−2)(2q−1).
Status: q ≡ 2 (mod 3) complete modulo ONE citation (value of 3F2(4): [BK] Thm 1.7, statement read; S = φ has order 2, allowed);
q ≡ 1 (mod 3): complete modulo the same citation plus two textbook facts (Hasse–Davenport; cubic character of 2), Step 7 below. [review fix 6; V4 pre-publication review fix 1]

## Step 1 — roots and pairs
Q(0) = −c ≠ 0, Q(1) = −d ≠ 0, so all F_q-roots lie in S = F_q∖{0,1}. For y ∈ S the condition Q(y)=0 is a line in (c,d)
meeting c=0, d=0 at distinct nonzero points → q−2 admissible (c,d) per root: Σ_{(c,d)} #roots = (q−2)².
For distinct y1, y2 ∈ S: det = (y2−y1)(y1+y2−2y1y2), c = y1²y2²(y2−y1)(2−y1−y2)/det, d = (1−y1)²(1−y2)²(y2²−y1²)/det
(sympy-checked, n2_types.py). With u = y1+y2, v = y1y2 the pair is admissible iff 2v ≠ u, u ≠ 2, u ≠ 0.
If det = 0 the two root-lines in the (c,d)-plane are parallel and distinct, so no (c,d) has both roots; conversely any two
distinct roots of some Q_{c,d} (c,d ≠ 0) form an admissible pair. [review fix 1]

## Step 2 — P := #admissible unordered pairs = (q−3)(q−5)/2
For y ∈ S the forbidden partners are −y, 2−y, y/(2y−1): pairwise distinct, each in S∖{y} except for exactly one y
(y = −1, 2, 1/2 resp.), and the relation is symmetric. Ordered pairs: (q−2)(q−3) − 3(q−3).

## Step 3 — residual quadratic and S2
For an admissible pair, Q = (y²−uy+v)(y²−sy+p), s = 2−u, p = −c/v, and (sympy, n2_disc.py)
disc = s²−4p = u(u−2)(2v−u+2) / (2v−u) ⇒ χ(disc) = χ(D), D := u(u−2)(2v−u)(2v−u+2).
S2 := Σ_{admissible pairs} χ(disc). Over all (u,v) ∈ F_q², weight (1+χ(u²−4v))/2 (=1 split pair, ½ diagonal):
Σ_{u,v} χ(D) = [Σ_u χ(u(u−2))][Σ_w χ(w(w+2))] = 1 and Σ_{u,v} χ(u²−4v)χ(D) = T (Step 4).
Excluded sets: v=0 (root 0): contributes 2q−4; v=u−1 (root 1): 2q−6 (the point (u,v)=(1,0) lies on both lines and is
counted once, on v=0); diagonal u²=4v: χ(D)=χ((u−1)²+3) → −3 (it meets the other lines only where D = 0) [review fix 2];
det/c/d=0: factors of D → 0. Hence S2 = (1 + T − (4q−13))/2 = (T − 4q + 14)/2. (n2_lines.py, 9 primes.)

## Step 4 — T = 1 + φ(−1)·G(4)
With x = u−1, z = 2v−u+1: T = Σ_{x,z} χ((x²−1)(z²−1)(x²+1−2z)). Put z = 1−2t, s = x², r = 1−s:
T = Σ_r (1+χ(1−r)) χ(−r) Σ_t χ(t(t−1)(4t−r)). The "1" part equals −Σ_t χ(t(t−1)) = 1; the other part equals
φ(−1)·G(4), G(λ) := Σ_{x,y} φ(x)φ(y)φ(1−x)φ(1−y)φ(x−λy). (Numerically T = q+1+b_q, 11 primes.)

## Step 5 — repeated roots
Q = (y²−y+m)² forces m = 1, (c,d) = (−1,−1): type (1)²(1)² iff −3 is a square (Dd = 1 if q≡1, else 0; for q≡2 the
point (−1,−1) has type (2)², which, like (2)(2) and (4), has no F_q-root and contributes to none of the identities).
Every E- or C-point has exactly one double root, so a ↦ (c,d) is injective on them; it is 2-to-1 only onto (−1,−1).
Also R_a(0) = −a ≠ 0 and R_a(1) = a ≠ 0, so the other roots lie in S. [review fix 3]
A double root a ∈ S forces c = a³, d = −(a−1)³, Q = (y−a)² R_a, R_a = y²+2(a−1)y−a, disc R_a = 4(a²−a+1),
R_a(a) = 3a(a−1) ≠ 0 (no triple roots). Σ_{a∈S} χ(a²−a+1) = −1 − 2 = −3, z0 := 1+χ(−3) ⇒
E := #(1)²(2) = (q+1−z0)/2, C := #(1)(1)(1)² = (q−5−z0)/2, Dd = z0/2. (n2_double.py.)

## Step 6 — inclusion–exclusion
Types: N=(1)(3), E, A=(1)(1)(2), B=(1)(1)(1)(1), C, Dd=(1)²(1)² [review fix 4: renamed]. Counting roots, pairs and χ(disc) per type:
(q−2)² = N+E+2A+2Dd+3C+4B,  P = A+Dd+3C+6B,  S2 = −A+Dd+2C+6B
⇒ N = (q−2)² − E − (4/3)P + (2/3)S2 − C/3 − (4/3)Dd.
Substituting Steps 2–5 and T = q + 1 + b_q (Step 7) gives N = ((q−2)(q+1) + b_q)/3 in both classes
(sympy: difference 0 in each class; n2_assemble.py: all identities and N exact on 9 primes).

## Step 7 — the hypergeometric value (citations)
[G] (elementary, review fix 5) q²·3F2(φ,φ,φ;ε,ε | 4) = φ(−1)·G(4): expand (φχ over χ) = χ(−1)/q·Σ_{y≠0,1} φ(y)χ(y/(1−y));
orthogonality gives q²·3F2(4) = Σ φ(y1y2y3) over y_i ∈ S with (1−y1)(1−y2)(1−y3)+4y1y2y3 = 0; solve for y3, put
t_i = y_i/(1−y_i) = −x_i: Σ_{x,y} φ(x(1−x)y(1−y)(1−4xy)); and x ↦ 1/x in G(4) gives φ(−1) times the same sum.
(Reviewer's proof; numerics 14 primes, n2_greene_norm.py + review_n2/rv_bruteforce.py.)
[BK] Barman–Kalita, arXiv:1208.0495, Thm 1.7 with S = φ (order 2, allowed): for q ≡ 2 (mod 3), 3F2(4) = −φ(−3)φ(16)/q = 1/q
(checked 5 primes) ⇒ G(4) = φ(−1)q ⇒ T = q + 1 ⇒ b_q = 0 term. S = φ recovers Ono, Trans. AMS 350 (1998) 1205–1223.
For q ≡ 1 (mod 3), [BK] Thm 1.7 with S = φ gives 3F2(4) = B² − 1/q with B = (φχ3 over χ3) + (φχ3² over χ3²), (A over B) = B(−1)/q·J(A, B̄).
Then qB = J(φχ3, χ̄3) + conj = 2 Re J(φχ3, χ̄3). Hasse–Davenport (g(χ3)g(φχ3) = χ̄3(4)g(χ3²)g(φ)) and g(χ3)g(χ3²) = q give
J(φχ3, χ̄3) = χ3(2)·conj J(χ3,χ3). Writing J(χ3,χ3) = a + bω (a ≡ −1, b ≡ 0 mod 3; Ireland–Rosen ch. 8), the associate χ3(2)J(χ3,χ3) is the
one congruent to 1 mod 2 (cubic character of 2, Ireland–Rosen ch. 9), so its real part is ±x with q = x² + 3y². Hence (qB)² = 4x² and
q²·3F2(4) = 4x² − q = q + b_q. Each step verified on 11 primes 7..97 (n2_jacobi.py, n2_bk1.py, CONTROL PASS).

## Open items before any external claim
1. DONE: [G] proved elementarily (Step 7).
2. DONE: q ≡ 1 (mod 3) step written above (Ono 1998 full text still not read; the statement is used via [BK] Thm 1.7, a preprint).
3. DONE (internal): independent review 2026-10-30 — all steps correct, 6 fixes applied; theorem brute-forced on 14 primes 5..53.
4. Before any PUBLIC claim: human expert review (an internal AI review is not peer review).
Scripts: erdos/stepb/n2_*.py, fq3.py (all with CONTROL lines). Proof log: PROOF_STATUS.md steps 1–11.
