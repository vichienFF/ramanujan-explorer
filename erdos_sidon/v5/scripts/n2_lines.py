r"""S2 bookkeeping (2026-10-30): S2 = sum over admissible unordered pairs of chi(disc); over ALL (u,v) the same weight (1+chi(u^2-4v))/2 * chi(D),
D = u(u-2)(2v-u)(2v-u+2) (disc times den^2), sums to (1+T)/2 (hand). Here: list each excluded line's contribution so each can be
evaluated by hand.  Lines: L0 v=0 (root 0), L1 v=u-1 (root 1), and pairs failing det!=0 / c!=0 / d!=0 (identified numerically).  # LOCAL-OK: seconds
CONTROL: (1+T)/2 - sum(all excluded contributions) must equal S2 from n2_pairs.pairs() at every q."""
import sys
from n2_pairs import pairs, chi   # n2_pairs runs its own CONTROL at import
def run(q):
    T = sum(chi((x*x-1)*(z*z-1)*(x*x+1-2*z), q) for x in range(q) for z in range(q))
    W = lambda u, v: ((1 + chi(u*u - 4*v, q)) * chi(u*(u-2)*(2*v-u)*(2*v-u+2), q))  # = 2 x weight
    adm = set()
    for y1 in range(2, q):
        for y2 in range(y1 + 1, q):
            A = [[(1-y1)**2 % q, y1*y1 % q], [(1-y2)**2 % q, y2*y2 % q]]; det = (A[0][0]*A[1][1]-A[0][1]*A[1][0]) % q
            if det == 0: continue
            r1 = y1*y1*(1-y1)**2 % q; r2 = y2*y2*(1-y2)**2 % q; di = pow(det, -1, q)
            c = (r1*A[1][1]-A[0][1]*r2)*di % q; d = (A[0][0]*r2-r1*A[1][0])*di % q
            if c and d: adm.add(((y1+y2) % q, y1*y2 % q))
    cats = {'v=0': 0, 'v=u-1': 0, 'u^2=4v': 0, 'other': 0}; examples = []
    for u in range(q):
        for v in range(q):
            if (u, v) in adm: continue
            w = W(u, v)
            k = 'v=0' if v == 0 else 'v=u-1' if (v - u + 1) % q == 0 else 'u^2=4v' if (u*u - 4*v) % q == 0 else 'other'
            cats[k] += w
            if k == 'other' and w and len(examples) < 4: examples.append((u, v, (2*v-u) % q, (2*v-u+2) % q))
    S2 = pairs(q)[1]; tot = (1 + T - sum(cats.values())) / 2   # split pairs weight 1, diagonal u^2=4v weight 1/2 (fixed after CONTROL FAIL, E58)
    return T, S2, cats, tot, examples
for q in map(int, sys.argv[1:]):
    T, S2, cats, tot, ex = run(q)
    print('q=%d T=%d S2=%d recon=%.1f %s | excluded 2xweight sums %s | other examples (u,v,2v-u,2v-u+2) %s' % (q, T, S2, tot, 'CONTROL PASS' if tot == S2 else 'CONTROL FAIL', cats, ex))
