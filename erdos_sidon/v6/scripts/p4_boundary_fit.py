# Fit closed forms for N3'[X], M[X] (X = c=1, c+d=0, rep) from p4_boundary.pieces over primes 7..67 (read-off; hand proofs follow).  # LOCAL-OK: < 5 min
# CONTROL: p4_boundary's own control (rest == -3q+12+5f1+6f2+4f3) re-checked on every prime used here.
import itertools, numpy as np
src = open('p4_boundary.py', encoding='utf-8').read().split('for q in (7,')[0]; exec(src)
P = [p for p in range(7, 68) if all(p % d for d in range(2, int(p**.5)+1))]; data = []
for q in P:
    out, Tm1 = pieces(q); f = {a: chi(-a, q) for a in (1, 2, 3, 7)}
    assert sum(a - b for a, b in out.values()) - Tm1 == -3*q + 12 + 5*f[1] + 6*f[2] + 4*f[3]
    data.append((q, f, out))
names = ['1', 'f1', 'f2', 'f3', 'f7', 'f1f2', 'f1f3', 'f1f7', 'f2f3', 'q', 'q f1', 'q f2', 'q f3']
def row(q, f): return [1, f[1], f[2], f[3], f[7], f[1]*f[2], f[1]*f[3], f[1]*f[7], f[2]*f[3], q, q*f[1], q*f[2], q*f[3]]
A = np.array([row(q, f) for q, f, _ in data], float)
print('CONTROL rest identity on', len(P), 'primes: PASS')
for X in ('c=1', 'c+d=0', 'rep'):
    for j, lab in ((0, "N3'"), (1, 'M')):
        y = np.array([o[X][j] for _, _, o in data], float); x, *_ = np.linalg.lstsq(A, y, rcond=None); xr = np.round(x*4)/4
        print('%-6s %-3s %s %s' % (X, lab, 'EXACT' if np.allclose(A @ xr, y) else 'NO FIT', ' + '.join('%g*%s' % (c, n) for c, n in zip(xr, names) if c)))
