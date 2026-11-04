import sympy as sp
s1,s2=sp.symbols('s1 s2')
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
t1=(1+s1)/(1-s1); t2=(1+s2)/(1-s2)
J=sp.together(-D4(t1+t2,t1*t2))
num=sp.expand(sp.numer(J)); den=sp.denom(J)
print('den',sp.factor(den))
conic=s1**2+s1*s2+s2**2+1
# reduce numerator mod conic wrt s2
r=sp.rem(sp.Poly(num,s2),sp.Poly(conic,s2)); r=sp.factor(r.as_expr()); print('num mod conic:',r)
# try -D4 = k * square: test ratio with candidate sqrt
