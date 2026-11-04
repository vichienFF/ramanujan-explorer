r"""Conjecture C-SB: S_b = G(4) + (3+f1) q + f1 f3, where G(l) = sum_{x,y} chi(x)chi(y)chi(1-x)chi(1-y)chi(x-l y) (Greene 3F2 numerator, as in N2_PROOF Step 4).  # LOCAL-OK: ~1 min
Motivation: N2_PROOF Step 4/7 gives T(l=-2) = 1 + f1 G(4) = q + 1 + b_q, so G(4) = f1 (q + b_q); S_b's b_q part is f1 b_q.
CONTROL: G(4) here reproduces the proved/cited identity 1 + f1*G(4) = q + 1 + b_q (independent route: Thm 3c Step 7) on every q tested."""
import sys
exec(open('p4_charsum.py', encoding='utf-8').read().split('# control:')[0])
def G(l, q):
    c = [chi(a, q) for a in range(q)]
    return sum(c[x] * c[y] * c[(1 - x) % q] * c[(1 - y) % q] * c[(x - l * y) % q] for x in range(q) for y in range(q))
ok_ctl = True; ok = True
for q in [p for p in range(7, 110) if all(p % k for k in range(2, int(p ** .5) + 1))]:
    f1, f3 = chi(-1, q), chi(-3, q); g = G(4, q)
    ok_ctl &= 1 + f1 * g == q + 1 + bq(q)
    Sb = sum(chi(u * u - 4 * v, q) * chi(D4(u, v), q) for u in range(q) for v in range(q))
    ok &= Sb == g + (3 + f1) * q + f1 * f3
print('CONTROL 1 + f1 G(4) = q+1+b_q:', 'PASS' if ok_ctl else 'FAIL'); print('C-SB exact on q=7..109:', ok)
sys.exit(0 if ok_ctl and ok else 1)
