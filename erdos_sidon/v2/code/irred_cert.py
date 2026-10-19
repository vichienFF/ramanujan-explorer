# Certify absolute irreducibility of C_{a,b,c}: s^a r^b t^c = 1, (s-1)^a (r-1)^b (t-1)^c = 1, a+b+c=0,
# minus the diagonal. Eliminate r by resultant -> plane curve F(s,t); drop factors s, s-1, t, t-1, s-t.
# Certificate for each remaining Q-factor G: G mod p irreducible over F_p (same total degree) AND has a smooth F_p-point
# => G absolutely irreducible over F_p-bar => over Q-bar.
import sys, itertools
from sympy import symbols, resultant, factor_list, Poly, degree, GF, expand
from math import gcd
s, r, t = symbols('s r t')
def mono(x, e): return (x**e, 1) if e >= 0 else (1, x**(-e))
def eqs(a, b, c):
    P = [mono(s, a), mono(r, b), mono(t, c)]
    Q = [mono(s-1, a), mono(r-1, b), mono(t-1, c)]
    e1 = P[0][0]*P[1][0]*P[2][0] - P[0][1]*P[1][1]*P[2][1]
    e2 = Q[0][0]*Q[1][0]*Q[2][0] - Q[0][1]*Q[1][1]*Q[2][1]
    return expand(e1), expand(e2)
def smooth_Q_point(G, B=12):
    # Galois-degree certificate: smooth points over number fields of degrees n_i (slices s=X and t=X); gcd(n_i)=1
    # => number of geometric components k divides every n_i => k = 1 (absolutely irreducible over Q-bar).
    from math import gcd as g_
    from sympy import Rational, factor_list as fl_, Poly as P_
    P = Poly(G, s, t); Ps = P.diff(s); Pt = P.diff(t); g = 0; used = []
    slices = [(s, X) for X in (0, 1)] + [(t, X) for X in (0, 1)] + [(s, t), (s, 1 - t), (s, t / (t - 1) if False else -t)]
    for k in range(2, 40):
        X = Rational((-1)**k * (k//2), 1 + (k % 3)); slices += [(s, X), (t, X)]
    for fix, X in slices:
            var = t if fix == s else s
            h = P_(P.as_expr().subs(fix, X), var)
            if h.is_zero or h.degree() < 1: continue
            a = P_(Ps.as_expr().subs(fix, X), var); b = P_(Pt.as_expr().subs(fix, X), var)
            for f, m in fl_(h.as_expr(), var)[1]:
                f = P_(f, var)
                if m > 1 or f.degree() < 1: continue
                if f.gcd(a).degree() == 0 or f.gcd(b).degree() == 0:
                    g = g_(g, f.degree()); used.append((str(fix), str(X), f.degree()))
                    if g == 1: return used[-3:]
    return None
def certify(a, b, c):
    e1, e2 = eqs(a, b, c)
    R = resultant(e1, e2, r)
    _, fl = factor_list(R)
    out = []
    for G, m in fl:
        d = Poly(G, s, t).total_degree()
        if d <= 1: out.append(("lin", str(G), m)); continue
        from gen_cert import cert as gcert
        sp = gcert(G)
        from sympy import subresultants, rem
        if abs(b) == 1: bir = 'birational (r rational, |b|=1)'
        else:
            S1 = [q for q in subresultants(Poly(e1, r), Poly(e2, r)) if q.degree() == 1]
            bir = 'birational (subres1 lc not = 0 on G)' if S1 and rem(Poly(S1[0].LC(), s, t).as_expr(), G, s, t) != 0 else 'BIRATIONALITY UNCHECKED'
        sp = (sp or 'NO CERT') + ' | ' + bir
        out.append(("deg%d" % d, sp, m))
    return out
if __name__ == "__main__":
    H = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    seen = set()
    for u in range(-H, H+1):
        for v in range(1, H+1):
            if u == 0 or u == v or gcd(abs(u), v) != 1: continue
            trip = (u-v, v, -u)
            key = min(tuple(sorted(x)) for x in (trip, tuple(-z for z in trip)))
            if key in seen: continue
            seen.add(key)
            # pick ordering with smallest |b| for elimination of r
            a_, c_, b_ = sorted(trip, key=abs, reverse=True)   # r gets the SMALLEST |exponent|
            res = certify(a_, b_, c_)
            big = [x for x in res if x[0] != "lin"]
            print(f"rho={u}/{v} exps={trip}", big, flush=True)
