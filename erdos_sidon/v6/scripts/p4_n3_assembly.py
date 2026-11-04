# N3 assembly: N3 = sum over ordered pairs of distinct roots of (#third roots), compared with the main term
# sum_{u,v}(1+chi(u^2-4v))(1+chi(-D4)) = q^2 + phi(-1)(S_a+S_b). Prints the exclusion term E by CATEGORY so each can be proved by hand.  # LOCAL-OK: < 5 min (q <= 61)
# CONTROLS: total of 'actual' equals N3 from p4_n3.py's Ns(q) (independent counting by (c,d)); E equals N3 - q^2 - phi(-1)(S_a+S_b) with S_a,S_b brute-forced.
import sys, numpy as np
from collections import defaultdict
exec(open('p4_n3.py', encoding='utf-8').read().split('REF =')[0])
def chi(a, q): a %= q; return 0 if a == 0 else (1 if pow(a, (q - 1) // 2, q) == 1 else -1)
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
def run(q):
    inv = lambda a: pow(a % q, q - 2, q); Y = np.arange(q)
    def r_of(c, d): return int(np.count_nonzero((c * Y**4 + d * (1 - Y)**4 - 1) % q == 0))
    cat = defaultdict(int); actual_total = 0
    for t1 in range(q):
        for t2 in range(q):
            if t1 == t2: continue
            u, v = (t1 + t2) % q, t1 * t2 % q; main = 1 + chi(-D4(u, v), q)
            if t1 == q - 1 or t2 == q - 1: cat['t=-1 (y=inf)'] -= main; continue
            a1, a2 = pow(t1, 4, q), pow(t2, 4, q); b1, b2 = pow(1 + t1, 4, q), pow(1 + t2, 4, q)
            if a1 == a2:
                act = 0
                for c in range(1, q):
                    d = (b1 - c * a1) % q
                    if d and (b2 - c * a2 - d) % q == 0: act += r_of(c, d) - 2
                cat['singular t1^4=t2^4'] += act - main; actual_total += act; continue
            c = (b1 - b2) * inv(a1 - a2) % q; d = (b1 - c * a1) % q
            if c == 0 or d == 0: cat['c=0 or d=0'] -= main; continue
            act = r_of(c, d) - 2; actual_total += act
            key = 'generic' if act == main else ('c=1 (root y=1)' if c == 1 else ('c+d=0' if (c + d) % q == 0 else 'repeated/other'))
            cat[key] += act - main
    cat['diagonal u^2=4v'] -= sum(1 + chi(-D4(2 * t % q, t * t % q), q) for t in range(q))
    for y2 in range(q):                                   # pairs containing y=1 (t=inf): c=1
        if y2 == 1: continue
        d = (1 - pow(y2, 4, q)) * inv(pow(1 - y2, 4, q)) % q
        if d == 0: continue
        act = r_of(1, d) - 2; cat['pairs with y=1'] += 2 * act; actual_total += 2 * act
    return cat, actual_total
for q in [int(a) for a in sys.argv[1:]] or [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
    cat, tot = run(q); N = Ns(q); f = {a: chi(-a, q) for a in (1, 2, 3)}
    Sa = sum(chi(D4(u, v), q) for u in range(q) for v in range(q)); Sb = sum(chi(u*u - 4*v, q) * chi(D4(u, v), q) for u in range(q) for v in range(q))
    E = N[3] - q*q - f[1] * (Sa + Sb); pred = -(10 + 6*f[1])*q + 25 + 18*f[1] + 9*f[2] + 4*f[3]
    print('q=%d CONTROL actual==N3 %s, sum(cat)==E %s, E==pred %s | f1,f2,f3=%d,%d,%d |' % (q, tot == N[3], sum(cat.values()) == E, E == pred, f[1], f[2], f[3]), dict(sorted(cat.items())), flush=True)
