# Independent referee report: paper_c9/c9_note_v2.tex (Version 2, 19 Oct 2026)

Reviewer: independent adversarial AI referee (Claude), 2026-10-19. I did not modify the .tex file or any data file.
Re-run: b28_analyze.py and b29_analyze.py, both reproduce b28_result.json and b29_result.json exactly. I recomputed V3 statistics from kaggle_v3, kaggle_lerr, kaggle_lbulk and kaggle_lall, the prime-power table from kaggle_ppa and kaggle_ppb, the orbit enumeration from irred_cert.py, and the forbidden-ratio constant exactly for q = 41, 293, 383, 1373.

## Verdict: PUBLISHABLE WITH FIXES

The mathematics that is labelled "proved" holds up. That covers the reduction (Bonferroni direction, F_k -> C^k, Sidon mod m => Sidon in Z, the arithmetic), Proposition 1 (variance and R_3 formula, rederived by hand), the identity sum N^2 = sum (I)_3, the Bezout argument, the conditional Cauchy-Schwarz proposition (including the sqrt(log q)/q weight norm, which I rederived heuristically) and the logic of the curve theorem.

Three statements are false as written and must be fixed before release:
- Theorem 1(d): the 18 orbits include the forbidden orbit, which does not satisfy the hypothesis of (c).
- The abstract's "within 0.3%" is not supported by the data.
- The table's `\\midrule` prints the word "midrule" and drops the rule.

The other issues are rounding, wording and bibliography.

## Issues

### 1. [MAJOR] Theorem 1(d) and the abstract count the forbidden orbit as "certified absolutely irreducible"
irred_cert.py with H = 8 enumerates 22 exponent orbits, and that count includes (-2,1,1), i.e. {-1, 2, 1/2}. 22 - 4 timed-out orbits = 18. Of these, only 17 have a certificate: 5 orbits of height <= 4 (-2, -3, -3/2, -4, -4/3) plus the 12 listed. For {-1, 2, 1/2}, part (b) says C_{u,v} is the diagonal, so "C_{u,v} minus the diagonal" is empty and not absolutely irreducible. The statement "holds for every ratio of height <= 4" is therefore false for rho = -1, 2, 1/2.

Fix, line 117-118. Replace
`(d) The hypothesis of (c) holds for every ratio of height $\le4$ and for the orbits ... $-8,-8/3,-8/5,-8/7$: 18 orbits in all.`
with
`(d) The hypothesis of (c) holds for every ratio of height $\le4$ other than $-1,2,1/2$ (five orbits) and for the orbits ... $-8,-8/3,-8/5,-8/7$: 17 orbits in all. Together with (b), every ratio of height $\le4$, and every orbit with representative $-a/b$, $a\le8$, except the four listed below, is covered (18 of 22 orbits).`

Abstract, lines 19-20. Replace
`which we certify by exact computation for 18 ratio orbits, including all ratios of height $\le4$`
with
`which we certify by exact computation for 17 ratio orbits, including all non-forbidden ratios of height $\le4$`

Release item: the folder holds no stored certificate output for the height <= 4 orbits. cert_H6.txt contains only -5, -5/2, -6, -6/5. kaggle_cert has the height 5-8 orbits. The H <= 4 run appears only in the earlier review's scratch re-run. Re-run `irred_cert.py 4`, save the output (for example as cert_H4.txt) and add it to the SHA ledger before claiming "certificates are released".

### 2. [MAJOR] The abstract and the absolute-irreducibility hypothesis are worded inconsistently
The diagonal is always a component of C_{u,v} (a double component, per the step B review). So "C_{u,v} is absolutely irreducible" (abstract, line 19) is never true.

Fix, line 19. Replace `whenever $C_{u,v}$ is absolutely irreducible` with `whenever $C_{u,v}$ minus its diagonal is absolutely irreducible`.

### 3. [MAJOR] V3 numbers: "3.000 +- 0.007" and "to within 0.3%" do not match the data
I recomputed over the 37 primes 293 <= q <= 2969 (m prime) from kaggle_v3 and kaggle_lerr:
- mean 2.998
- standard deviation 0.0083, standard error of the mean 0.0014
- range 2.979 (q = 701) to 3.019 (q = 383)
- largest per-q deviation 0.72%

"Within 0.3% for prime q <= 2969" is false per q. It also suggests every prime q <= 2969 was tested, when only 37 primes with m prime were.

Fix, abstract lines 24. Replace
`to within $0.3\%$ for prime $q\le2969$`
with
`to within $0.8\%$ for each of 37 primes $293\le q\le2969$ with $m$ prime (mean $2.998$)`

Fix, line 166. Replace
`the ratio is $3.000\pm0.007$ over 37 primes $293\le q\le2969$`
with
`the ratio has mean $2.998$ (s.d.\ $0.008$, range $[2.979,3.019]$) over 37 primes $293\le q\le2969$`

### 4. [MAJOR, LaTeX] The table header rule is broken
Line 171: `...&ratio$/3k$\\midrule`. Here `\\` ends the row and `midrule` is typeset as text in the first cell of the row for q = 121. No rule is drawn. The file still compiles, so this is easy to miss.

Fix: `...&ratio$/3k$\\ \midrule`.

### 5. [MINOR] Blind-test ratios are rounded incorrectly in two places
- B28, k = 3: the measured value is 1.0246, which rounds to **1.02**, not 1.03.
- B29, C = 2, k = 3: the measured value is 0.9748, which rounds to **0.97**, not 0.98.

All other values match: 1.06, 1.06, 1.05 / 0.97, 0.97, 0.97, 1.01 / 0.95, 0.98, 1.00, 1.00, 1.00, 1.01.

Fix, line 155. Replace `$k=3,\dots,6$ gave $1.03,1.06,1.06,1.05$` with `$k=3,\dots,6$ gave $1.02,1.06,1.06,1.05$`.
Fix, line 156. Replace `$C=2$ gave $0.98,0.97,0.97,0.97,1.01$` with `$C=2$ gave $0.97,0.97,0.97,0.97,1.01$`.

### 6. [MINOR] The null-control sentence contradicts the voided cell
For C = 2, k = 8 the random sets are at 3.4 standard errors (-68.1 +- 19.8). That is why the cell was voided.

Fix, lines 158-159. Replace `Random sets were within $3$ standard errors of $0$.` with `Random sets were within $3$ standard errors of $0$ in every other cell.`

### 7. [MINOR] Blindness for k = 3 in B28
PLAN_BATCH28 says "BLIND for k >= 4". Exact R_3 had already been computed at overlapping primes (B27: 293-1373; Lane B1: 1559-2969).

Fix, line 154. After `Two registered blind tests` insert `(blind for $k\ge4$ in the first, for all $k$ in the second)`.
Abstract line 23. Replace `for $k\le8$ on 129 new primes` with `for $k\le8$ (up to $k=7$ at $C=2$, $k=8$ at $C=4$) on 129 primes not previously used for $k\ge4$`.

### 8. [MINOR] The prime-power variance law is under-specified
- In pp_template.py, E is the empirical mean of N over good rho, not (n)_3/(m-2). The paper never defines E for composite m.
- The small q excluded by the frozen q >= 121 rule disagree strongly with the law. In kaggle_ppa, ratio/3k is 0.196 at q = 9, 0.68 at q = 16, 0.69 at q = 49 and 0.83 at q = 81. The plan's own smoke list omits q = 9 and q = 81.
- PLAN_PPV3 also freezes shards c (1681-2197) and d (2209-3125). Their results are not in the folder or the paper.

Fix, Conjecture line 164. Append `, and $E$ is the mean of $N(\rho)$ over these $\rho$ (equal to $(n)_3/(m-2)$ when $m$ is prime)`.
Fix, Table caption. Append `For $q<121$ (outside the registered range) the ratio$/3k$ is far from $1$ (e.g.\ $0.20$ at $q=9$, $0.69$ at $q=49$, $0.83$ at $q=81$).`
Then either report shards c and d or state `shards with $q>1369$ were registered and are pending`.

### 9. [MINOR] The genus claim is stated as fact but is only numerical extrapolation
Line 133: `The genus of $C_{u,v}$ grows at least quadratically in the height`. The evidence is numerical Riemann-Hurwitz/monodromy genus values for 8 curves. The (-n,1,n-1) family has only n = 3..6 (values 0, 0, 1, 3).

Replace with `Numerically, the genus of $C_{u,v}$ appears to grow at least quadratically in the height`.

### 10. [MINOR] The Bezout statement needs a non-degeneracy caveat
Line 144: `so $I_\lambda\le d$ by B\'ezout`. This fails if L is a component of the image curve. For example, when q is even, lambda = 2 is a multiplier (d = 2, I = n).

Replace with `so $I_\lambda\le d$ by B\'ezout unless $L$ lies on that curve (this does not happen for $d=2$ and odd $q$)`.

### 11. [MINOR] The exact identity needs m prime
lambda = (b'-a')/(b-a) is a unit and every distinct triple has a ratio only if m is prime.

Line 138: after `Let $I_\lambda(\mu)=|S\cap(\lambda S+\mu)|$` insert `and let $m$ be prime`. (q = 5, 17, 41, 59 all give prime m: 31, 307, 1723, 3541.)

### 12. [MINOR] Null lambda list: the data support more q than stated
The all-lambda runs give exactly the 9 elements at q = 167, 173, 293 (kaggle_lall) and 383 (kaggle_lbulk). Line 146: replace `for $q=41,59,383$` with `for $q=41,59,167,173,293,383$`.

### 13. [MINOR] N(rho) = 0 mod 3 is a lemma, not evidence
For m prime, x -> qx + c has gcd(q-1, m) = 1 fixed point. So the multiplier acts freely on distinct triples and orbits have size 3.

Line 166: replace `Evidence: $N(\rho)\equiv0\pmod3$ in every case computed.` with `For $m$ prime, the multiplier $q$ acts freely on distinct triples, so $N(\rho)\equiv0\pmod3$ (observed also for all prime powers computed).`

### 14. [MINOR] Dangling Version 1 sentence
Line 49: `The largest $q$ gives the example in the abstract;` refers to an example that is no longer in the abstract. Replace with `The largest $q$ gives excess ...` (state the number) or delete the clause.

### 15. [MINOR] Bootstrap interval
RESULTS_DIGEST gives 95% CI 0.962-1.000. The paper (line 54) says `[0.963,1.000]`. Use the digest value or re-check the source log.

### 16. [MINOR] Reduction hypothesis wording in the abstract and Section 9
The reduction needs R_k -> 0 for every fixed k **and every C**.
- Abstract (i): replace `for every fixed order` with `for every fixed order and every window constant $C$`.
- Line 202: replace `follows from $R_k\to0$ for each fixed $k$` with `follows from $R_k\to0$ for each fixed $k$ and each $C$`.
- Abstract line 21-22: "the deviation ... equals" should read "is, to first order,".

### 17. [MINOR] Bibliography (checked on the web where possible)
- **Pickert.** Replace `G.~Pickert, Difference sets and ovals (1989); see zbMATH Open.` with `G.~Pickert, Differenzmengen und Ovale, Discrete Math. 73 (1989) 165--179 (zbMATH 0667.51002).`
- **Shakan.** arXiv:2004.14828 is correct (verified). The paper was published: append `; SIAM J. Discrete Math., doi:10.1137/20M1335030`. I did not confirm volume and pages.
- **Aubry-Perret.** Verified. Add the editors: `in: R.~Pellikaan, M.~Perret, S.~G.~Vl\u{a}du\c{t} (eds.), Arithmetic, Geometry and Coding Theory (Luminy 1993), de Gruyter, Berlin 1996, 1--7.`
- **Jungnickel-Vedder.** EJC 5 (1984) 143-148 is verified as cited by others. I did not see the original.
- **Gowers.** Title and date (13 July 2012) are verified. The dilate idea is in **Ben Green's** comment (20 July 2012). Line 38: say `in B.~Green's comment on \cite{Go}`.
- **Green's open problems.** These are cited in the text but have no bibitem. Add `\bibitem{Gr} B.~Green, 100 open problems, Problems 31--32 (manuscript, updated 2026).` and cite it at line 38.
- **Martin-O'Bryant.** Verified via ar5iv, Section 3.2: the $500 prize and "answered negatively if Bose(p,theta,1) has a gap not O(p)" are both there. Correct.
- **erdosproblems.com/30.** The $1000 prize for the N^eps form is verified. The O(1) form is a remark. Consistent with the paper.
- **RD (Rokicki-Dogon).** Defined but never cited. Cite it (for example at line 39, as prior dilate computations) or remove it.
- **BFR, BHP, Bose, ET, Singer, Zhang, Guy.** Consistent with standard citations. My search for BFR was cut off by a session limit, so these are not re-verified online.

### 18. [MINOR] Release preparation
- The URL `https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v2` does not exist yet. Create it before release and include the files below, then check that the link resolves:
  - certificates (H <= 4: issue 1; cert_H6.txt; kaggle_cert and kaggle_cert2 outputs)
  - irred_cert.py
  - b28 and b29 plans, scripts and outputs
  - PLAN_PPV3.md
  - the lane_b LEDGER with SHA-256 values
  - all kaggle_* jsonl files
- Section cross-references are hard-coded ("Section 4", "Section 6", "Section 10", "Section 3", "Section 1"). They are currently correct (1 Background, 2 Dilate gaps, 3 Moment route, 4 Reduction, 5 Curves, 6 Identities, 7 Higher moments, 8 Variance, 9 What remains, 10 Limitations). Using `\ref` would keep them correct after edits.

## Checked and found correct
- **Reduction proof.**
  - Odd-index truncation is a lower bound, since sum_{k<=j}(-1)^k C(Z,k) = (-1)^j C(Z-1,j).
  - H_k -> C^k.
  - The choice of a fixed K.
  - Cutting gives a Sidon set in an interval of m - l integers.
  - N = q^2 + (1-C)q + O(1) and q + 1 - sqrt N = (C+1)/2 + O(1/q).
- **Proposition 1.**
  - Var = q l(m-l)/m^2, using n^2 = m + q.
  - R_2 = 0.
  - The R_3 formula, sum A = l(l-1)(l-2)/(m-1), and sum N = (n)_3 = E(m-2).
  - The forbidden-ratio contribution -3/(2Cq). My exact ratios to the asymptotic value at C = 2: 1.0123 at q = 41, 1.0017 at q = 293, 1.0013 at q = 383. This matches "1.2%" and "0.2%".
- **P_3 ~ 3/(2l) and P_4 ~ 2/l**, and therefore c_k ~ k^4.
- **Identity and second moment.** The affine-map bijection, sum_mu (I)_2 = m - 1, and the multiplier term 3(n)_3.
- **Bezout and lambda = -1.** -1 = q^2 + q has digit sum 2. 1/2 follows by inversion.
- **Conditional proposition.**
  - The uniform part cancels.
  - Cauchy-Schwarz is applied correctly.
  - ||w - wbar||_2 ~ sqrt(log q)/q is plausible: low-height rho has w ~ 1/(qH), and the sum over H gives log q / q^2.
  - The threshold o(q^4/log q) in Section 9 is consistent.
- **Theorem 1(d) certificate logic.** Galois orbit, smooth K-point, k | [K:Q]. This is valid because G is a Q-irreducible factor. Saying so in the sketch would help.
- **Genus formula.** (n-3)(n-4)/2 matches the numerical genera for n = 3..6 (0, 0, 1, 3).
- **Variance, kurtosis and the null-lambda class.** At q = 383: bulk sd 4.208q and kurtosis 3.009, with the 9 null lambda excluded. The 9-element class is exactly {-1, 2, 1/2} x {1, q, q^2} at q = 167, 173, 293, 383.
- **Prime-power table.** All 18 rows (good-rho counts, ratios, ratio/3k) match the jsonl files. 16 of 18 are within 10%.
- **Section 3 numbers.**
  - RMSE 0.0028 / 0.0238 / 0.0013 / 0.0112.
  - C q R_3 bands -1.45..-1.41 and -1.47..-1.46.
  - D_mid slopes -0.13 +- 0.17 and -0.504 +- 0.098.
- **Section 2 numbers.** 10.2797, RMSE 1.22 / 4.25 and 1.52 / 7.34, -0.57, 0.983. All match RESULTS_DIGEST.
- **Primes in [607, 1499].** There are 129: 65 + 64.

## Could not check
- I could not compile the LaTeX. A careful read found no unbalanced braces or undefined refs; the only defect is issue 4.
- I did not re-run the exact-arithmetic irreducibility certificates (hours of SymPy). I checked only the stored outputs and the certificate logic.
- I did not independently verify Theorem 1(a) (the twist). I rely on the 2026-10-16 review's exact counts for q = 5, 7, 11, 13.
- I did not check the numerical monodromy genus computations.
- Not confirmed from source data:
  - the sealed-set slope -1.28 +- 0.39
  - sqrt(q) D_mid range 0.49-1.84
  - sqrt(q) D_all ~ 1.73 vs 1.0
  - the q = 41, 59 null-lambda counts (kaggle_v4 does not record them)
  - the SHA-256 ledger hashes
- Not accessed: the Guy C9 text, the Jungnickel-Vedder original, MathSciNet, and the full Shakan SIAM citation. My BFR check was cut off.
- No human expert has checked the "proved" statements. The paper discloses this correctly.
