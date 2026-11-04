r"""Split S_b = A + B with s = x^2: A = sum_{s,m} chi(m H(s,m)), B = sum_{s,m} chi(s m H(s,m)).  # LOCAL-OK: ~1 min
Hypothesis: A elementary (double plane branched over line+cubic = rational surface), B carries f1*b_q (K3).
Also: singular points of the cubic H(s,m)=0 (sympy) -> if nodal, rational cubic.
CONTROL: A + B equals S_b computed directly from D4 (p4_charsum definition) at every q (independent formula path)."""
import sys
exec(open('p4_charsum.py', encoding='utf-8').read().split('# control:')[0])
from sympy import symbols, solve, diff, factor
s_, m_ = symbols('s m')
Hs = m_**3 + 8*m_**2 - 3*m_*s_**2 + 6*m_*s_ + 13*m_ + 2*s_**3 + 2*s_**2 - 10*s_ + 6
print('singular points of H=0:', solve([Hs, diff(Hs, s_), diff(Hs, m_)], [s_, m_], dict=True))
def H(s, m): return m**3 + 8*m**2 - 3*m*s*s + 6*m*s + 13*m + 2*s**3 + 2*s*s - 10*s + 6
ok = True
for q in [p for p in range(7, 80) if all(p % k for k in range(2, int(p ** .5) + 1))]:
    f1, f3 = chi(-1, q), chi(-3, q)
    A = sum(chi(m * H(s, m), q) for s in range(q) for m in range(q)); B = sum(chi(s * m * H(s, m), q) for s in range(q) for m in range(q))
    Sb = sum(chi(u * u - 4 * v, q) * chi(D4(u, v), q) for u in range(q) for v in range(q)); ok &= A + B == Sb
    print('q=%d f1 %+d f2 %+d f3 %+d b %+d | A %+d | B %+d | B - f1 b %+d' % (q, f1, chi(-2, q), f3, bq(q), A, B, B - f1 * bq(q)))
print('CONTROL A+B == S_b:', 'PASS' if ok else 'FAIL')
