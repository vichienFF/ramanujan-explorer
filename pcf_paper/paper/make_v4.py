"""Apply the v4 edits (Batch 21: C2 identified and proven; mechanism-guided filter; C12 band test) to pcf_paper_v4.tex.
Run make_v3.py first (v3 is generated from v2)."""
import shutil
shutil.copy("pcf_paper_v3.tex", "pcf_paper_v4.tex")
f = "pcf_paper_v4.tex"; s = open(f, encoding="utf-8").read()
def R(old, new, count=1):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, count)

R(r"seven hidden low-degree equivalences with proofs,\\ a staged identification pipeline, and eight unidentified candidates",
  r"eight hidden low-degree equivalences with proofs,\\ a staged identification pipeline, and seven unidentified candidates")
R(r"\date{DRAFT v3, \today}", r"\date{DRAFT v4, \today}")
R(r"""seven of the fifteen are disguised degree-$(1,2)$ PCFs, i.e.\ ratios of contiguous Gauss hypergeometric functions (agreement to
170 digits). For ALL seven we give""", r"""eight of the fifteen are disguised degree-$(1,2)$ PCFs, i.e.\ ratios of contiguous Gauss hypergeometric functions (agreement to
170 digits). For ALL eight we give""")
R("shifted by up to\nthree steps", "shifted by up to\nfour steps")
R(r"The remaining eight passed every test we could devise", r"The remaining seven passed every test we could devise")
R(r"pipeline that would have identified the seven on the first day.", r"""pipeline that would have identified the eight on the first day. One of the eight (C2) had passed all our
novelty tests before it was identified, which shows how weak such tests are as evidence of novelty.""")
R(r"\section{Seven of the fifteen are disguised", r"\section{Eight of the fifteen are disguised")
R(r"""C14 & $2n+8$ & $4(4n+1)(5n-7)$ & $y=(4+x)/6$ & $(3n+4)/2$ & $-2$ & 6\\\bottomrule""",
  r"""C14 & $2n+8$ & $4(4n+1)(5n-7)$ & $y=(4+x)/6$ & $(3n+4)/2$ & $-2$ & 6\\
C2 & $2n-8$ & $8(2n+1)(3n-2)$ & $y=-5x/(x+12)$ & $(3n+8)/2$ & $-4$ & 6\\\bottomrule""")
R(r"All seven relations are proven (Theorem~2)", r"All eight relations are proven (Theorem~2)")
R(r"hence none of the seven is a new constant.", r"""hence none of the eight is a new constant. C2 was found
only by the mechanism-guided filter of Batch~21 (below); it needs a M\"obius coefficient 12 and a shift of four steps.""")
R(r"For each of the seven candidates there is", r"For each of the eight candidates there is")
R(r"""random partner. Earlier searches had missed C1, C5, C7, C14 because they used shifts $s\ge-2$ and integer $\kappa$ only.""",
  r"""random partner. Earlier searches had missed C1, C5, C7, C14 because they used shifts $s\ge-2$ and integer $\kappa$ only.

\paragraph{Mechanism-guided filter.} In all proven cases the leading coefficients satisfy
$\alpha^2/\mathrm{lead}(b_2)=A^2/B$ ($A,B$ the leading coefficients of the candidate's $a,b$; $\alpha$ that of the partner's $a$),
i.e.\ the characteristic roots have the same ratio. Fixing $\alpha$ this way removes one search dimension, which we spent on
independent shifts $s_1,s_2\in[-6,6]$ of the two factors, fractional normalisations and M\"obius coefficients up to 12. All five
positive controls (C0, C1, C5, C7, C14) were re-found, two random reals gave no match, and C2 was identified (331 digits with an
independent evaluator) and then proven. C3, C4, C6, C8, C9, C12 and C13 gave no match and no unresolved partner.""")
R(r"\section{The eight unidentified candidates}", r"\section{The seven unidentified candidates}")
R(r"""C2 & $3n^2+8n+8$ & $2(2n+3)(3n+1)(3n+2)(3n+8)$ & $33.5147685956496535\ldots$ & $-187/42$\\
""", "")
R(r"\paragraph{Tests passed by all eight (none identified).}", r"\paragraph{Tests passed by all seven (none identified).}")
R(r"no low-degree M\"obius partner in the searches of Section~4;", r"no low-degree M\"obius partner in the searches of Section~4, including the mechanism-guided filter;")
R(r"""not converge numerically and is unresolved. The negative results for the eight are limited to the searched boxes.""",
  r"""does not converge: its convergents between depths $10^4$ and $10^6$ oscillate in a band of width $3\times10^{-9}$ that does not
shrink and does not contain the predicted value (which lies $6\times10^{-9}$ outside); by our pre-registered rule this case is
formally unresolved. The negative results for the seven are limited to the searched boxes; the mechanism-guided filter covers
only partners related by the proven mechanism.""")
R(r"the seven proofs ($V$ matrices)", r"the eight proofs ($V$ matrices), the mechanism-guided filter \texttt{b21b\_mechanism.py}")
R("at\nmost three partner matrices", "at\nmost four partner matrices")
open(f, "w", encoding="utf-8").write(s); print("v4 written")
