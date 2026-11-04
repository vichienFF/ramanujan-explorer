# Exploratory (char 5 compensation): A = sum chi(m H(s,m)) vs (1+phi(-1))q + phi(-1)phi(-3); B deficit vs C-B is -2q at 5,25,125.  # LOCAL-OK: seconds
# CONTROL: A formula holds at q=7,11,13 (Step 4d, read off 7..79).
from sage.all import GF
def AB(q):
    F = GF(q, 'a'); sq = {x*x for x in F if x != 0}; c = lambda v: 0 if v == 0 else (1 if v in sq else -1)
    Hf = lambda s, m: m**3+8*m*m-3*m*s*s+6*m*s+13*m+2*s**3+2*s*s-10*s+6
    A = sum(c(m*Hf(s, m)) for s in F for m in F); f1, f3 = c(F(-1)), c(F(-3))
    return A, (1+f1)*q + f1*f3
ctl = all(a == p for a, p in (AB(q) for q in (7, 11, 13)))
print('CONTROL:', 'PASS' if ctl else 'FAIL')
for q in (5, 25, 125): a, p = AB(q); print('q=%d A=%d formula %d diff %d (diff/q %s)' % (q, a, p, a - p, (a - p) / q))
