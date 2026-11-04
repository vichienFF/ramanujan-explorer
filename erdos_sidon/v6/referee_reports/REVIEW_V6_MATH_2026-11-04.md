# AI referee report (mathematics) on the Version 6 draft — Claude Sonnet, 2026-11-04
Verdict: no FATAL; two SERIOUS wording/packaging items; several MINOR items. (Report text condensed by the author; all items listed.)

Independent checks by the referee: b_q recurrence reproduces a_p of eta(2t)^3 eta(6t)^3 for p = 7, 13, 19, 31, 37, 43; b_q = 2q / 0 for p = 2 mod 3;
identity (q-2)(2q-1)+b_q-(q-2)^2 = (q-2)(q+1)+b_q; brute force on Singer sets q = 7, 11, 13: sum (I_4)_3 = sum (I_-2)_3 = 42, 108, 132; (N3) re-derived at
q = 343, 2197, 2401, 28561, 5^5, 5^6; counts 666 + 878 + 715 = 2259 = pi(20000) - 3; char-3 law against p4_scope.out.

(a) Theorem statement: OK.
(b) SERIOUS: "the full proof is in the release" overstates: P4_FULL_PROOF.md was headed "internal draft", P4_SPECIAL_LEMMA.md is a proof sketch whose
    step-5 list was tagged INF. Say that step (5) is released as a proof sketch with computer-generated exceptional lists, the least completely written part.
    MINOR: heights give rank >= 2; rho = 20 because rho <= h^{1,1} = 20.
    SERIOUS (attribution): modularity is Livne [Li95]; the determinant eps_K * chi_cyc^2 is our short argument (P4_CB_PROOF.md Step 5), not checked by an expert.
    MINOR: cite [Li87, Thm 4.3 and Prop 4.11].
(c) Numbers and ranges accurate. MINOR: say the 43 primes 7..199 were checked before registration.
    SERIOUS: separate characteristic 5 (125, 3125, 15625; and 25, 125 in the direct third-moment list) from the p >= 7 evidence; ship outputs for the
    essential p = 7, 13 checks (343, 2197, 2401, 28561) and for 3125, 15625.
(d) MINOR: abstract (vi): define b_q = alpha^n + beta^n explicitly (not a_q for n > 1); mark "computer-assisted; reviewed by AI instances only"; punctuation.
    MINOR: the uncited "closest work" sentence: cite or delete. MINOR: corollary count wording ("adds the class {4, 1/4}").
    MINOR: say the K3 of the new section is a different surface from the heuristic diag(2,6) one. MINOR: observation bullet "(proved by computation, not by a symmetry of P)".
    MINOR: phi = chi duplicate notation; add End_Hodge(T) = Q(sqrt-3). MINOR: "Changes in Version 6": only report 5 of the earlier referees is released in full.
    Status: five referees = four on mathematics, one on reproducibility.
(e) Bibliography: Li87, Li95, Sch09, Shi look right; Sch12 (arXiv:1112.0405): confirm author/title; add journal data if published.
