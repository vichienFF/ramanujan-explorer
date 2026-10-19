# Literature check (full text where possible): R1-R5, Singer dilates / Erdos #30 (Guy C9)

Date: 2026-10-19. Reviewer: independent sub-agent (adversarial prior-art search).
Labels: SOURCE = seen in a document I read; INFERENCE = my own reasoning, not stated in a source.

## Verdict table

| Claim | Verdict | Closest prior art |
|---|---|---|
| R1 universal curve + Weil, forbidden ratios -1, 2, 1/2 | **PARTIALLY KNOWN**: forbidden ratios are folklore/known; the curve + Weil count was NOT FOUND | Sidon definition (O'Bryant survey); Jungnickel-Vedder 1984 via Chan-Law-Wong 2011 |
| R2 moment deficit law (3-APs + parallelograms) | **NOT FOUND** | none (window-count technique only in Erdos-Turan / Carter-Hunter-O'Bryant upper-bound proofs) |
| R3 variance law 3(m-2)E, 3k(m-2)E | **NOT FOUND** (multiplier-q orbits of triples are known in another context) | Herron 2025 (arXiv 2502.09536) uses multiplier-q orbits of triples |
| R4 identity + 9 null dilates + degree-s curves / Bezout | **PARTIALLY KNOWN**: -D is an arc, 2D an oval/conic is classical; the identity and the full 9-element list were NOT FOUND | Jungnickel-Vedder 1984; Chan-Law-Wong 2011 Sec. 2, 4 |
| R5 Poisson convergence would imply unbounded h(N)-sqrt N | **PARTIALLY KNOWN as strategy, NOT FOUND as a reduction** | Green's open problems list (Problem 31 comments + Problem 32); Zhang 1994; Lindstrom 1998; Dimitromanolakis 2002; Rokicki-Dogon; Shakan 2020 |

## R1: universal curve / Weil / forbidden ratios
- SOURCE: O'Bryant, "A complete annotated bibliography of work related to Sidon sequences", Electron. J. Combin. Dynamic Survey DS11 (2004), Sec. 1. A Sidon set has every nonzero difference represented at most once. INFERENCE: so a 3-AP a,b,c (a-b = b-c) is impossible. That gives N(-1) = N(2) = N(1/2) = 0, a known triviality.
- SOURCE: Chan, Law, Wong, "On polar ovals in abelian projective planes", Innov. Incidence Geom. 12 (2011), Sec. 2 and Sec. 4 (they cite Jungnickel-Vedder, Europ. J. Combin. 5 (1984) 143-148). For a planar abelian difference set D, -D is always an arc, and 2D is an oval when q is odd. So -1 and 2 are never multipliers, and Lemma 4.4 says -2 is never a multiplier. This is the geometric form of the forbidden ratios.
- SOURCE: Hung-Kang, arXiv 2609.14332 (full HTML read). They prove a 2 sqrt(q) bound for odd multiplicative Fourier coefficients of a square-class lift of the Singer set from the trace conic (Thm 1.1), and a Ramanujan double cover (Thm 1.2). The paper has no triple counts, no ratio equation, no curves s^a r^b t^c = 1 and no dilates. The method is similar in kind (Weil on a curve tied to a Singer set), but the object is different.
- SOURCE: Momihara-Xiang, arXiv 2110.10959 (FFA; full PDF text read). Thm 3.1 says the cyclotomic class C0(N,q^3)/F_q is an M-arc in PG(2,q) for p large, proved with Do Duc-Leung-Schmidt cyclotomic-number bounds (Props 3.3, 3.4). Thm 1.2 is about srg existence via Gauss periods. Nothing on ratio-counts of triples or Weil point counts of our curve family.
- SOURCE: Forey-Fresan-Kowalski, arXiv 2301.12878 (full HTML read via summary). They build Sidon sets from generalized Jacobians, and the Singer set appears as the torus k3^x/k^x (Sec. 3). Only the Sidon equation is studied. No dilates, no curve C_{a,b,c}.
- SOURCE: Eberhard-Manners, arXiv 2107.05744 (EJC 2023; full text read via summary). Dense Sidon sets come from projective planes. No dilates, triples or windows.
- SOURCE: Evans-Hollmann-Krattenthaler-Xiang, math/9807029 (JCTA 87, 1999; abstract only). This covers 2-ranks of (2^d-1, 2^{d-1}-1, 2^{d-2}-1) difference sets, i.e. Singer-PARAMETER sets in char 2 from hyperovals, via Stickelberger. It has no triple counts and is not about planar Singer sets. Not relevant.
- Verdict: the reduction N(rho) = #C_{u-v,v,-u}(F_q) - diagonal and the O(q^{-1/2}) estimate were NOT FOUND.

## R2: forbidden-structure law for factorial moments
- NOT FOUND in any source read. SOURCE: Carter-Hunter-O'Bryant, arXiv 2310.20032 (full PDF text read), and Erdos-Turan/Lindstrom use window counts of a Sidon set in [0,n) for UPPER bounds. These are deterministic variance arguments, not factorial moments over random dilates. Chmelnitzki (2005 essay for B. Green, full text read) studies only the distribution of arguments of Fourier coefficients of Singer sets under dilation (Sec. 2-3). He makes discrepancy conjectures 3.4-3.5, but these are not window-count moments.

## R3: variance law
- NOT FOUND. Related: SOURCE: Herron, "Triangle presentations encoded by perfect difference sets", arXiv 2502.09536 (read to 100k of 125k chars). Thm 2.4 and Lemma 2.2: orbits of triples (j, j+d, j+d+qd) under the multiplier q. This is the same multiplier-orbit "clump of 3" structure, used for buildings/lattices with no statistics. INFERENCE: the clump explanation in R3 rests on a known symmetry, but the variance asymptotic is new as far as I found.

## R4: identity, nine null dilates, Bezout degrees
- SOURCE (see R1): -D is an arc, and 2D is an oval and hence a conic in the Desarguesian case (Segre). Chan-Law-Wong Sec. 4 says this explicitly and attributes it to Jungnickel-Vedder 1984. INFERENCE: so |D cap (lambda D + mu)| <= 2 for lambda in {-1, 2} and its multiplier orbit, i.e. (I)_3 = 0. Part of the "9 null dilates" is classical. The 1/2 case follows by inversion.
- SOURCE: Momihara-Xiang Thm 3.1 / Remark 3.2 (Maruta 1995, Szonyi 1996): cyclic arcs from x -> x^{N} type maps. This is related "power maps send lines to curves" geometry, but not our digit-sum degree statement.
- Arasu-Davis-Jungnickel-Pott, "A note on intersection numbers of difference sets", Europ. J. Combin. 11 (1990) 95-98: abstract only. It gives a necessary condition used for non-existence, not Singer-specific counts.
- The identity sum N^2 = sum over affine maps of (I)_3 is INFERENCE-level standard double counting. NOT FOUND stated for Singer sets. The exact claim that there are only 9 non-multiplier lambda with (I)_3 = 0 was NOT FOUND.

## R5: Poisson -> unbounded excess (Erdos #30 / Guy C9)
- SOURCE: B. Green, 100 open problems (version updated Jan 2026, full PDF text read), Problem 31 comments. The lower bound comes from unwrapping a modular Sidon set, and Green says a suitable dilation ought to do this more efficiently. He then poses **Problem 32**: does some dilate of a sqrt(p)-size set in Z/pZ have a gap of length 100 sqrt(p)? So the dilate strategy for beating sqrt N is explicitly in the literature as an open direction.
- SOURCE: Shakan, "A large gap in a dilate of a set", arXiv 2004.14828 (full HTML read). Some dilate has a gap >= 2p/|A| - 2 (Thm 1, Redei polynomial method). The case |A| ~ sqrt p with a constant C is left open.
- SOURCE: O'Bryant DS11 annotations: Zhang, Math. Comp. 63 (1994) 403-414 computes min over dilates/translates of cut Bose sets to make m - a_m^{1/2} large (K(p_145) > 10.279). Lindstrom, Math. Comp. 67 (1998) 1173-1178: varying the generator equals an affine map.
- SOURCE: Dimitromanolakis thesis (TU Crete 2002, full text read), Ch. 6-7: exhaustive dilate+cut of Bose/Ruzsa up to 65000 marks. Sec. 7.2.2: the conjectured n^2 - n^{3/2} law for optimal length "does not seem to hold". Rokicki-Dogon (cube20.org/golomb): all affine images of Singer/Bose/Ruzsa up to 40000 marks, with no growth law stated.
- SOURCE: erdosproblems.com/30 and its forum (9 visible comments plus 1 proof-claim thread read; 3 comments hidden). Comments cover upper-bound constants (0.98183 -> 0.9435 -> about 0.9428 claims) and exact h(N) for N <= 586 (excess 1.93 -> 3.79). There is nothing on Poisson/dilate reductions.
- Verdict: the general strategy (dilate + translate + cut, and Green's suggestion) is KNOWN. The specific reduction "R_k -> 0 for each k implies unbounded excess via Bonferroni" was NOT FOUND.

## OpenAI October 2026 batch (github openai/math)
- SOURCE: CONTENTS.md (638 KB, full index) grepped for sidon/singer/golomb/difference set/perfect difference/dilate/Erdos. The only hits were the four-manifold "Singer conjecture" (#315, unrelated), the Erdos similarity conjecture (#084) and the reciprocal-sum/AP result (#159). Nothing on Sidon sets, Singer difference sets or Erdos #30. SOURCE (news): Bloom's list of 23 Erdos problems in the batch excludes #30.

## Coverage
- Full text read: 2609.14332 (HTML); 2110.10959 (PDF text); Chmelnitzki essay; Dimitromanolakis thesis; Green open problems (Problems 31-32); O'Bryant DS11 (grep of the full text); Carter-Hunter-O'Bryant 2310.20032 (grep); Chan-Law-Wong 2011; Shakan 2004.14828; Herron 2502.09536 (first 80%); erdosproblems #30 page and forum; openai/math CONTENTS.md.
- Read through a summarizer only: Eberhard-Manners 2107.05744; Forey-Fresan-Kowalski 2301.12878.
- Abstract/bibliographic only: EHKX math/9807029; Arasu-Davis-Jungnickel-Pott 1990; Zhang 1994; Lindstrom 1998; Cilleruelo 1003.3576; Jungnickel-Vedder 1984 (only as cited by Chan-Law-Wong).
- Not accessed: Guy, Unsolved Problems in Number Theory, C9 (book, paywalled); Ho's papers on multipliers; Jungnickel-Vedder original; 3 hidden erdosproblems comments; individual openai/math manuscripts (index only).
- Databases NOT searched: MathSciNet, zbMATH, Google Scholar citation chains, Scopus. Search used a general web engine plus arXiv/GitHub only.
- Residual risk (INFERENCE): R2/R3 could exist in finite-geometry papers on "intersection of a Singer line with its images under power maps" or in the Golomb-ruler engineering literature (statistics of window counts). A zbMATH search for "Singer difference set" AND (dilation OR multiplier) AND (Poisson OR moment) is recommended before publication.

## zbMATH Open check (Claude, 2026-10-19, API api.zbmath.org/v1/document/_search; web UI returned 403)
Queries: "Singer difference sets" (156 hits, first 25 titles read), "dilates Sidon" (2), "Sidon sets Poisson" (8),
"difference set dilation intersection" (1), "Golomb ruler Singer affine" (1: Drakakis 2009 review of Golomb constructions),
"Erdos Sidon sqrt N excess" (0), "Bose Chowla Sidon dilation" (0), "planar difference set three term" (3, unrelated).
Relevant classical items: Pickert 1989 "Difference sets and ovals" (2D oval fact), Baumert 1971 "Cyclic difference sets",
Pott 1995 "Finite geometry and character theory", Evans-Hollmann-Krattenthaler 1999. None states R1 (curve count), R2, R3, R4 or
the Poisson -> C9 reduction. Coverage limit: keyword search on titles/abstracts only; MathSciNet not available.
