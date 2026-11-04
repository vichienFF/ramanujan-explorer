r"""P4 N3 route: residual quadratic of F(t) = (1+t)^4 - c t^4 - d given two roots t1,t2 (u=t1+t2, v=t1 t2).  # LOCAL-OK: seconds
CONTROL: product (t^2-u t+v)(residual) * lead reproduces F identically (sympy expand == 0)."""
from sympy import symbols, solve, expand, factor, Poly, div, discriminant, together, numer, denom, simplify
t, t1, t2, c, d, u, v = symbols('t t1 t2 c d u v')
F = (1 + t)**4 - c * t**4 - d
sol = solve([F.subs(t, t1), F.subs(t, t2)], [c, d], dict=True)[0]
cs, ds = factor(sol[c]), factor(sol[d]); print('c =', cs); print('d =', ds)
Fp = expand(F.subs({c: cs, d: ds})); Fp = together(Fp)
qq, r = div(Poly(numer(Fp), t), Poly(expand((t - t1) * (t - t2)), t))
print('remainder zero:', r.is_zero)
R = qq.as_expr() / denom(Fp)
D = factor(discriminant(Poly(qq.as_expr(), t)))
print('disc(residual numerator) =', D)
# symmetric-function form
from sympy import symbols as S
Ds = factor(simplify(D))
print('CONTROL product check:', simplify(expand(R * (t - t1) * (t - t2)) - Fp) == 0)
