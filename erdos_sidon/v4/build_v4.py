"""Build c9_note_v4.tex from c9_note_v3.tex + v4_new.tex (Version 4). All edits asserted before writing (as build_v3.py)."""
import os
D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, 'c9_note_v3.tex'), encoding='utf-8').read()
new = open(os.path.join(D, 'v4_new.tex'), encoding='utf-8').read()
R = [
 (r'a resonance theorem, and a reduction}',
  r'a resonance theorem, exact Galois autocorrelations,\\ and a reduction}'),
 (r'\date{Version 3, 21 October 2026 (Version 2: 19 October 2026; Version 1: 16 October 2026)}',
  r'\date{Version 4, 31 October 2026 (Version 3: 21 October 2026; Version 2: 19 October 2026; Version 1: 16 October 2026)}'),
 (r'(an average over dilates), which we isolate but do not prove; the Erd\H{o}s question remains open.',
  r"(an average over dilates), which we isolate but do not prove; the Erd\H{o}s question remains open. \emph{New in Version 4:} exact values of the Galois autocorrelation $C(l)$ of the underlying Jacobi sums at $l=2,-1$ (minimal) and $l=3,-2$: $C(l)$ is an explicit function of an elementary count $P(l)$ (Proposition~\ref{prop:gal}), $P(2)=P(-1)=(q-2)^2$, $P(3)=(q-2)(2q-1)$ for $q\equiv2\pmod3$, and $P(-2)=(q-2)(2q-1)+b_q$ for every prime $q\ge5$, where $b_q=0$ for $q\equiv2\pmod3$ and $b_q=4x^2-2q$ for $q=x^2+3y^2$ (numerically the $q$-th coefficient of the CM form $\eta(2\tau)^3\eta(6\tau)^3$) (Theorem~\ref{thm:gal}; one step uses a known evaluation of a finite-field hypergeometric value, due to Ono and in the general form of Barman and Kalita)."),
 (r'\section{What remains}\label{sec:rem}', new + '\n' + r'\section{What remains}\label{sec:rem}'),
 (r'beyond the square-root (Weil--Deligne) bound for single sums. We do not know how to prove it.',
  r'beyond the square-root (Weil--Deligne) bound for single sums. We do not know how to prove it. Section~\ref{sec:gal} evaluates these correlations exactly at a few small dilations. Three cheap routes to the averaged bound failed in our tests: the exact formulas grow in complexity with the height of the dilation; among small heights (numerators and denominators $\le12$, avoiding $3$ and $7$) we found no further coincidences of $P$ beyond those explained by Theorem~\ref{thm:gal} and one unexplained class; and maximum bounds for roots of trinomials \cite{BCR} are far too weak for an $L^2$ statement.'),
 (r'The statements labelled as proved were checked by an independent AI review and by exact computation, but not yet by a human expert.',
  r'The statements labelled as proved were checked by an independent AI review and by exact computation, but not yet by a human expert. For Version~4 (searches on 30 October 2026: zbMATH Open, web, GitHub), we found no prior statement of Theorem~\ref{thm:gal} or of Proposition~\ref{prop:gal}. Also not checked for Version~4: the original paper of Jungnickel and Vedder, the full text of the paper of Ono, and a 2005 essay on Singer sets (A.~Chmelnitzki), whose server was unreachable. Theorem~\ref{thm:gal}(c) relies on \cite[Thm.~1.7]{BK} (statement read; a preprint) and on standard facts from \cite{IR}.'),
 (r'Version 3 additions (Lean files, Sage scripts for Theorem~\ref{thm:res}, resonance blind tests): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v3}.',
  r'Version 3 additions (Lean files, Sage scripts for Theorem~\ref{thm:res}, resonance blind tests): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v3}. Version 4 additions (proof of Theorem~\ref{thm:gal}, verification scripts, independent review): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v4}.'),
 (r'\bibitem{Si}',
  r'\bibitem{BK} R.~Barman, G.~Kalita, Certain values of Gaussian hypergeometric series and a family of algebraic curves, arXiv:1208.0495 (2012).' + '\n' +
  r'\bibitem{BCR} J.~Bi, Q.~Cheng, J.~M.~Rojas, Sub-linear root detection, and new hardness results, for sparse polynomials over finite fields, Proc. ISSAC 2013, 61--68.' + '\n' +
  r'\bibitem{HS} K.~Hulek, M.~Sch\"utt, Arithmetic of singular Enriques surfaces, Algebra Number Theory 6 (2012) 195--230; arXiv:1002.1598, Example 3.1.' + '\n' +
  r'\bibitem{Gre} J.~Greene, Hypergeometric functions over finite fields, Trans. Amer. Math. Soc. 301 (1987) 77--101.' + '\n' +
  r'\bibitem{IR} K.~Ireland, M.~Rosen, A Classical Introduction to Modern Number Theory, 2nd ed., Springer 1990, Chapters 8, 9 and 11.' + '\n' +
  r'\bibitem{Ke} Z.~Kelley, The number of roots of trinomials over prime fields, Texas A\&M REU report and slides (2015).' + '\n' +
  r'\bibitem{KO} Z.~Kelley, S.~Owen, Estimating the number of roots of trinomials over finite fields, arXiv:1510.01758 (2015).' + '\n' +
  r'\bibitem{On} K.~Ono, Values of Gaussian hypergeometric series, Trans. Amer. Math. Soc. 350 (1998) 1205--1223.' + '\n' + r'\bibitem{Si}'),
]
for a, b in R:
    assert s.count(a) == 1, ('pattern count != 1', a[:70], s.count(a))
    s = s.replace(a, b)
assert '\r' not in s
# CONTROL: known structure - every pattern matched exactly once (above); new labels present exactly once; V3 theorems still present.
for lab in (r'\label{sec:gal}', r'\label{thm:gal}', r'\label{prop:gal}', r'\label{thm:res}', r'\label{prop:orb}', r'\label{sec:rem}'):
    assert s.count(lab) == 1, ('CONTROL FAIL label', lab, s.count(lab))
open(os.path.join(D, 'c9_note_v4.tex'), 'w', encoding='utf-8').write(s)
print('ok', len(s))
