# Wider-basis fit (all products of chi(-1),chi(2),chi(3),chi(5),chi(7) + q*{1,chi(-1),chi(-2),chi(-3)}) over primes 7..199 for N3'[X], M[X], D[X]=N3'-M.  # LOCAL-OK: est. < 15 min
# CONTROL: rest identity (p4_boundary) asserted at every prime.
import itertools, numpy as np
exec(open('p4_boundary.py', encoding='utf-8').read().split('for q in (7,')[0])
P = [p for p in range(7, 200) if all(p % d for d in range(2, int(p**.5)+1))]; data = []
for q in P:
    out, Tm1 = pieces(q); f1, f2, f3 = chi(-1, q), chi(-2, q), chi(-3, q)
    assert sum(a - b for a, b in out.values()) - Tm1 == -3*q + 12 + 5*f1 + 6*f2 + 4*f3
    data.append((q, out))
gens = (-1, 2, 3, 5, 7); subsets = [s for r in range(6) for s in itertools.combinations(gens, r)]
def row(q): 
    ch = {g: chi(g, q) for g in gens}; r = [int(np.prod([ch[g] for g in s])) if s else 1 for s in subsets]
    return r + [q, q*chi(-1, q), q*chi(-2, q), q*chi(-3, q)]
names = ['*'.join('c(%d)' % g for g in s) or '1' for s in subsets] + ['q', 'q c(-1)', 'q c(-2)', 'q c(-3)']
A = np.array([row(q) for q, _ in data], float); print('CONTROL rest identity on %d primes: PASS' % len(P)); print('E93 guard: rank(A) =', np.linalg.matrix_rank(A), 'of', A.shape[1], 'params', '(FITS BELOW NOT RELIABLE)' if np.linalg.matrix_rank(A) < A.shape[1] else '')
for X in ('c=1', 'c+d=0', 'rep', 'ALL'):
    for lab, fn in (("N3'", lambda o: o[0]), ('M', lambda o: o[1]), ('D', lambda o: o[0]-o[1])):
        y = np.array([sum(fn(v) for v in o.values()) if X == 'ALL' else fn(o[X]) for _, o in data], float)
        x, *_ = np.linalg.lstsq(A, y, rcond=None); xr = np.round(x*4)/4; ok = np.allclose(A @ xr, y)
        print('%-6s %-3s %s %s' % (X, lab, 'EXACT' if ok else 'NO FIT', ' + '.join('%g*%s' % (c, n) for c, n in zip(xr, names) if c) if ok else ''), flush=True)
# Direct check (not a fit): ALL D = rest + T_{-1} = -q + 10 + 5f1 + 6f2 + 2f3 - 2chi(-7)  (hand: T_{-1} = 2(q-1) - 2chi(-7) - 2f3)
okD = all(sum(a - b for a, b in o.values()) == -q + 10 + 5*chi(-1, q) + 6*chi(-2, q) + 2*chi(-3, q) - 2*chi(-7, q) for q, o in data)
print('ALL D direct formula on %d primes:' % len(data), okD, '| note: wide-basis lstsq is rank-deficient on 43 primes -> NO FIT lines above are not evidence against elementarity')
