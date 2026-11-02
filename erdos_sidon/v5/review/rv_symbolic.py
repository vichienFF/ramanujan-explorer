"""Independent symbolic checks (sympy) of Step 1/3/5 formulas in N2_PROOF.md.
CONTROL: known-answer assert that sympy factors y^2-1 as (y-1)(y+1) and that discriminant(y^2+b y+c) = b^2-4c.
"""
import sympy as sp
y, y1, y2, c, d, a = sp.symbols('y y1 y2 c d a')
assert sp.expand(sp.factor(y**2-1) - (y-1)*(y+1)) == 0
b_, c_ = sp.symbols('b_ c_')
assert sp.expand(sp.discriminant(y**2+b_*y+c_, y) - (b_**2-4*c_)) == 0

Q = y**2*(1-y)**2 - c*(1-y)**2 - d*y**2
assert sp.expand(Q - (y**4 - 2*y**3 + (1-c-d)*y**2 + 2*c*y - c)) == 0
sol = sp.solve([Q.subs(y, y1), Q.subs(y, y2)], [c, d], dict=True)[0]
det = sp.Matrix([[(1-y1)**2, y1**2], [(1-y2)**2, y2**2]]).det()
assert sp.simplify(det - (y2-y1)*(y1+y2-2*y1*y2)) == 0
assert sp.simplify(sol[c] - y1**2*y2**2*(y2-y1)*(2-y1-y2)/det) == 0
assert sp.simplify(sol[d] - (1-y1)**2*(1-y2)**2*(y2**2-y1**2)/det) == 0
# residual quadratic and its discriminant
Qs = Q.subs(sol)
quo, rem = sp.div(sp.together(Qs).as_numer_denom()[0], sp.expand((y-y1)*(y-y2)), y)
assert sp.simplify(rem) == 0
num, den = sp.together(Qs).as_numer_denom()
quo = sp.simplify(quo/den)
disc = sp.discriminant(sp.Poly(sp.expand(quo*1), y)) if False else None
co = sp.Poly(sp.expand(sp.cancel(Qs / ((y-y1)*(y-y2)))), y).all_coeffs()
co = [sp.cancel(t) for t in co]
assert co[0] == 1
u, v = y1+y2, y1*y2
disc = sp.cancel(co[1]**2 - 4*co[2])
assert sp.simplify(disc - u*(u-2)*(2*v-u+2)/(2*v-u)) == 0
assert sp.simplify(co[1] + (2-u)) == 0  # s = 2-u
assert sp.simplify(co[2] + sol[c]/v) == 0  # p = -c/v
# Step 5 double root
Qa = Q.subs({c: a**3, d: -(a-1)**3})
Ra = y**2 + 2*(a-1)*y - a
assert sp.expand(Qa - (y-a)**2*Ra) == 0
assert sp.expand(sp.discriminant(Ra, y) - 4*(a**2-a+1)) == 0
assert sp.expand(Ra.subs(y, a) - 3*a*(a-1)) == 0
# double-root system determinant
M = sp.Matrix([[(1-a)**2, a**2], [(1-a), -a]])
assert sp.factor(M.det()) in (-a*(1-a), a*(a-1), sp.factor(-a*(1-a)))
# square of quadratic case
m = sp.symbols('m')
assert sp.expand((y**2-y+1)**2 - Q.subs({c: -1, d: -1})) == 0
print('rv_symbolic: ALL PASS')
