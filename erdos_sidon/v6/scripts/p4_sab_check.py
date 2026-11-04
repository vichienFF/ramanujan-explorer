r"""Check the read-off closed forms (fitted on q=7..113 by eye from p4_charsum.py) on NEW primes 127..199.  # LOCAL-OK: seconds
S_a = (3+f1) q + f1 f3 (corrected 11-02: first read-off had sign -f3, failed blind on q=1 mod 4); S_b = (3+2 f1) q + f1 (f3 + b_q)   (f_a = chi(-a)); q=5 excluded (small-prime anomaly).
CONTROL: reproduces p4_charsum.py printed values at q=13 (S_a 53, S_b 44) and q=19 (37, -8)."""
import sys
exec(open('p4_charsum.py', encoding='utf-8').read().split('# control:')[0])
def S(q):
    Sa = sum(chi(D4(u, v), q) for u in range(q) for v in range(q)); Sb = sum(chi(u * u - 4 * v, q) * chi(D4(u, v), q) for u in range(q) for v in range(q)); return Sa, Sb
ctl = S(13) == (53, 44) and S(19) == (37, -8); print('CONTROL:', 'PASS' if ctl else 'FAIL')
if not ctl: sys.exit(1)
res = []
for q in [p for p in range(127, 200) if all(p % k for k in range(2, int(p ** .5) + 1))]:
    f1, f3 = chi(-1, q), chi(-3, q); Sa, Sb = S(q)
    res.append((q, Sa == (3 + f1) * q + f1 * f3, Sb == (3 + 2 * f1) * q + f1 * (f3 + bq(q))))
print(res); print('ALL EXACT on new primes:', all(a and b for _, a, b in res))
