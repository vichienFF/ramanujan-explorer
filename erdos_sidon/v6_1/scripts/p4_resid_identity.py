r"""Lemma 'resid' of the FFA draft (R4): for distinct roots t1, t2 of F = (1+t)^4 - c t^4 - d with (c, d) solved from F(t1) = F(t2) = 0,  # LOCAL-OK: seconds
  c = (u+2)(t1^2+2t1+t2^2+2t2+2) / (u (t1^2+t2^2)),  1 - c = -2(2t1^2+2t1t2+3t1+2t2^2+3t2+2) / (u (t1^2+t2^2)),
  R = F / ((t-t1)(t-t2)) is a polynomial in t of degree 2 with leading coefficient 1 - c, and
  disc(R) = -4 D4(u, v) / (u^2 (t1^2+t2^2)^2),   u = t1+t2, v = t1 t2.
Hence for non-singular pairs (u (t1^2+t2^2) != 0, equivalently t1^4 != t2^4 given t1 != t2) and c != 1: chi(disc R) = chi(-D4(u, v)); if moreover the member
has no repeated root (F'(t1) F'(t2) != 0), 1 + chi(-D4) is the number of further roots in F_q (residual roots distinct or conjugate).
CONTROL: numeric check at q = 13: for random admissible pairs, the number of further roots of the actual member equals 1 + chi(-D4) whenever the
residual roots are distinct (brute force over F_13)."""
import sys, random, sympy as sp
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
t, t1, t2, c, d = sp.symbols('t t1 t2 c d')
D4 = lambda u, v: 7*u**4+12*u**3*v+12*u**3+12*u**2*v**2-4*u**2*v+12*u**2-16*v**3+32*v**2-16*v
F = (1+t)**4 - c*t**4 - d
sol = sp.solve([F.subs(t, t1), F.subs(t, t2)], [c, d], dict=True)[0]
u, v = t1 + t2, t1*t2
R = sp.cancel(sp.together(sp.expand(F.subs(sol))) / ((t - t1)*(t - t2)))
num, den = sp.fraction(sp.together(R)); P = sp.Poly(num, t); a2, a1, a0 = [sp.cancel(x/den) for x in P.all_coeffs()]
checks = {
 'c': sp.simplify(sol[c] - (u+2)*(t1**2+2*t1+t2**2+2*t2+2)/(u*(t1**2+t2**2))) == 0,
 '1-c = lead(R)': sp.simplify((1 - sol[c]) - a2) == 0,
 'degree 2': P.degree() == 2,
 'disc identity': sp.simplify((a1**2 - 4*a2*a0) - (-4*D4(u, v)/(u**2*(t1**2+t2**2)**2))) == 0,
}
print('SYM:', checks, '->', 'PASS' if all(checks.values()) else 'FAIL')
q = 13; rnd = random.Random(1); ok = True; n = 0
def chi(x): x %= q; return 0 if x == 0 else (1 if pow(x, (q-1)//2, q) == 1 else -1)
for _ in range(400):
    a, b = rnd.randrange(q), rnd.randrange(q)
    if a == b or (a+1) % q == 0 or (b+1) % q == 0 or pow(a, 4, q) == pow(b, 4, q): continue
    M = [[pow(a, 4, q), 1], [pow(b, 4, q), 1]]; det = (M[0][0] - M[1][0]) % q
    if det == 0: continue
    ra, rb = pow(1+a, 4, q), pow(1+b, 4, q); inv = pow(det, q-2, q)
    cc = (ra - rb) * inv % q; dd = (ra - cc*pow(a, 4, q)) % q
    if cc in (0, 1) or dd == 0: continue
    dF = lambda x: (4*pow(1+x, 3, q) - 4*cc*pow(x, 3, q)) % q
    if dF(a) == 0 or dF(b) == 0: continue      # repeated member (a residual root equals t1 or t2): rep class, excluded by the hypothesis
    others = [x for x in range(q) if x not in (a, b) and (pow(1+x, 4, q) - cc*pow(x, 4, q) - dd) % q == 0]
    if len(others) == 1: continue              # residual double root (chi(-D4) = 0, separate case)
    n += 1; ok &= len(others) == 1 + chi(-D4(a+b, a*b))
print('CONTROL brute force at q=13 (%d pairs): %s' % (n, 'PASS' if ok and n > 20 else 'FAIL'))
