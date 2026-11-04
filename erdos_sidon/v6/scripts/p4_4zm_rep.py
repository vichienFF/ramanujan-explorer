# Step 4zm part 3 (rep class): member with double root y0 is (c,d) = (y0^-3, (1-y0)^-3) (Step 5b HAND). Residual quadratic Q(y) = F(y)/(y-y0)^2;
# its discriminant D(y0) decides the pair locus {(y0,y2)}: genus 0 iff D = const*square*(deg<=2). Also the c+d=0 class cubic g(s)=s(s^2+1)/2 data.  # LOCAL-OK: seconds
# CONTROL: F(y0) = F'(y0) = 0 symbolically for the parametrised member (double root check).
import sympy as sp
y, y0, s = sp.symbols('y y0 s')
c, d = y0**-3, (1-y0)**-3
F = sp.together(c*y**4 + d*(1-y)**4 - 1)
ctl = sp.simplify(F.subs(y, y0)) == 0 and sp.simplify(sp.diff(F, y).subs(y, y0)) == 0
print('CONTROL double root at y0:', 'PASS' if ctl else 'FAIL')
num = sp.Poly(sp.numer(sp.together(F)), y)
q_, r_ = sp.div(num, sp.Poly((y - y0)**2, y))
print('remainder zero:', r_.is_zero)
D = sp.factor(sp.discriminant(q_.as_expr(), y)); print('residual quadratic disc D(y0) =', D)
g = s*(s**2+1)/2
print('c+d=0: g(s)-1 =', sp.factor(sp.expand(2*(g-1))), '| g\'=', sp.factor(sp.diff(g, s)))
