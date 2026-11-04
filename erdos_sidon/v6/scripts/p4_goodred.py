"""Good reduction of the C-B elliptic K3 (P4_CB_PROOF.md Step 2) at every p >= 7: exact local data at each bad place.
E_k: Y^2 = X(X-e1)(X-e2), e1 = (k-1)^2(k+2)(k+4), e2 = k(k-2)(k+3)^2. At a bad place k0 the two coinciding roots r1, r2 of the cubic
satisfy r1 - r2 = t^m g(t) (t = local parameter); with the third root r3, the local equation is Y^2 = u (X'^2 - t^{2m} g^2/4), u(0) = r_node - r3,
i.e. an A_{2m-1} point / I_{2m} fibre over Z_(p) as long as g(0), u(0) (and 2) are p-units. The script prints these constants and their primes.
CONTROL: the fibre configuration must reproduce the char-0 one of Step 2 (I4 at 1, -3; I2 at -2, -4, 0, 2, -1; I6 at infinity; Euler 24).
"""
from sympy import symbols, expand, factorint, Poly, roots, Rational, factor
k, t = symbols('k t')
e1 = (k-1)**2*(k+2)*(k+4); e2 = k*(k-2)*(k+3)**2
places = []                                           # (k0, pair difference, third-root data) in local parameter t
for k0, (a, b) in [(1, (e1, 0)), (-2, (e1, 0)), (-4, (e1, 0)), (0, (e2, 0)), (2, (e2, 0)), (-3, (e2, 0)), (-1, (e1, e2))]:
    other = e2 if (a, b) == (e1, 0) else (e1 if (a, b) == (e2, 0) else 0)
    places.append((k0, expand((a - b).subs(k, k0 + t)), expand(((a if b == 0 else a) - other).subs(k, k0 + t))))
E1i, E2i = expand(t**4*e1.subs(k, 1/t)), expand(t**4*e2.subs(k, 1/t))   # weight-4 model at infinity, t = 1/k
places.append(('inf', expand(E1i - E2i), expand(E1i - 0)))
conf, bad = {}, set()
for k0, diff, sep in places:
    P = Poly(diff, t); m = min(mon[0] for mon in P.monoms()); g0 = P.coeff_monomial(t**m); u0 = sep.subs(t, 0)
    conf[k0] = 2*m; pr = set(factorint(abs(g0))) | set(factorint(abs(u0))) | {2}
    bad |= pr; print('k0=%s: I_%d, g(0)=%s, u(0)=%s, primes %s' % (k0, 2*m, g0, u0, sorted(pr)))
dist = [1, -2, -4, 0, 2, -3, -1]
for i in range(len(dist)):
    for j in range(i):
        bad |= set(factorint(abs(dist[i] - dist[j])))
bad |= set(factorint(1))                               # leading coefficients of e1, e2 are 1 (places stay finite)
ctl = conf == {1: 4, -3: 4, -2: 2, -4: 2, 0: 2, 2: 2, -1: 2, 'inf': 6} and sum(conf.values()) == 24
print('CONTROL (char-0 configuration of Step 2, Euler 24):', 'PASS' if ctl else 'FAIL')
print('primes where some local constant or place collision fails:', sorted(bad), '-> good reduction for p >= 7' if max(bad) <= 5 else '')
