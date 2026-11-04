# HAND step check: (u,v) -> (x,z) with u=x-1, v=z+x^2/4-x/2, m=u^2-4v=1-4z gives D4 = H(x^2,m)/4 (sympy solve; unique a=-4,b=1,lam=1/4).  # LOCAL-OK: seconds
# CONTROL: evenness of D in x printed True; S_b then = sum_{x,m} chi(m H(x^2,m)) = A + B (s=x^2, weight 1+chi(s)).
import sympy as sp
u, v, x, z, s, m, a, b, lam = sp.symbols('u v x z s m a b lam')
D4 = 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
D = sp.expand(D4.subs({u: x-1, v: z + x**2/4 - x/2}))
print('D(x,z) =', sp.factor(D)); print('even in x:', sp.expand(D - D.subs(x, -x)) == 0)
Ds = sp.expand(D.subs(x**2, s)) if False else sp.expand(D).subs(x, sp.sqrt(s))
H = m**3+8*m*m-3*m*s*s+6*m*s+13*m+2*s**3+2*s*s-10*s+6
sol = sp.solve(sp.Poly(sp.expand(Ds - lam*H.subs(m, a*z+b)), s, z).coeffs(), [a, b, lam], dict=True); print(sol)
