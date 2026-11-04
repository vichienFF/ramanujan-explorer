# Theorem P4 = Theorem "multiplier 4" of Version 6 (consolidated proof overview, 2026-11-04; released with Version 6)
Released as the overview of a computer-assisted proof reviewed by AI referee instances only (no human expert yet). Step 5 (special classes,
P4_SPECIAL_LEMMA.md) is a proof sketch whose exceptional lists are computer-generated and checked; it is the least completely written part.
The section "Before any external use" at the end records the internal release checklist.

**Theorem.** Let q = p^n with p >= 7, m = q^2+q+1, S a Singer difference set in Z/m, I_4(mu) = |S ∩ (4S + mu)|. Then

  F3(4) := sum_mu I_4(mu)(I_4(mu)-1)(I_4(mu)-2) = (q-2)(q+1) + b_q,

where b_q = alpha^n + beta^n, alpha + beta = b_p, alpha beta = (-3/p) p^2, b_p = 4x^2 - 2p if p = x^2 + 3y^2, b_p = 0 if p = 2 mod 3
(the Frobenius traces of the CM newform 12.3.c.a). Equivalently P(4) = P(-2) (third moments of the multipliers 4 and -2 agree).

Status labels: [HAND] [SYM] [EXACT] [SOURCE] [INF]. Referees: five reviews of the proof (referee 2 on reproducibility, referees 1, 3, 4, 5 on mathematics) and two on the Version 6 paper (math, repro); all Claude Sonnet; no FATAL.

## 1. Reduction to a pencil count (P4_PROOF.md Steps 1-3, 5) [HAND + EXACT]
With t = y/(1-y) the members are c t^4 + d = (1+t)^4, (c,d) in (F*)^2. F3(4) = 3T with
T = (N1 - N2 + N3/3)[genuine simple members] + D3, and the degenerate (c+d=0) and repeated-root corrections are proved by hand
(Steps 5b-5d). N1 = (q-2)^2 + 2(q-1), N2 = q^2 - 4q + 10 + 5phi(-1) [HAND, Step 2]. The theorem is equivalent to

  N3 = q^2 - 7q + 19 + 18 phi(-1) + 9 phi(-2) + 6(1 + phi(-3)) + b_q.        (N3)

## 2. Main-term identity (Step 4w) [HAND, referee 3]
Ordered root pairs <-> (u,v) with weight 1 + chi(u^2-4v); the residual-quadratic discriminant is -4 D4(u,v)/den^2 for non-singular pairs:
N3 = q^2 + phi(-1)(S_a + S_b) + E, S_a = sum chi(D4), S_b = sum chi(u^2-4v) chi(D4).

## 3. The character sums
- Change of variables u = x-1, v = z + x^2/4 - x/2, m = 1-4z: D4 = H(x^2, m)/4 [SYM, Step 4v], so S_b = A + B, S_a = A' + B'.
- A = (1+phi(-1))q + chi(3), A' = 2q, B' = (1+phi(-1))q + chi(3) [HAND, node projection, Steps 4u, 4x; referee 3].
- **B = 2q + phi(-1)q + chi(3) b_q** (C-B) [HAND + SOURCE, P4_CB_PROOF.md]: elementary reduction to an elliptic K3 X (Step 1);
  rho(X) = 20 by exact Shioda heights; |disc NS| = 48 -> CM by Q(sqrt-3); trace formula; Livne 1995 (modularity, det) and the
  Livne 1987 criterion with S = {2,3,5} (test primes <= 73 suffice, Schuett 1112.0405 §2.8) -> trT = chi(3) b_q.
  [Good reduction for p >= 7 and the trace decomposition written out 11-04 (p4_goodred.py; referee 5: no FATAL/SERIOUS, MINOR fixed).]
Hence S_a = (3+phi(-1))q + phi(-1)phi(-3), S_b = (3+2phi(-1))q + phi(-1)(phi(-3) + b_q).

## 4. The exclusion term E (Steps 4w-4zb) [HAND, referee 3]
E = generic (0) + c/d=0 (-6(1+f1)q + 24(1+f1)) + diagonal (-q + 3f2) + singular (-11(1+f1)) + SPEC - T_{-1},
T_{-1} = 2(q-1) - 2chi(-7) - 2f3 [HAND]; f_a = phi(-a).

## 5. The special-class term SPEC (P4_SPECIAL_LEMMA.md) [HAND + SYM + EXACT, referee 4]
SPEC(q) = -q + 10 + 5f1 + 6f2 + 2f3 - 2chi(-7) for all q = p^n, p >= 7: the three special classes live on smooth conics with
Q-rational square roots of -D4; weights are constant off explicit finite exceptional sets defined over L = Q(i, sqrt2, sqrt-3, sqrt-7)
(table: p4_exc_table.py), collisions only at {2,3,5,7,13}; so SPEC = A(sigma)q + B(sigma). Two q per Frobenius class of Gal(L/Q)
(all 16 classes; identity class 193, 337, 457, 673) and n odd/even at p = 7 (7, 343 | 49, 2401), p = 13 (13, 2197 | 169, 28561) fix it.

## 6. Conclusion
Sections 2-5 give (N3); with Section 1 the theorem follows for q = p^n, p >= 7.

## Evidence table (all exact, registered/blind where stated)
- (N3) at all 2259 primes 7..19999 (43 + 623 + 1593; corrected 11-04, E97) (blind 211..19999: H-N3-BIG, H-N3-HUGE) and q = 49, 121, 125, 169, 343, 2197, 2401, 28561, 3125, 15625.
- F3(4) directly from Singer sets: primes 7..139, q = 25, 49, 121, 125 (H-P4-SCOPE blind).
- C-B: primes 7..1500, prime powers 49..1331; trT = (3/p) b_p for 7..420.

## Outside the theorem
- p = 5: formula verified at 5, 25, 125 (F3) and 5..15625 (N3); proof route via supersingular reduction (Charles' Tate) - incomplete.
- p = 3: F3(4) = q(q-2+(-1)^n) (blind to 729); N3 law (blind to 19683) - no proof.

## Before any external use (RULES 24)
final LaTeX text + pub_gate.py PASS + math and repro referees on the FINAL text + G1 remainder (MathOverflow) + human expert review;
the user decides on publication (V6 or separate note).
