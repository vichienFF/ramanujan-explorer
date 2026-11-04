import sympy as sp
y0,w,u,v=sp.symbols('y0 w u v')
Q1=3*y0**4-6*y0**3+6*y0**2-3*y0+2; Q2=3*y0**4-6*y0**3+9*y0**2-6*y0+1
X=(2*y0-1)*Q1+Q2*w
R=sp.resultant(X,w**2+2*(y0**2-y0+1),w)
print('rep zero locus of X in y0:',sp.factor(R))
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
print('c=1 check:',sp.factor(sp.expand(-D4(u,u**2+sp.Rational(3,2)*u+1))))
