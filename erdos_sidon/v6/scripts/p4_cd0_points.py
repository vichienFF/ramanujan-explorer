# Exceptional points on the 6 c=0 / d=0 lines (sympy over Q(i)); used for the hand count of the c/d=0 category.  # LOCAL-OK: seconds
# NO-CONTROL: symbolic enumeration; the resulting count -2(6q-24) is checked against p4_n3_assembly category values (H-N3CAT PASS).
import sympy as sp
t,u,v=sp.symbols('t u v'); I=sp.I
D4=7*u**4+12*u**3*v+12*u**3+12*u**2*v**2-4*u**2*v+12*u**2-16*v**3+32*v**2-16*v
def roots(expr):
    num=sp.numer(sp.together(expr)); P=sp.Poly(sp.expand(num),t,extension=I)
    return set(sp.nsimplify(r) for r in sp.roots(P,multiple=True)) if P.degree()>0 else set()
tot2P_Z=0
for kind in ('c=0','d=0'):
  for z in (-1,I,-I):
    t2 = z*(1+t)-1 if kind=='c=0' else 1/(z*(1+t)/t-1)
    bad=set()
    bad|={sp.Integer(-1)}; bad|=roots(t2+1)                  # t1=-1, t2=-1
    if kind=='d=0': bad|={sp.Integer(0)}; bad|=roots(1/t2)   # t1=0, t2 undefined (pole)
    bad|=roots(t**4-t2**4)                       # singular t1^4=t2^4 (incl. t1=t2)
    zeros=roots(-D4.subs({u:t+t2,v:t*t2})) - bad # main=1 points (D4=0)
    bad={b for b in bad if b.is_finite}
    print(kind,'z=',z,'| excluded t1:',len(bad),sorted(map(str,bad)),'| zeros:',len(zeros),sorted(map(str,zeros)))
