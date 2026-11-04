import sympy as sp
a=sp.symbols('a'); w=sp.Rational(-1,2)+sp.sqrt(-3)/2
r3=sp.sqrt(-3)
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
y=-(a+1/a)/r3; x=a+y*w
s1,s2=sp.simplify(x),sp.simplify(y)
print('check conic',sp.simplify(s1**2+s1*s2+s2**2+1))
t1=(1+s1)/(1-s1); t2=(1+s2)/(1-s2)
u=sp.together(t1+t2); v=sp.together(t1*t2)
E=sp.factor(sp.together(-D4(u,v)),extension=[sp.sqrt(-3)])
print('-D4 =',E)
num=sp.numer(sp.together(-D4(u,v)))
P=sp.Poly(sp.expand(num),a,extension=sp.sqrt(-3))
print(sp.sqf_list(P))
