r"""Step 5, class c = 1 written out in full (2026-11-04): closed form of SPEC_c1(q) = sum over members (1, d) of r(r-1)(r-2) - sing*(r-2) - M.  # LOCAL-OK: < 1 min
Hand derivation (P4_SPECIAL_LEMMA.md, section 'Class c = 1 in full'):
  members y^4 + d(1-y)^4 = 1, d != 0; y = 1 is always a root; other roots t = y/(1-y) solve g(t) = (1+t)^4 - t^4 = d, t != -1.
  ordered pairs (a, b) of distinct t with g(a) = g(b)  <->  u = a+b with v = ab = u^2 + 3u/2 + 1 and Delta(u) = u^2 - 4v = -(3u^2+6u+4) a nonzero square;
  third root t3 = -3/2 - u;  d(u) = 1 - 4 v (3/2 + u) = -(u+1)(4u^2+8u+5);  a or b = -1  <->  2u^2+5u+4 = 0;  t3 in {a, b}  <->  12u^2+24u+13 = 0;
  t3 = -1 <-> 2u+1 = 0;  singular pairs (a^4 = b^4)  <->  u(u+1)(u+2) = 0;  on the conic -D4 = (2u(u+1)(u+2))^2.
  => SPEC_c1 = sum_{u: E(u) != 0} (1+chi(Delta(u))) * (2 + N(u)(I(u) - 1)),  E = (u+1)(4u^2+8u+5)(2u^2+5u+4)(3u^2+6u+4),
     N(u) = [u(u+1)(u+2) != 0], I(u) = [(12u^2+24u+13)(2u+1) != 0]
  => closed form  2(q - chi(-3)) - 2 * sum_{u in Z_E} (1+chi(Delta(u))) - sum_{u in Z_I, u not in Z_E u {0,-2}} (1+chi(Delta(u)))  (Z = roots in F_q).
CONTROL: SPEC_c1 from the referee's independent brute-force code (referee4/perclass.py, pieces(q)['c=1']) at every prime 7 <= q < 400.
"""
import sys, sympy as sp
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
exec(open('referee4/perclass.py', encoding='utf-8').read().split("if __name__=='__main__':")[0])   # pieces(q), D4(u, v)
u, a, b = sp.symbols('u a b')
g = lambda t: sp.expand((1+t)**4 - t**4)
v = u**2 + sp.Rational(3, 2)*u + 1; t3 = -sp.Rational(3, 2) - u
sym = {
 'conic': sp.simplify(sp.factor(g(a) - g(b)) / (a - b) - (4*((a+b)**2 - a*b) + 6*(a+b) + 4)) == 0,
 'Viete t3': sp.expand(sp.Poly(4*sp.Symbol('z')**3 + 6*sp.Symbol('z')**2, sp.Symbol('z')).coeffs()[1] / -4 - (-sp.Rational(3, 2))) == 0,
 'd(u)': sp.expand(1 - 4*v*(sp.Rational(3, 2) + u) + (u+1)*(4*u**2+8*u+5)) == 0,
 'd(u) = g(root)': sp.expand(g(t3) - (1 - 4*v*(sp.Rational(3, 2) + u))) == 0,   # t3 is a root of g(t) = d
 'Delta': sp.expand(u**2 - 4*v + (3*u**2+6*u+4)) == 0,
 'a=-1': sp.expand(2*(1 + u + v) - (2*u**2+5*u+4)) == 0,
 't3 in {a,b}': sp.expand(4*(t3**2 - u*t3 + v) - (12*u**2+24*u+13)) == 0,
 '-D4 square': sp.expand(-D4(u, v) - (2*u*(u+1)*(u+2))**2) == 0,
 'singular a^2+b^2=0 <-> u^2=2v': sp.expand(u**2 - 2*v - (-(u+1)*(u+2))) == 0,
}
print('SYM identities:', sym, '->', 'PASS' if all(sym.values()) else 'FAIL')
def chi(x, q):
    x %= q
    return 0 if x == 0 else (1 if pow(x, (q-1)//2, q) == 1 else -1)
def roots(coeffs, q): return {x for x in range(q) if sum(c*pow(x, i, q) for i, c in enumerate(coeffs)) % q == 0}
def spec_sum(q):          # per-u expression
    s = 0
    for x in range(q):
        E = (x+1)*(4*x*x+8*x+5)*(2*x*x+5*x+4)*(3*x*x+6*x+4) % q
        if E == 0: continue
        N = (x*(x+1)*(x+2)) % q != 0; I = ((12*x*x+24*x+13)*(2*x+1)) % q != 0
        s += (1 + chi(-(3*x*x+6*x+4), q)) * (2 + N*(I - 1))
    return s
def spec_closed(q):        # closed form from root sets
    ZE = roots([1, 1], q) | roots([5, 8, 4], q) | roots([4, 5, 2], q) | roots([4, 6, 3], q)
    ZI = roots([13, 24, 12], q) | roots([1, 2], q)
    w = lambda x: 1 + chi(-(3*x*x+6*x+4), q)
    return 2*(q - chi(-3, q)) - 2*sum(w(x) for x in ZE) - sum(w(x) for x in ZI - ZE - {0, q-2})
P = [p for p in range(7, 400) if sp.isprime(p)]
ok = [(q, pieces(q)['c=1'], spec_sum(q), spec_closed(q)) for q in P]
bad = [r for r in ok if not (r[1] == r[2] == r[3])]
print('CONTROL vs referee brute force (perclass.pieces) at %d primes 7..%d: %s' % (len(P), P[-1], 'PASS' if not bad else 'FAIL %s' % bad[:5]))
print('examples (q, brute, per-u, closed):', ok[:4])
