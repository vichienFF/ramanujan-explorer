"""Build c9_note_v3.tex from c9_note_v2.tex + v3_new.tex (Version 3). All edits asserted before writing."""
import os
D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, 'c9_note_v2.tex'), encoding='utf-8').read()
new = open(os.path.join(D, 'v3_new.tex'), encoding='utf-8').read()
R = [
 (r'a curve-counting theorem, forbidden-structure laws,\\ and a reduction}',
  r'a curve-counting theorem, forbidden-structure laws,\\ a resonance theorem, and a reduction}'),
 (r'\date{Version 2, 19 October 2026 (Version 1, 16 October 2026: numerical evidence only)}',
  r'\date{Version 3, 21 October 2026 (Version 2: 19 October 2026; Version 1: 16 October 2026)}'),
 (r"The remaining step towards Erd\H{o}s's question is a uniform estimate",
  r"\emph{New in Version 3:} $3k\mid N(\rho)$ (a free multiplier action, partly machine-checked in Lean), and a resonance theorem for cube $q=r^3$. For the six ratios of the $S_3$-orbit of $r+r^{-1}$ (roots modulo $m$ of $x^3-3x+1$ and $x^3-3x^2+1$), every point of the Singer line not fixed by the $q$-Frobenius has exactly $r$ partners, so $N(\rho)=r(q+1-e)$ with $e\in\{0,1\}$ ($m$ prime). This explains most of the excess of the variance ratio for cube $q$. There is one pre-registered blind test of the predicted excess ($q=12167$), and pre-registered tests of the resonant orbit and of $M/\mu\approx r$ ($q=4913,6859,15625$). The remaining step towards Erd\H{o}s's question is a uniform estimate"),
 (r'(an average over dilates), which we isolate but do not prove.',
  r"(an average over dilates), which we isolate but do not prove; the Erd\H{o}s question remains open."),
 (r'We did not find it in the literature (Section~10).', r'We did not find it in the literature (Section~\ref{sec:lim}).'),
 (r'Sections~4--9 (new in Version~2)', r'Sections~4--8 and~\ref{sec:rem} (new in Version~2; Sections~\ref{sec:orb}--\ref{sec:resblind} are new in Version~3)'),
 (r'\section{Limitations, literature and disclosure}', r'\section{Limitations, literature and disclosure}\label{sec:lim}'),
 (r'$\sum_{\rho}(N(\rho)-E)^2=r\,\sum_\rho E\,(1+o(1))$, where $r$ is the order of the multiplier group ($r=3$ for prime $q$, $r=3k$ for',
  r'$\sum_{\rho}(N(\rho)-E)^2=|G|\,\sum_\rho E\,(1+o(1))$, where $|G|$ is the order of the multiplier group ($|G|=3$ for prime $q$, $|G|=3k$ for'),
 ("For $m$ prime the multiplier $q$ acts freely on distinct triples, so $N(\\rho)\\equiv0\\pmod3$ (observed also for all prime powers\ncomputed).",
  r"By Proposition~\ref{prop:orb} (Section~\ref{sec:orb}), $3k\mid N(\rho)$ for every prime power $q=p^k$."),
 (r'the two misses and the largest excesses occur for $k=3$, which we have not explained;',
  r'the two misses and most of the excess at cube $q$ are accounted for by the resonance of Section~\ref{sec:res} (Table~\ref{tab:res});'),
 (r'a further shard $2209\le q\le3125$ is registered and pending).',
  r'later runs: all 11 later non-cube $q$ ($2209,2401,2809,3125,3481,3721,4489,6561,8192,14641,16384$) give ratio$/3k\in[0.9980,1.0026]$; the later cube $q=4096,4913,6859$ give $1.022,1.038,1.064$, see Table~\ref{tab:res}).'),
 (r'\section{What remains}\label{sec:rem}', new + '\n' + r'\section{What remains}\label{sec:rem}'),
 ("The higher-moment and variance laws are\nnumerical.",
  "The higher-moment and variance laws are\nnumerical. " + r"Theorem~\ref{thm:res} is proved; two polynomial identities and one factorisation in its proof were verified by exact computer algebra (Sage 10.7; the scripts and their SHA-256 hashes are released) rather than by hand. The excess formula of Section~\ref{sec:resblind} is a heuristic, not a theorem. For Version~3, a search (web, zbMATH Open, three full texts; 20 October 2026) found no prior statement of Theorem~\ref{thm:res}. Proposition~\ref{prop:orb} is elementary and probably known."),
 (r'blind-test plans with SHA-256 ledger, Kaggle outputs): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v2}.',
  r'blind-test plans with SHA-256 ledger, Kaggle outputs): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v2}. Version 3 additions (Lean files, Sage scripts for Theorem~\ref{thm:res}, resonance blind tests): \url{https://github.com/vichienFF/ramanujan-explorer/tree/main/erdos_sidon/v3}.'),
 (r'\bibitem{Si}',
  r'\bibitem{Ha} M.~Hall, Jr., Cyclic projective planes, Duke Math. J. 14 (1947) 1079--1090.' + '\n' +
  r'\bibitem{MR} R.~L.~McFarland, B.~F.~Rice, Translates and multipliers of abelian difference sets, Proc. Amer. Math. Soc. 68 (1978) 375--379.' + '\n' + r'\bibitem{Si}'),
]
for a, b in R:
    assert s.count(a) == 1, ('pattern count != 1', a[:70], s.count(a))
    s = s.replace(a, b)
assert '\r' not in s
open(os.path.join(D, 'c9_note_v3.tex'), 'w', encoding='utf-8').write(s)
print('ok', len(s))
