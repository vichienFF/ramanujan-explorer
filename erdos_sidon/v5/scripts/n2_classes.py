r"""Data-first: equality classes of P(l) over small-height rationals l=a/b (|a|,|b|<=6) that hold at EVERY tested q.  # LOCAL-OK: minutes
CONTROL: l and 1/l always in one class (pair-swap, the only small Mobius symmetry, n2_hidden.py); P(2)=P(-1) (N1-CONIC theorem)."""
import sys
from math import gcd
from fractions import Fraction as Fr
from n2_hidden import Ptable
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = 6
if len(sys.argv) > 1 and sys.argv[1].startswith('H='): H = int(sys.argv.pop(1)[2:])  # usage: python n2_classes.py H=12 q1 q2 ...
rats = sorted({Fr(a, b) for a in range(-H, H + 1) for b in range(1, H + 1) if a != 0 and Fr(a, b) != 1}, key=lambda r: (abs(r.numerator) + r.denominator, r))
sig = {r: [] for r in rats}
for q in map(int, sys.argv[1:]):
    m, P = Ptable(q)
    for r in rats:
        sig[r].append(P.get(r.numerator * pow(r.denominator, -1, m) % m) if gcd(r.denominator, m) == 1 else None)
classes = {}
for r in rats:
    if None not in sig[r]: classes.setdefault(tuple(sig[r]), []).append(r)
ok = all(sig[r] == sig[1 / r] for r in rats if None not in sig[r] and None not in sig.get(1 / r, [None])) and sig[Fr(2)] == sig[Fr(-1)]
print('CONTROL l~1/l and P(2)=P(-1):', 'PASS' if ok else 'FAIL')
for k, v in sorted(classes.items(), key=lambda kv: -len(kv[1])):
    if len(v) > 2: print(len(v), [str(x) for x in v][:18])
