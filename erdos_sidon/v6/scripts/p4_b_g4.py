r"""Blind check C-B: B = sum_{s,m} chi(s m H(s,m)) = G(4) + 2q  (read off q=7..79 in p4_ab_split.py); new primes 83..139.  # LOCAL-OK: ~2 min
Also checks the node-projection form: B = (q-2) + sum_k sum_{s != 1} chi(s (k(s-1)-4) L_k(s)), L_k = (k-1)^2(k+2)s - (k-2)(k+3)^2.
CONTROL: G(4) satisfies 1 + f1 G(4) = q + 1 + b_q (Thm 3c, independent) on each q."""
import sys
exec(open('p4_sb_g4.py', encoding='utf-8').read().split('ok_ctl = True')[0])
def H(s, m): return m**3 + 8*m**2 - 3*m*s*s + 6*m*s + 13*m + 2*s**3 + 2*s*s - 10*s + 6
ok = True; ctl = True; proj = True
for q in [p for p in range(83, 140) if all(p % k for k in range(2, int(p ** .5) + 1))]:
    f1 = chi(-1, q); g = G(4, q); ctl &= 1 + f1 * g == q + 1 + bq(q)
    B = sum(chi(s * m * H(s, m), q) for s in range(q) for m in range(q)); ok &= B == g + 2 * q
    Bp = (q - 2) + sum(chi(s * (k * (s - 1) - 4) * ((k - 1)**2 * (k + 2) * s - (k - 2) * (k + 3)**2), q) for k in range(q) for s in range(q) if s != 1)
    proj &= Bp == B
print('CONTROL:', 'PASS' if ctl else 'FAIL'); print('C-B blind 83..139:', ok); print('node-projection form equals B:', proj)
sys.exit(0 if ok and ctl and proj else 1)
