# Re-verify referee-4 claim: on the rep-class pair locus, -D4 is a SQUARE in the function field (so chi(-D4) = 1 off zeros).  # LOCAL-OK: sympy, < 2 min
# Method: member (y0^-3,(1-y0)^-3), partner y2 = root of residual quadratic Q(y); R = -D4(t0+t2, t0 t2) reduced mod Q(y2) = r0 + r1*y2.
# r0 + r1*y2 is a square in K(y0)[y2]/(Q) iff some (a0 + a1 y2)^2 == it; test: norm N(R) must be a square in Q(y0) (necessary), then solve.
# CONTROL (independent): the zero factors of the norm must be exactly the referee-4 singular points of the rep list (y0^2+1, y0^2-2y0+2, 2y0^2-2y0+1) plus y0, y0-1 - observed in the printed norm.
import sympy as sp
y, y0, y2 = sp.symbols('y y0 y2')
c, d = y0**-3, (1-y0)**-3
num = sp.Poly(sp.numer(sp.together(c*y**4 + d*(1-y)**4 - 1)), y); Q, r = sp.div(num, sp.Poly((y - y0)**2, y)); assert r.is_zero
Qy2 = sp.Poly(Q.as_expr().subs(y, y2), y2)
t = lambda Y: Y/(1-Y); u_, v_ = t(y0) + t(y2), t(y0)*t(y2)
D4 = lambda u, v: 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
R = sp.together(-D4(u_, v_)); Rn, Rd = sp.numer(R), sp.denom(R)
def red(e): return sp.rem(sp.Poly(sp.expand(e), y2), Qy2)
Nn = sp.factor(sp.resultant(sp.Poly(sp.expand(Rn), y2), Qy2, y2)); Nd = sp.factor(sp.resultant(sp.Poly(sp.expand(Rd), y2), Qy2, y2))
def is_sq(e):
    f = sp.factor_list(sp.factor(e)); return all(m % 2 == 0 for _, m in f[1]) and sp.sqrt(f[0]).is_rational
print('norm(numerator) =', Nn); print('norm(denominator) =', Nd)
print('rep: norm of -D4 is a square in Q(y0):', is_sq(Nn) and is_sq(Nd))
