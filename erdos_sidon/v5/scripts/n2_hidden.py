r"""Hidden-symmetry scan for P(l) (2026-10-30, ANOMALY: P(4)=P(-2) on 20 primes).  # LOCAL-OK: minutes
For each q compute P(l) for ALL units l mod m, then test maps f(l) = (a l + b)/(c l + d) with small integer a,b,c,d (det != 0 mod m):
f is a symmetry at q if P(f(l)) = P(l) for every unit l with f(l) a unit. Report maps that are symmetries at EVERY tested q.
CONTROL (v1 result 2026-10-30): l->1/l (pair swap) must be found; l->l+1 must NOT. v0 also expected l->1-l: that was WRONG (E62) -
P(l) counts pairs v, l*v of Zech points (scaling), not lines of slope l, so y->1/y is a symmetry of the point set only."""
import sys, itertools
from math import gcd
from collections import Counter
from n1_char import field


def Ptable(q):
    log = field(q); m = q*q + q + 1; one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    pts = Counter((log[sub(one, y)] % m, log[y] % m) for y in log if sub(one, y) in log)
    U = [l for l in range(1, m) if gcd(l, m) == 1]
    return m, {l: sum(c * pts.get((l * x % m, l * y % m), 0) for (x, y), c in pts.items()) for l in U}


if __name__ == "__main__":  # import-safe (n2_classes imports Ptable)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    R = range(-3, 4)
    alive = {(a, b, c, d) for a, b, c, d in itertools.product(R, R, R, R) if a*d - b*c != 0 and (a, b, c, d) != (1, 0, 0, 1)}
    for q in map(int, sys.argv[1:]):
        m, P = Ptable(q)
        for f in list(alive):
            a, b, c, d = f; ok = True; used = 0
            for l, v in P.items():
                den = (c * l + d) % m
                if gcd(den, m) != 1: continue
                fl = (a * l + b) * pow(den, -1, m) % m
                if fl in P:
                    used += 1
                    if P[fl] != v: ok = False; break
            if not ok or used < len(P) // 2: alive.discard(f)
        print('q=%d m=%d units %d : surviving maps %d' % (q, m, len(P), len(alive))); sys.stdout.flush()
    found = sorted(alive)
    print('CONTROL l->1/l found, l->l+1 absent:', 'PASS' if (0, 1, 1, 0) in alive and (1, 1, 0, 1) not in alive else 'FAIL')
    for f in found: print('  symmetry l -> (%d l + %d)/(%d l + %d)' % f)
