# c=1 class: check the hand decomposition D[c=1] = N3'[c=1] - M[c=1] = sum_members |R|(|R|^2-1) - 2P + U - Sadj  (Step 4zf), then hand forms.  # LOCAL-OK: seconds
# CONTROL: N3', M recomputed by p4_boundary.pieces (independent code path) must equal the decomposition at every q.
exec(open('p4_boundary.py', encoding='utf-8').read().split('for q in (7,')[0])
def c1_parts(q):
    g = lambda t: ((1+t)**4 - t**4) % q
    roots = {}
    for t in range(q):
        if (t+1) % q: roots.setdefault(g(t), []).append(t)
    S1 = P = U = Sadj = 0
    for d, R in roots.items():
        if d == 0: continue
        n = len(R); S1 += n*(n*n-1); r = n + 1
        for a in R:
            for b in R:
                if a == b: continue
                if pow(a, 4, q) == pow(b, 4, q): Sadj += r - 2; continue
                P += 1; U += ((a+b) % q) in (0, q-1, q-2)
    return S1 - 2*P + U - Sadj, (S1, P, U, Sadj)
for q in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
    out, _ = pieces(q); D, parts = c1_parts(q)
    print('q=%d CONTROL D==N3\'-M %s | D=%d parts(S1,P,U,Sadj)=%s | f1 f2 f3 f7 = %d %d %d %d' % (q, D == out['c=1'][0] - out['c=1'][1], D, parts, chi(-1,q), chi(-2,q), chi(-3,q), chi(-7,q)))
