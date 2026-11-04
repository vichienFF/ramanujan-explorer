r"""Step 5, class c + d = 0 written out in full (2026-11-04): closed form of SPEC_cd0(q).  # LOCAL-OK: < 1 min
Hand derivation (P4_SPECIAL_LEMMA.md, 'Class c + d = 0 in full'): members (c, -c), c != 0, 1. With s = 2y - 1: c[y^4 - (1-y)^4] = 1 <-> s^3 + s = 2e, e = 1/c
(e != 0, 1); y = 1 <-> s = 1 is never a root. Ordered pairs of distinct roots <-> sigma = s1+s2 with pi = s1 s2 = sigma^2 + 1 (conic s1^2+s1s2+s2^2 = -1),
number 1 + chi(Delta), Delta = sigma^2 - 4 pi = -(3 sigma^2 + 4) (0 pairs if Delta = 0). Third root s3 = -sigma; e = -sigma(sigma^2+1)/2;
e != 0 <-> sigma(sigma^2+1) != 0; e != 1 <-> (sigma+1)(sigma^2-sigma+2) != 0; s3 in {s1, s2} <-> 3 sigma^2 + 1 = 0.
In t = y/(1-y) = (s+1)/(1-s): -D4 = [4 sigma (sigma-2)(sigma+2) / (sigma^2-sigma+2)^2]^2 on the conic; singular (t1^4 = t2^4) <-> sigma^2 (sigma^2-4)(sigma^2+1) = 0.
=> SPEC_cd0 = sum_{sigma: E != 0} (1 + chi(Delta)) * N (I - 2),  E = sigma(sigma^2+1)(sigma+1)(sigma^2-sigma+2)(3sigma^2+4), N = [sigma^2 != 4], I = [3sigma^2+1 != 0]
=> closed form  -(q - chi(-3)) + sum_{Z_E} w + sum_{sigma = +-2, not in Z_E} w - sum_{Z_I \ (Z_E u {+-2})} w,  w(sigma) = 1 + chi(Delta(sigma)).
CONTROL: referee brute force referee4/perclass.py pieces(q)['c+d=0'] at every prime 7 <= q < 400.
"""
import sys, sympy as sp
from sympy.polys.polyfuncs import symmetrize
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
exec(open('referee4/perclass.py', encoding='utf-8').read().split("if __name__=='__main__':")[0])   # pieces(q), D4(u, v)
s1, s2, S, P = sp.symbols('s1 s2 S P')
def on_conic(e):                    # symmetric polynomial in s1, s2 -> polynomial in sigma with pi = sigma^2 + 1
    sym, rem, defs = symmetrize(sp.expand(e), [s1, s2], formal=True); assert rem == 0
    return sp.expand(sym.subs({defs[0][0]: S, defs[1][0]: P}).subs(P, S**2 + 1))
t = lambda s: (s + 1)/(1 - s)
u = sp.together(t(s1) + t(s2)); v = sp.together(t(s1)*t(s2))
nD, dD = sp.fraction(sp.factor(-D4(u, v)))
nS, dS = sp.fraction(sp.factor(u*(u**2 - 2*v)))
sym = {
 'conic': sp.expand(sp.cancel(((s1**3+s1) - (s2**3+s2))/(s1 - s2)) - (s1**2+s1*s2+s2**2+1)) == 0,
 'y-equation': sp.expand(((S+1)/2)**4 - ((1-S)/2)**4 - (S**3+S)/2) == 0,
 '-D4 on conic': sp.expand(on_conic(nD) * (S**2-S+2)**4 - on_conic(sp.expand(dD)) * (4*S*(S-2)*(S+2))**2) == 0,
 'singular on conic': sp.factor(on_conic(nS)) == sp.factor(-4*S**2*(S-2)*(S+2)*(S**2+1)),
 'e(sigma)': sp.expand(on_conic(s1*s2*(-(s1+s2))) - 2*(-S*(S**2+1)/2)) == 0,
 'e=1 factor': sp.expand(-S*(S**2+1) - 2 + (S+1)*(S**2-S+2)) == 0,
 's3 in {s1,s2}': sp.expand(S**2 + S*S + (S**2+1) - (3*S**2+1)) == 0,
}
print('SYM identities:', sym, '->', 'PASS' if all(sym.values()) else 'FAIL')
def chi(x, q):
    x %= q
    return 0 if x == 0 else (1 if pow(x, (q-1)//2, q) == 1 else -1)
def roots(coeffs, q): return {x for x in range(q) if sum(c*pow(x, i, q) for i, c in enumerate(coeffs)) % q == 0}
w = lambda x, q: 1 + chi(-(3*x*x+4), q)
def spec_sum(q):
    s = 0
    for x in range(q):
        E = x*(x*x+1)*(x+1)*(x*x-x+2)*(3*x*x+4) % q
        if E == 0: continue
        N = (x*x - 4) % q != 0; I = (3*x*x+1) % q != 0
        s += w(x, q) * N * (I - 2)
    return s
def spec_closed(q):
    ZE = roots([0, 1], q) | roots([1, 0, 1], q) | roots([1, 1], q) | roots([2, -1, 1], q) | roots([4, 0, 3], q)
    ZI = roots([1, 0, 3], q); PM2 = {2 % q, (-2) % q}
    return -(q - chi(-3, q)) + sum(w(x, q) for x in ZE) + sum(w(x, q) for x in PM2 - ZE) - sum(w(x, q) for x in ZI - ZE - PM2)
Pr = [p for p in range(7, 400) if sp.isprime(p)]
rows = [(q, pieces(q)['c+d=0'], spec_sum(q), spec_closed(q)) for q in Pr]
bad = [r for r in rows if not (r[1] == r[2] == r[3])]
print('CONTROL vs referee brute force (perclass.pieces) at %d primes 7..%d: %s' % (len(Pr), Pr[-1], 'PASS' if not bad else 'FAIL %s' % bad[:5]))
print('examples (q, brute, per-sigma, closed):', rows[:4])
