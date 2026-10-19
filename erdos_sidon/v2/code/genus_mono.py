"""Geometric genus of an irreducible plane curve G(s,t)=0 via Riemann-Hurwitz for the projection to s:
2g - 2 = -2D + sum over branch points (incl. s = infinity) of (D - #cycles of the local monodromy), D = deg_t G.
Monodromy computed numerically by tracking the D roots in t around a small circle about each candidate branch point
(roots of disc_t(G) and of the leading coefficient). Validation: Fermat curves s^n + t^n = 1 -> (n-1)(n-2)/2."""
import numpy as np, sympy as sp
s, t = sp.symbols('s t')
def coeff_funcs(G):
    P = sp.Poly(G, t); cs = [sp.lambdify(s, c, 'numpy') for c in P.all_coeffs()]
    return lambda z: np.array([complex(c(z)) if callable(c) else complex(c) for c in cs])
def roots_at(cf, z): return np.roots(cf(z))
def perm_around(cf, z0, r, D, steps=400):
    th = np.linspace(0, 2 * np.pi, steps + 1); start = roots_at(cf, z0 + r)
    if len(start) != D: return None
    cur = start.copy()
    for a in th[1:]:
        nxt = roots_at(cf, z0 + r * np.exp(1j * a))
        if len(nxt) != D: return None
        order = []; used = set()
        for x in cur:
            d = np.abs(nxt - x); d[list(used)] = np.inf; j = int(np.argmin(d)); used.add(j); order.append(j)
        cur = nxt[order]
    perm = [int(np.argmin(np.abs(start - y))) for y in cur]
    if len(set(perm)) != D: return None
    return perm
def cycles(perm):
    seen, c = set(), 0
    for i in range(len(perm)):
        if i in seen: continue
        c += 1; j = i
        while j not in seen: seen.add(j); j = perm[j]
    return c
def genus(G, steps=400):
    P = sp.Poly(G, t); D = P.degree(); lc = P.LC()
    disc = sp.Poly(sp.sqf_part(sp.resultant(G, sp.diff(G, t), t)), s)
    cand = set()
    for poly in (disc, sp.Poly(sp.sqf_part(sp.Poly(lc, s)), s)):
        if poly.degree() > 0:
            for z in np.roots([complex(c) for c in poly.all_coeffs()]): cand.add(complex(np.round(z, 9)))
    cand = sorted(cand, key=lambda z: (z.real, z.imag)); C = np.array(cand)
    cf = coeff_funcs(G); total = 0
    for z0 in cand:
        dmin = np.min(np.abs(C[C != z0] - z0)) if len(C) > 1 else 1.0
        r = min(0.3 * dmin, 0.1)
        p = None; k = steps
        while p is None and k <= 6400: p = perm_around(cf, z0, r, D, k); k *= 2
        if p is None: raise RuntimeError("tracking failed at %s" % z0)
        total += D - cycles(p)
    R = 2 * (max(abs(C)) if len(C) else 1) + 2
    p = None; k = steps
    while p is None and k <= 25600: p = perm_around(cf, 0, R, D, k); k *= 2
    total += D - cycles(p)              # monodromy at infinity (inverse loop: same cycle type)
    g2 = -2 * D + total
    return (g2 + 2) // 2, D, len(cand)
if __name__ == "__main__":
    for n in (3, 4, 5, 6):
        print("Fermat", n, genus(s**n + t**n - 1), "expect", (n - 1) * (n - 2) // 2, flush=True)
