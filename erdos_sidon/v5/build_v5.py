"""Build c9_note_v5.tex from c9_note_v4.tex (Version 5 = corrective version after the two AI referee reports of 2026-11-01:
D:/Claude_Brain/reviews/REVIEW_C9_V4_MATH_2026-11-01.md and REVIEW_C9_V4_REPRO_2026-11-01.md). Every edit is asserted (old text occurs once)."""
import os, re  # NO-CONTROL: text build, not a computation; each edit is asserted to match exactly once
D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, 'c9_note_v4.tex'), encoding='utf-8').read()
a0 = s.index(r'\begin{abstract}'); a1 = s.index(r'\end{abstract}')
ABSTRACT = r"""\begin{abstract}
Let $h(N)$ be the maximal size of a Sidon set in $\{1,\dots,N\}$. Erd\H{o}s asked whether $h(N)=N^{1/2}+O(1)$ (Guy C9); the weaker
$h(N)=N^{1/2}+O_\varepsilon(N^\varepsilon)$ is Erd\H{o}s problem \#30. Both questions remain open, and we do not settle them. We study dilates of Singer perfect difference sets $S$
($|S|=q+1$, modulus $m=q^2+q+1$) and the number $Z$ of points of a random dilate in a window of length $Cq$.
\emph{Proved:} (i) if the factorial moments of $Z$ converge to the Poisson ones for every fixed order and every $C$, then $h(N)-N^{1/2}$ is unbounded
(Proposition~\ref{prop:red}; experts regard this reduction as folklore, and we give a written proof); (ii) for a ratio $\rho$, the number $N(\rho)$ of triples of $S$ with $c-a=\rho(b-a)$
is the number of $\mathbb F_q$-points of a twisted form of a curve that does not depend on $q$, so $N(\rho)/E-1=O_\rho(q^{-1/2})$ for 17 ratio orbits certified by exact computation (Theorem~\ref{thm:curve});
(iii) for prime $m$, $\sum_\rho N(\rho)^2=\sum_{\lambda,\mu}(|S\cap(\lambda S+\mu)|)_3$; (iv) $3k\mid N(\rho)$ for $q=p^k$, and a resonance theorem for cube $q=r^3$: $N(\rho)=r(q+1-e)$,
$e\in\{0,1\}$, for the six ratios of the $S_3$-orbit of $r+r^{-1}$ ($m$ prime); (v) for prime $q\ge5$ and every unit $\lambda$, the per-dilation third moment
$\sum_\mu(|S\cap(\lambda S+\mu)|)_3$ equals $P(\lambda)-(q-2)^2$, where $P(\lambda)$ counts solutions of $c\,y^\lambda+d(1-y)^\lambda=1$ ($y\in\mathbb F_{q^3}$, $c,d\in\mathbb F_q^\times$);
it is $0$ at $\lambda=2,-1$ (the classical conic fact), $(q-2)(q+1)$ at $\lambda=3$ ($q\equiv2\pmod3$), and $(q-2)(q+1)+b_q$ at $\lambda=-2$, where $b_q$ is the $q$-th
coefficient of the CM newform $\eta(2\tau)^3\eta(6\tau)^3$ (Theorem~\ref{thm:gal}; one step uses an evaluation of a finite-field hypergeometric value due to Ono, in the form of Barman and Kalita).
\emph{Observed} (registrations are self-attested, see Section~\ref{sec:lim}): to first order the $k$-th factorial moment of $Z$ falls short of the random value by
$\binom k3P_3+\binom k4P_4$, where $P_3,P_4$ are the window probabilities of 3-term progressions and parallelograms ($k=3,\dots,6$ at $C=2$ on 129 primes; $k=7$ at $C=2$
and $k=3,\dots,8$ at $C=4$ on 64 of them); and $\sum_\rho(N(\rho)-E)^2$ is close to the order of the multiplier group times $\sum_\rho E$ for prime $q$ and non-cube prime powers,
while most of the excess at cube $q$ is explained by (iv).
\emph{What remains:} a negative answer would follow from Poisson convergence of all fixed-order factorial moments. For order $3$ this reduces to a variance bound, which by (iii) and (v)
is a statement about the average of $P(\lambda)$ over all $\lambda$; for order $\ge4$ we have no such reduction.
"""
s = s[:a0] + ABSTRACT + s[a1:]
R = [
 (r'\date{Version 4, 31 October 2026 (Version 3',
  r'\date{Version 5, November 2026 (corrective version; Version 4: 30 October 2026; Version 3'),
 (r'\begin{document}', r'\begin{document}' '\n' r'\emergencystretch=3em'),
 # Table 1 caption: borderline q = 125 (math m8)
 (r'here 21 of 23; the two misses', r'here 21 of 23, with $q=125$ ($1.1013$) a borderline miss under the rule $|\mathrm{ratio}/3k-1|\le0.10$; the two misses'),
 # global caveat on registrations (repro M3)
 (r'proved that every $A\subset\mathbb F_p$ with $|A|>1$ has a dilate with a gap of at least $2p/|A|-2$.',
  r'proved that every $A\subset\mathbb F_p$ with $|A|>1$ has a dilate with a gap of at least $2p/|A|-2$.'
  '\n' r"Throughout, ``registered'' and ``blind'' mean that"
  r' a plan file and its SHA-256 hash were recorded locally before the computation;'
  r' these records are self-attested (there is no third-party timestamp), and later amendments to a plan are listed in the release.'),
 # novelty of the reduction (repro M5)
 (r'''The cutting step is classical (Section~1); what we add is the reduction of unbounded excess to the convergence of fixed-order factorial
moments of window counts. We did not find it in the literature (Section~\ref{sec:lim}).''',
  r'''The cutting step is classical (Section~1). The reduction of unbounded excess to the convergence of fixed-order factorial moments of
window counts is regarded as folklore by experts (private communication); we did not find a written proof and include one here.'''),
 # Section 6 pointer to the lemma (math M1)
 (r'''which we also checked exactly for $q=5,17,41,59$.''',
  r'''which we also checked exactly for $q=5,17,41,59$. For prime $q$ each inner sum $\sum_\mu(I_\lambda(\mu))_3$ is an explicit point count over
$\mathbb F_{q^3}$ (Lemma~\ref{lem:I3} in Section~\ref{sec:gal}).'''),
 # blind-test plans self-attested (repro M3)
 (r'used plans frozen with a recorded SHA-256 before computing,',
  r'used plans frozen with a recorded SHA-256 before computing (self-attested; two amendments made before any computation are listed in the release),'),
 # Table 1 caption: q=16807 (repro minor 9)
 (r'($2209,2401,2809,3125,3481,3721,4489,6561,8192,14641,16384$) give ratio$/3k\in[0.9980,1.0026]$',
  r'($2209,2401,2809,3125,3481,3721,4489,6561,8192,14641,16384,16807$) give ratio$/3k\in[0.9980,1.0026]$'),
 # Section 11 percent (repro minor 8)
 (r'In the other rows of Table~\ref{tab:res} it gives $55$--$100\%$ (lowest at $q=512$).',
  r'In the other rows of Table~\ref{tab:res} it gives $54$--$100\%$ (lowest at $q=512$).'),
 # Table 2 caption: composite m (math m9) + code (repro C1)
 (r'''Non-cube controls ($q=8192,14641,16384$) give ratio$/3k\in[0.9997,1.0024]$.}''',
  r'''Non-cube controls ($q=8192,14641,16384$) give ratio$/3k\in[0.9997,1.0024]$. For composite $m$, $M$ uses the count restricted to unit differences
(for example $N(\rho_1)=576$ at $q=125$, against $r(q+1-e)=630$ for all triples in Theorem~\ref{thm:res}), so $M/\mu\approx r$ is approximate partly for this reason.
Rows $q=4096,4913,6859$ were computed on Kaggle with \texttt{run\_nb\_top12.py} (all triples) and rows $q\ge12167$ with the orbit-reduced program \texttt{run\_orb.py};
both are released with Version~5, with a regression test of \texttt{run\_orb.py} against an independent brute-force count and a per-row provenance table.}'''),
 # Section 12 hypotheses (math m5) and the "missing input" sentence (math M1)
 (r'Let $K=\mathbb F_{q^3}$ ($q$ an odd prime), $m=q^2+q+1$,',
  r'Let $K=\mathbb F_{q^3}$ ($q$ an odd prime; Theorem~\ref{thm:gal} needs $q\ge5$), $m=q^2+q+1$,'),
 (r'''i.e.\ the correlation of the Jacobi sums with their conjugates under $\zeta_m\mapsto\zeta_m^{\,l}$. Correlations of this kind are the
missing input of Section~\ref{sec:rem}. We also use the elementary count''',
  r'''i.e.\ the correlation of the Jacobi sums with their conjugates under $\zeta_m\mapsto\zeta_m^{\,l}$. By Lemma~\ref{lem:I3} below, these correlations are
the per-dilation third moments of Section~6 in another form. We also use the elementary count'''),
 # Prop gal proof wording (math m2)
 (r'''=m^2P(l^{-1})$, and swapping $y,y'$ gives
$P(l^{-1})=P(l)$.''',
  r'''=m^2P(l^{-1})$, by the pair description of $P$; counting the same set of pairs with the other coordinate as the free variable gives $m^2P(l)$, hence
$P(l^{-1})=P(l)$. (The power $y^l$ depends on the integer representative of $l$ only up to a factor in $\mathbb F_q^\times$, which is absorbed into $(c,d)$.)'''),
 # the lemma (math M1)
 (r'''For $y\in\mathbb F_q\setminus\{0,1\}$ there are exactly $q-2$ admissible pairs $(c,d)$, so $P(l)\ge(q-2)^2$ always.''',
  r'''\begin{lemma}\label{lem:I3}
For every unit $l$ modulo $m$, $P(l)-(q-2)^2=\sum_{\mu}\bigl(I_l(\mu)\bigr)_3$, where $I_l(\mu)=|S\cap(lS+\mu)|$ as in Section~6.
\end{lemma}
\begin{proof}
Identify $\mathbb Z/m$ with the points of $\mathrm{PG}(2,q)=K^\times/\mathbb F_q^\times$ by the discrete logarithm; $S$ is a line, translation by $\mu$ is multiplication by $g^\mu$, and
dilation by $l$ is $x\mapsto x^l$. Because $l$ is a unit modulo $m$, this map is a bijection of the points, so it maps distinct points to distinct points (this is the only use of the
unit condition, and it is essential: for non-units the identity fails). Since the Singer group acts regularly on lines, $\sum_\mu(I_l(\mu))_3$ is the number $T_S$ of ordered
triples of distinct points of $S$ whose $l$-th powers are collinear. Multiplication by $g^\nu$ maps lines to lines and $(g^\nu x)^l=g^{l\nu}x^l$, so $T_{S'}=T_S$ for every line $S'$.
Counting the triples of distinct collinear points with collinear $l$-th powers in two ways (by their line, or by their first point, which multiplication moves to $1$ freely) gives
$m\,T_S=m\,T_1$, where $T_1$ is the number of ordered pairs $(x_2,x_3)$ of points such that $1,x_2,x_3$ are distinct and collinear and $1,x_2^l,x_3^l$ are collinear.
The map $y\mapsto([y],[1-y])$ is a bijection from $K\setminus\mathbb F_q$ onto the pairs $(x_2,x_3)$ with $1,x_2,x_3$ distinct and collinear: given such a pair, $1=a y_0+b z_0$ for
representatives $y_0,z_0$ and unique $a,b\in\mathbb F_q^\times$, and $y=a y_0$ is the unique representative of $x_2$ with $1-y$ representing $x_3$. Collinearity of the three distinct points
$1,y^l,(1-y)^l$ means that $c\,y^l+d(1-y)^l=1$ for exactly one $(c,d)\in(\mathbb F_q^\times)^2$. Hence the sum counts the solutions of $P(l)$ with $y\notin\mathbb F_q$. For
$y\in\mathbb F_q\setminus\{0,1\}$ there are exactly $q-2$ admissible pairs $(c,d)$, which gives the term $(q-2)^2$.
\end{proof}
The lemma was found by an AI referee and checked numerically in the release (\texttt{v5\_lemma\_I3.py}, $5\le q\le19$, ten values of $l$ each, with the controls $l=1$, where both sides
equal $q^3-q$, and $l=-1,2$, where both sides vanish). In particular $P(l)\ge(q-2)^2$ always.'''),
 # Theorem gal: b_q and (a) (math M1, m4)
 (r'''(Numerically, $b_q$ is the $q$-th coefficient of $\eta(2\tau)^3\eta(6\tau)^3$; this is not used below.)''',
  r'''($b_q$ is the $q$-th coefficient of the weight-3 newform $\eta(2\tau)^3\eta(6\tau)^3$ of level $12$, which has CM by $\mathbb Q(\sqrt{-3})$ \cite{LM}; this is the standard
Hecke-character description of a CM form, and we checked it for all primes $5\le q\le199$. It is not used below.)'''),
 (r'''\item[(a)] $P(2)=P(-1)=(q-2)^2$, the least possible value.''',
  r'''\item[(a)] $P(2)=P(-1)=(q-2)^2$, the least possible value. By Lemma~\ref{lem:I3} this is equivalent to the conic fact $(I_\lambda)_3=0$ of Section~6 \cite{JV,Pi}; we include it for completeness.'''),
 (r'''\item[(c)] $I(-2)=\big((q-2)(q+1)+b_q\big)/3$, hence $P(-2)=(q-2)(2q-1)+b_q$. In particular $P(3)=P(-2)$ when $q\equiv2\pmod3$.
\end{itemize}
\end{theorem}''',
  r'''\item[(c)] $I(-2)=\big((q-2)(q+1)+b_q\big)/3$, hence $P(-2)=(q-2)(2q-1)+b_q$. In particular $P(3)=P(-2)$ when $q\equiv2\pmod3$.
\end{itemize}
Equivalently (Lemma~\ref{lem:I3}), $\sum_\mu(I_3(\mu))_3=(q-2)(q+1)$ for $q\equiv2\pmod3$ and $\sum_\mu(I_{-2}(\mu))_3=(q-2)(q+1)+b_q$. (The unit condition: $l=\pm3$ is a unit modulo $m$ only for $q\equiv2\pmod3$.)
\end{theorem}
\noindent\emph{Corollary.} If $m$ is prime, then $\sum_{\rho\ne0,1}N(\rho)^2=\sum_{\lambda}\bigl(P(\lambda)-(q-2)^2\bigr)$, the sum over all units $\lambda$ (Section~6 and Lemma~\ref{lem:I3}).
So Conjecture~\ref{conj:var}, which is a sufficient condition for the order-3 case of the hypothesis of Proposition~\ref{prop:red}, is a statement about the average of $P(\lambda)$ over all $\lambda$.
Theorem~\ref{thm:gal} evaluates four of the roughly $q^2$ terms.'''),
 # proof of (b): c = d (math m3)
 (r'''Write $c\,y^3+d(1-y)^3-1$ as $(c-d)\,g(y)$''',
  r'''If $c=d$ the polynomial has degree $2$ and, as in (a), has no root outside $\mathbb F_q$. For $c\ne d$ write $c\,y^3+d(1-y)^3-1$ as $(c-d)\,g(y)$'''),
 # verification paragraph (repro M2, minor 4, 16)
 (r'''\item step (7) on $7\le q\le97$;''',
  r'''\item step (7): the Jacobi-sum part on all primes $q\equiv1\pmod3$, $7\le q\le97$ (including the choice of associate), the value $1/q$ for $q\equiv2\pmod3$ on all primes $5\le q\le97$;'''),
 (r'''The symbolic identities were checked with SymPy. An independent AI review (local, with its own code) found no error; it is not a human expert review.''',
  r'''The symbolic identities were checked with SymPy. A separate AI instance reviewed steps (1)--(6) with its own code and found no error. Step (7) for $q\equiv1\pmod3$ was written
after that review; it was checked numerically and by the AI referee reports prepared for Version~5, which corrected one sentence of the released proof (the choice of associate). None of these is a human expert review.'''),
 # geometric explanation hedged (math m6, repro minor 6)
 (r'''\emph{Geometric explanation (not used in the proof).} We identified the source of $b_q$ by exact computation. In the twisted form,''',
  r'''\emph{Geometric explanation (heuristic, not used in the proof).} In the twisted form,'''),
 (r'''The double cover branched at the $I_3$ and $I_1$ fibres is the singular K3 surface with fibres $3I_6+3I_2$ and transcendental lattice $\mathrm{diag}(2,6)$ \cite{HS},
which has complex multiplication by $\mathbb Q(\sqrt{-3})$; this is why the error term is a CM coefficient.''',
  r'''The fibre types were computed exactly. We expect the double cover branched at the $I_3$ and $I_1$ fibres to be the singular K3 surface with fibres $3I_6+3I_2$ and transcendental
lattice $\mathrm{diag}(2,6)$ \cite{HS}, which has complex multiplication by $\mathbb Q(\sqrt{-3})$, but we have not written down the isomorphism. This would explain why the error term is a CM coefficient.'''),
 # observations (math m10, repro minor 7)
 (r'''\item $P(4)=P(-2)$ for all 20 primes $5\le q\le79$ tested.''',
  r'''\item $P(4)=P(-2)$, i.e.\ $\sum_\mu(I_4)_3=\sum_\mu(I_{-2})_3$, for all 20 primes $5\le q\le79$ tested.'''),
 (r'''over the primes $47\le q\le79$ its standard deviation grows from about $1$ at $l=-2$ to about $4$ at $l=7$ (smaller $q$ include multiplier coincidences such as $l=q$, which inflate it).''',
  r'''over the primes $47\le q\le79$ (only $4$ to $8$ values of $q$ for each $l$) its standard deviation is about $1$ at $l=-2$ and about $4$ at $l=7$, but it is not monotone in the height, so this is a rough observation (smaller $q$ include multiplier coincidences such as $l=q$, which inflate it).'''),
 (r'''The Poisson-type laws of Sections~4--9 are an extension-field analogue''',
  r'''The Poisson-type laws of Sections~7--8 are an extension-field analogue'''),
 # what remains (math M2)
 (r'''By Proposition~\ref{prop:red}, a negative answer to the $O(1)$ question follows from $R_k\to0$ for each fixed $k$ and each $C$. For $k=3$ this follows
from Conjecture~\ref{conj:var}, or from any bound $o(q^4/\log q)$ on the variance. For $k\ge4$ a different decomposition is needed. In
Fourier terms the missing input is cancellation,''',
  r'''By Proposition~\ref{prop:red}, a negative answer to the $O(1)$ question would follow from Poisson convergence of all fixed-order factorial moments of $Z$, that is, $R_k\to0$ for each fixed $k$ and each $C$.
This is a full Poisson limit law for the window counts, not a single remaining estimate. For $k=3$ it reduces to a variance bound: Conjecture~\ref{conj:var}, or any bound $o(q^4/\log q)$ on the variance,
and by the Corollary of Section~\ref{sec:gal} this is a statement about the average of $P(\lambda)$ over all units $\lambda$. For $k\ge4$ we have no comparable reduction. In
Fourier terms the missing input for $k=3$ is cancellation,'''),
 # limitations (math M1, repro M3, minor 16)
 (r'''The statements labelled as proved were checked by an independent AI review and by exact computation, but not yet by a human expert. For Version~4 (searches on 30 October 2026: zbMATH Open, web, GitHub), we found no prior statement of Theorem~\ref{thm:gal} or of Proposition~\ref{prop:gal}.''',
  r'''The statements labelled as proved were checked by separate AI instances and by exact computation, but not yet by a human expert. For Version~4 (searches on 30 October 2026: zbMATH Open, web, GitHub), we found no prior statement of Theorem~\ref{thm:gal}(b),(c) or of Proposition~\ref{prop:gal}; Theorem~\ref{thm:gal}(a) is, by Lemma~\ref{lem:I3}, equivalent to the classical conic fact \cite{JV,Pi}.'''),
 (r'''Theorem~\ref{thm:gal}(c) relies on \cite[Thm.~1.7]{BK} (statement read; a preprint) and on standard facts from \cite{IR}.''',
  r'''Theorem~\ref{thm:gal}(c) relies on \cite[Thm.~1.7]{BK} (statement read; a preprint; we did not confirm a journal version) and on standard facts from \cite{IR}. All registrations in this paper are self-attested (Section~1).

\emph{Changes in Version~5.} This version corrects Version~4 after two AI referee reports (mathematics; reproducibility). They found no error in the statements or proofs of the paper; one sentence of the released proof file was wrong and is corrected (item 4).
(1) Lemma~\ref{lem:I3}: $P(l)-(q-2)^2$ is the per-dilation third moment of Section~6, so Theorem~\ref{thm:gal}(a) is a known fact and (b), (c) are exact third moments; we added the Corollary.
(2) The summary of what remains no longer speaks of a single remaining step that we isolate; the reduction of Section~\ref{sec:red} is described as folklore.
(3) The abstract gives the exact prime sets of the higher-moment tests (129 primes for $k\le6$ at $C=2$, 64 primes otherwise) and states that registrations are self-attested.
(4) Released: the programs behind the rows $q\ge4096$ of Table~\ref{tab:res} (\texttt{run\_nb\_top12.py}; \texttt{run\_orb.py}, which produced the blind test at $q=12167$) with a regression test and a per-row provenance table, and the raw output for $q=16807$; a script for Lemma~\ref{lem:I3};
a corrected sentence in the released proof of Theorem~\ref{thm:gal}(c) (step 7: the associate congruent to $1$ modulo $2$ is $\overline{\chi_3(2)}J(\chi_3,\chi_3)$); a claim-to-script table.
(5) Smaller fixes: the case $c=d$ in the proof of (b), the wording of the proof of Proposition~\ref{prop:gal}, hedged geometric explanation and height observation, two numbers ($54\%$, $q=16807$), the borderline row $q=125$ of Table~\ref{tab:pp}, the date of Version~4, the disclosure that step (7) was written after the first review, and the note on composite $m$ in Table~\ref{tab:res}.
Still open: a notation table, and exact theorem numbers for \cite{On} and \cite{IR}.'''),
 # separate AI instance wording elsewhere (repro minor 16)
 (r'''An independent review checked (a)--(c)
and the certificate logic''',
  r'''A separate AI review checked (a)--(c)
and the certificate logic'''),
 (r'''An independent AI review accepted it after the fixes included here.''',
  r'''A separate AI review accepted it after the fixes included here.'''),
 # data and code
 (r'''Version 4 additions (proof of Theorem~\ref{thm:gal}, verification scripts, independent review): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v4}.''',
  r'''Version 4 additions (proof of Theorem~\ref{thm:gal}, verification scripts, independent review): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v4}. Version 5 additions (\texttt{run\_orb.py} with regression test, Lemma~\ref{lem:I3} script, corrected proof file, claim-to-script table, referee reports): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v5}.'''),
 (r'\newtheorem{conjecture}{Conjecture}', r'\newtheorem{conjecture}{Conjecture}' '\n' r'\newtheorem{lemma}{Lemma}'),
 (r'\bibitem{MO}', r'\bibitem{LM} The LMFDB Collaboration, The L-functions and modular forms database, newform 12.3.c.a, \url{https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/12/3/c/a/}.' '\n' r'\bibitem{MO}'),
]
for old, new in R:
    assert s.count(old) == 1, ('edit target not found exactly once', old[:80], s.count(old))
    s = s.replace(old, new)
for bad in ['which we isolate', 'We did not find it in the literature', 'on 129 primes not previously used', 'An independent AI review (local']:
    assert bad not in s, bad
open(os.path.join(D, 'c9_note_v5.tex'), 'w', encoding='utf-8').write(s)
print('wrote c9_note_v5.tex,', len(R) + 1, 'edits, all asserted')
