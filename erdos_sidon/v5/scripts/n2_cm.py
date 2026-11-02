r"""PREDICTION (stated 2026-10-30 before running q=37..79): for q == 1 mod 3, What_twisted = What_untwisted - 3q = t^2 - 2q,  # LOCAL-OK: seconds
t = the EVEN integer with 4q = t^2 + 3 m^2 (sign irrelevant)  [= pi^2 + conj(pi)^2, weight-3 CM by Q(sqrt-3)]; for q == 2 mod 3 both CM terms 0.
Fitted by hand on q = 7, 13, 19, 31 (n2_k3.py output); this run tests q = 37, 43, 61, 67, 73, 79 out of sample.
CONTROL: recomputes q = 7 and 13 (must give 2 and -22 as in n2_k3.py)."""
import sys
from fq3 import field, p2_reps, chi
def sums(q):
    mul, inv, tr = field(q); tw = un = 0
    for u in p2_reps(q):
        T = tr(u); a2 = mul(u, u); p2, p3 = tr(a2), tr(mul(a2, u))
        Q = (T * T - p2) * pow(2, -1, q) % q; N = (T**3 - 3 * T * p2 + 2 * p3) * pow(6, -1, q) % q
        tw += chi((T * Q - N) * (T * Q - 9 * N), q)
    for x, y, z in p2_reps(q):
        T, Q, N = x + y + z, x*y + y*z + z*x, x*y*z
        un += chi((T * Q - N) * (T * Q - 9 * N), q)
    return tw, un
def pred(q):
    if q % 3 == 2: return 0
    t = next(t for t in range(0, 2 * int(q**0.5) + 2, 2) if (4 * q - t * t) % 3 == 0 and round(((4*q - t*t) / 3) ** 0.5) ** 2 == (4*q - t*t) // 3)
    return t * t - 2 * q
c = [sums(7)[0], sums(13)[0]]; print('CONTROL q=7,13 twisted', c, 'PASS' if c == [2, -22] else 'FAIL')
bad = 0
for q in map(int, sys.argv[1:]):
    tw, un = sums(q); p = pred(q); ok = tw == p and un - 3 * q == p; bad += not ok
    print('q=%d tw=%d un-3q=%d pred=%d %s' % (q, tw, un - 3 * q, p, 'HIT' if ok else 'MISS'))
print('misses:', bad)
