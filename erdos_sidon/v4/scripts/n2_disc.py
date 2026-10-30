r"""Symbolic form of the obstruction in n2_pairs.py: disc(y1,y2) = s^2 - 4p of the residual quadratic, with (c,d) from the 2x2 system.  # LOCAL-OK: seconds
Question: after removing square factors, is the branch curve a union of lines (double cover of P^2 branched on 6 lines -> known modular K3s)?
CONTROL: at a random admissible pair over Q the symbolic disc must equal the numeric one from the explicit quartic factorisation."""
from sympy import symbols, Matrix, factor, together, fraction, factor_list, Rational, Poly, sqf_part
y1, y2, y = symbols('y1 y2 y')
A = Matrix([[(1 - y1)**2, y1**2], [(1 - y2)**2, y2**2]]); r = Matrix([y1**2*(1 - y1)**2, y2**2*(1 - y2)**2])
c, d = A.LUsolve(r)
s = 2 - y1 - y2; p = -c / (y1*y2)
D = factor(together(s**2 - 4*p))
num, den = fraction(D)
print('disc =', D)
print('numerator factors:', factor_list(num))
print('denominator factors:', factor_list(den))
# CONTROL
v1, v2 = Rational(3), Rational(-5)
cv, dv = [x.subs({y1: v1, y2: v2}) for x in (c, d)]
quart = Poly(y**4 - 2*y**3 + (1 - cv - dv)*y**2 + 2*cv*y - cv, y)
quo = quart.div(Poly((y - v1)*(y - v2), y))
assert quo[1].is_zero, 'CONTROL FAIL: pair not roots'
qa, qb, qc = quo[0].all_coeffs()
print('CONTROL symbolic vs numeric disc:', 'PASS' if (qb**2 - 4*qa*qc) == D.subs({y1: v1, y2: v2}) else 'FAIL')
