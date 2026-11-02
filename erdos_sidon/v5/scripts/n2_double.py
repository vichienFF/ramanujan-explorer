r"""Double-root types E=(1)^2(2), C=(1)(1)(1)^2 (2026-10-30).  # LOCAL-OK: seconds
Hand: a double root a fixes (c,d) by Q(a)=Q'(a)=0 (linear in c,d); then Q=(y-a)^2 R_a(y). E counts a with R_a irreducible, C counts a with
R_a split with roots != a. So E, C are 1-variable character sums of disc(R_a) -> closed forms.
CONTROL: E, C from this parametrisation must equal the census values of n2_types at q=7,11,13 (E=3,6,6 ; C=0,3,3)."""
from sympy import symbols, solve, factor, Poly, div, discriminant, together, fraction
a, y, c, d = symbols('a y c d')
Q = y**4 - 2*y**3 + (1 - c - d)*y**2 + 2*c*y - c
sol = solve([Q.subs(y, a), Q.diff(y).subs(y, a)], [c, d], dict=True)[0]
print('c(a) =', factor(sol[c]), '   d(a) =', factor(sol[d]))
Qa = Poly(Q.subs(sol), y)
R, rem = div(Qa, Poly((y - a)**2, y))
print('remainder zero:', rem.is_zero, '  R_a =', R.as_expr())
D = factor(together(discriminant(R.as_expr(), y)))
print('disc(R_a) =', D, '   R_a(a) =', factor(R.as_expr().subs(y, a)))
def counts(q):
    E = C = 0
    for av in range(2, q):
        cv, dv = [int(x.subs(a, av) % q) if x.subs(a, av).is_Integer else None for x in (sol[c], sol[d])]
        num_c, den_c = fraction(together(sol[c])); num_d, den_d = fraction(together(sol[d]))
        if int(den_c.subs(a, av)) % q == 0 or int(den_d.subs(a, av)) % q == 0: continue
        cv = int(num_c.subs(a, av)) * pow(int(den_c.subs(a, av)), -1, q) % q; dv = int(num_d.subs(a, av)) * pow(int(den_d.subs(a, av)), -1, q) % q
        if cv == 0 or dv == 0: continue
        Rq = Poly(y**4 - 2*y**3 + (1 - cv - dv)*y**2 + 2*cv*y - cv, y, modulus=q)
        fl = sorted((g.degree(), e) for g, e in Rq.factor_list()[1])
        if fl == [(1, 2), (2, 1)]: E += 1
        if fl == [(1, 1), (1, 1), (1, 2)]: C += 1
    return E, C
res = {q: counts(q) for q in (7, 11, 13)}
print('CONTROL', 'PASS' if res == {7: (3, 0), 11: (6, 3), 13: (6, 3)} else 'FAIL', res)
