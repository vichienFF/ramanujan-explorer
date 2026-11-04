# Exploratory char 5: S_a = sum chi(D4), S_b = sum chi(u^2-4v)chi(D4) over F_q^2 vs read-off forms (3+f1)q+f1f3 and (3+2f1)q+f1(f3+b_q).  # LOCAL-OK: < 2 min
# CONTROL: reproduces p4_charsum.py values q=13 (53,44) and q=19 (37,-8).
from sage.all import GF
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
def S(q):
    F = GF(q, 'a'); sq = {x*x for x in F if x != 0}; c = lambda v: 0 if v == 0 else (1 if v in sq else -1)
    return sum(c(D4(u, v)) for u in F for v in F), sum(c(u*u - 4*v) * c(D4(u, v)) for u in F for v in F), c(F(-1)), c(F(-3))
ctl = S(13)[:2] == (53, 44) and S(19)[:2] == (37, -8); print('CONTROL:', 'PASS' if ctl else 'FAIL')
for q, b in ((5, 0), (25, 50), (125, 0)):
    a, s, f1, f3 = S(q); pa = (3+f1)*q + f1*f3; pb = (3+2*f1)*q + f1*(f3+b)
    print('q=%d S_a=%d (form %d, diff %d) S_b=%d (form %d, diff %d)' % (q, a, pa, a-pa, s, pb, s-pb))
