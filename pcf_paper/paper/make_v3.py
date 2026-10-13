"""Apply the v3 edits (Batch 20 proofs, C12 rerun, 20B exploratory) to pcf_paper_v3.tex (copied from v2)."""
import shutil
shutil.copy("pcf_paper_v2.tex", "pcf_paper_v3.tex")
f = "pcf_paper_v3.tex"; s = open(f, encoding="utf-8").read()
def R(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, 1)

R(r"hidden low-degree equivalences, a staged identification pipeline,\\ and eight unidentified candidates",
  r"seven hidden low-degree equivalences with proofs,\\ a staged identification pipeline, and eight unidentified candidates")
R(r"\date{DRAFT v2, \today}", r"\date{DRAFT v3, \today}")
R(r"""170 digits); for three of them we give exact proofs by polynomial coboundaries (Theorem~2), revealing a simple hiding mechanism
that standard deflation tests do not detect.""",
r"""170 digits). For ALL seven we give exact proofs by coboundaries (Theorem~2): the candidate is its partner, shifted by up to
three steps, multiplied at each step by a constant times one linear factor of its own $b(n)$, and mixed by a polynomial gauge of
degree at most six. This simple hiding mechanism is not detected by standard deflation tests.""")
R(r"""\begin{center}{\small\begin{tabular}{llllc}\toprule
cand. & partner $a(n)$ & partner $b(n)$ & relation & status\\\midrule
C0 & $2n+3$ & $(3n+5)(5n+1)$ & $y=3-x$ & proven\\
C10 & $n-3$ & $(2n+1)(3n+2)$ & $y=(8-6x)/(4-5x)$ & proven\\
C11 & $n-3$ & $(3n-1)(4n+1)$ & $y=(8-3x)/(4+x)$ & proven\\
C1 & $2n-1$ & $(3n-5)(5n-21)$ & $y=-(5+4x)/5$ & 171 digits\\
C5 & $6n-3$ & $9(3n-2)(5n-2)$ & $y=(x-3)/(-4-x)$ & 171 digits\\
C7 & $2n$ & $4(2n+3)(3n+1)$ & $y=-3x/(5-x)$ & 171 digits\\
C14 & $2n+8$ & $4(4n+1)(5n-7)$ & $y=(4+x)/6$ & 172 digits\\\bottomrule
\end{tabular}}\end{center}""",
r"""\begin{center}{\small\begin{tabular}{llllccc}\toprule
cand. & partner $a(n)$ & partner $b(n)$ & relation & $\lambda(n)$ & $s$ & $\deg V$\\\midrule
C0 & $2n+3$ & $(3n+5)(5n+1)$ & $y=3-x$ & $2n+1$ & $1$ & 3\\
C10 & $n-3$ & $(2n+1)(3n+2)$ & $y=(8-6x)/(4-5x)$ & $3n+4$ & $1$ & 3\\
C11 & $n-3$ & $(3n-1)(4n+1)$ & $y=(8-3x)/(4+x)$ & $3n+1$ & $1$ & 3\\
C1 & $2n-1$ & $(3n-5)(5n-21)$ & $y=-(5+4x)/5$ & $2n+5$ & $-3$ & 3\\
C5 & $6n-3$ & $9(3n-2)(5n-2)$ & $y=(x-3)/(-4-x)$ & $(2n+3)/3$ & $-3$ & 6\\
C7 & $2n$ & $4(2n+3)(3n+1)$ & $y=-3x/(5-x)$ & $(3n+5)/2$ & $-2$ & 6\\
C14 & $2n+8$ & $4(4n+1)(5n-7)$ & $y=(4+x)/6$ & $(3n+4)/2$ & $-2$ & 6\\\bottomrule
\end{tabular}}\end{center}
All seven relations are proven (Theorem~2); $\lambda$, $s$ and $V$ refer to the identity there; all $V$ matrices are in the released data.""")
R(r"""\begin{theorem}
Let $M_1$ be the matrix of candidate C0""", r"""\begin{theorem}
For each of the seven candidates there is a polynomial $2\times2$ matrix $V(n)$ with $\det V\not\equiv0$ such that
$M_1(n)\,V(n)=\lambda(n)\,V(n-1)\,M_2(n-s)$, with $\lambda$, $s$ as in the table; in every case $\lambda$ is a constant ($1$, $1/2$ or
$1/3$) times a linear factor of the candidate's $b(n)$. For example, let $M_1$ be the matrix of candidate C0""")
R(r"""$\det U(n)=-\frac59(2n-1)(2n+1)\neq0$ for integers $n$. Analogous identities hold for C10 ($\lambda=3n+4$) and C11 ($\lambda=3n+1$).
\end{theorem}""", r"""$\det U(n)=-\frac59(2n-1)(2n+1)\neq0$ for integers $n$; for C1, $s=-3$, $\lambda=2n+5$ and
\[V(n)=\begin{pmatrix}\frac65n^2+\frac{21}5n+\frac{18}5 & 6n^3+\frac{109}5n^2+\frac{82}5n-\frac{21}5\\[2pt] \frac15 & n+\frac85\end{pmatrix},\qquad
\det V(n)=\tfrac{11}{25}(2n+3)(2n+5).\]
\end{theorem}""")
R(r"""The identities are polynomial and were verified symbolically; they make the convergent matrices equivalent and imply the M\"obius
relations of the table. Mechanism: the candidate is its degree-$(1,2)$ partner shifted by one step and wrapped by one linear factor
$\lambda(n)$ of its own $b(n)$, mixed by a cubic polynomial gauge $U(n)$; the partner's $b$ is then a product of two linear factors
of the candidate's $b$, which turns the search into a cheap filter. C1, C5, C7 and C14 are not obtained this way within the searched
gauge degrees (up to 5), nor by a two-step (contraction) ansatz whose positive control failed, so their mechanism is open.""",
r"""\begin{proof}[Proof and use]
Each identity is an equality of polynomial matrices and was verified by expanding it symbolically, by two independent scripts.
Multiplying it for $n=1,\dots,N$ gives $A_1M_1(1)\cdots M_1(N)=\Lambda_N\,G\,A_2M_2(1)\cdots M_2(N-s)\,V(N)^{-1}$ with a scalar
$\Lambda_N$ and a constant matrix $G$ built from $V(0)$, $A_i=\left(\begin{smallmatrix}1&a_i(0)\\0&1\end{smallmatrix}\right)$ and at
most three partner matrices; hence $x=(g_{11}y+g_{12})/(g_{21}y+g_{22})$. The exact $G$ obtained this way reproduces every relation
of the table (numerical agreement better than $10^{-87}$).
\end{proof}
Mechanism: the candidate is its degree-$(1,2)$ partner shifted by $s$ steps and wrapped by $\lambda(n)$, mixed by a polynomial
gauge; the partner's $b$ is (a scalar times) a product of two linear factors of the candidate's $b$, which turns the search into a
cheap filter. The proofs were found by solving the identity as a linear system over $\mathbb Q$ for $V$, for $\lambda=\kappa\,p(n)/q(n)$
with $p,q$ built from linear factors of $b_1$, $b_2$ and their unit shifts; a determinant condition ($\det V(n)/\det V(n-1)$ must
telescope) prunes the search exactly. Controls: C0 re-proven, a planted rational $\lambda$ recovered, no proof for C2 against a
random partner. Earlier searches had missed C1, C5, C7, C14 because they used shifts $s\ge-2$ and integer $\kappa$ only.

\paragraph{How common is the mechanism? (exploratory)} In a random sample of 1{,}065 full-FR PCFs of the extended search, the
mechanism filter found a verified (60 digits) M\"obius partner of degree $(1,2)$ for $168/291$ of the Conjecture~1.3 family,
$195/300$ of the deflatable PCFs and $40/300$ of the remaining ones (``survivors'').
The pre-registered mismatch control (partners built from the factors of a DIFFERENT PCF) gave $12/150$ verified matches, above
the 2\% limit we had set; the matches are genuine, which shows that the partners are generic rather than specific. These
fractions are therefore lower bounds for M\"obius equivalence to some degree-$(1,2)$ PCF, not a measure of the specific mechanism.""")
R(r"""Novelty is not established: unpublished databases (e.g.\ the Ramanujan Library) were not available to us. C12 was not completed
by the widest mechanism filter. The identifications of C1, C5, C7, C14 are numerical (170 digits). Irreducibility is over""",
r"""Novelty is not established: unpublished databases (e.g.\ the Ramanujan Library) were not available to us. For C12 the widest
mechanism filter rejected 76 of 77 float matches; one partner ($a=14n-7$, $b=-54n^2+261n-81$, complex characteristic roots) did
not converge numerically and is unresolved. The negative results for the eight are limited to the searched boxes. Irreducibility is over""")
R(r"""(stages: basic constants, known structures, mechanism filter, low-degree
search, constant libraries, operator analysis, coboundary proof; self-test included) are released with this preprint.""",
r"""(stages: basic constants, known structures, mechanism filter, low-degree
search, constant libraries, operator analysis, coboundary proof; self-test included) are released with this preprint, together
with the rational-$\lambda$ prover \texttt{b20\_rational.py}, the seven proofs ($V$ matrices) and the independent check scripts.""")
open(f, "w", encoding="utf-8").write(s); print("v3 written")
