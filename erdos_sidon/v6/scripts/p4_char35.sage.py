# Exploratory: does C-B  B(q) = 2q + phi(-1)q + chi(3) b_q  hold in char 3 / char 5 (outside the Livne proof scope)?  # LOCAL-OK: < 2 min
# CONTROL: same evaluator reproduces the char>=7 values q=7 (B=5), 13 (B=17) from p4_bookkeep output; b_q via Frobenius power sums from b_p.
from sage.all import GF
def bp(p):
    if p % 3 != 1: return 0
    x = next(x for x in range(1, p) if any(x*x + 3*t*t == p for t in range(1, p))); return 4*x*x - 2*p
def bq(p, n):   # alpha^n+beta^n, alpha+beta=b_p, alpha*beta=(-3/p)p^2 (p=3: ramified, alpha=beta... use b_3 from 12.3.c.a)
    s0, s1 = 2, bp(p); e = p*p*(0 if p == 3 else (1 if pow(-3 % p, (p-1)//2, p) == 1 else -1))
    for _ in range(n - 1): s0, s1 = s1, s1 * bp(p) - e * s0
    return s1 if n >= 1 else 2
def B(q):
    F = GF(q, 'a'); sq = {x*x for x in F if x != 0}; c = lambda v: 0 if v == 0 else (1 if v in sq else -1)
    return sum(c(s*m*(m**3+8*m*m-3*m*s*s+6*m*s+13*m+2*s**3+2*s*s-10*s+6)) for s in F for m in F), c(F(-1)), c(F(3))
ctl = B(7)[0] == 5 and B(13)[0] == 17
print('CONTROL:', 'PASS' if ctl else 'FAIL', flush=True)
PN = [tuple(map(int, a.split("^"))) for a in __import__("sys").argv[1:]] or [(3, 2), (3, 3), (3, 4), (3, 5), (5, 1), (5, 2), (5, 3)]
for p, n in PN:
    q = p**n; b, f1, c3 = B(q); pred = 2*q + f1*q + c3*bq(p, n)
    print('q=%d B=%d predicted %d -> %s' % (q, b, pred, 'HOLDS' if b == pred else 'FAILS (diff %d)' % (b - pred)), flush=True)
