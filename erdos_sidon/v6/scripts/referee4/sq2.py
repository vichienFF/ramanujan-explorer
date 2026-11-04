import sympy as sp
y0,w=sp.symbols('y0 w')
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
A=3*y0**2-3*y0+1
r=y0*(-(y0**2-3*y0+1)+(y0-1)*w)/A
t0=y0/(1-y0); tr=r/(1-r)
J=sp.together(-D4(t0+tr,t0*tr))
num=sp.expand(sp.numer(J)); den=sp.denom(J)
W2=-2*(y0**2-y0+1)
# reduce num mod w^2 - W2
P=sp.Poly(num,w); rem=sp.rem(P,sp.Poly(w**2-W2,w)); 
Rr=rem.as_expr()
print('den factor',sp.factor(den))
a=sp.factor(rem.coeff_monomial(1)); b=sp.factor(rem.coeff_monomial(w))
print('a=',a); print('b=',b)
Q1=3*y0**4-6*y0**3+6*y0**2-3*y0+2; Q2=3*y0**4-6*y0**3+9*y0**2-6*y0+1
ap=sp.expand(a/(4*y0**2*(y0-1)**2)); bp=sp.expand(b/(4*y0**2*(y0-1)**2))
for al,be in (((2*y0-1)*Q1,Q2),((2*y0-1)*Q2,Q1)):
    print(sp.expand(al**2+be**2*W2-ap)==0, sp.expand(2*al*be-bp)==0)
