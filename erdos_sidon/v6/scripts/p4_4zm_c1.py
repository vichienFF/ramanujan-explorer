# Step 4zm part 1 (c=1 class): exceptional t-values as roots of explicit polynomials; field L_c1 = splitting field; bad primes = primes dividing
# pairwise resultants/discriminants (where two exceptional points collide mod p).  # LOCAL-OK: seconds
# CONTROL: the known collision at p=13 (-3/2 = i) must appear: resultant(2t+3, t^2+1) has prime factor 13.
import sympy as sp
t = sp.symbols('t')
EXC = {'t=-1': t+1, 'd=0 (2t+1)': 2*t+1, 'd=0 (2t^2+2t+1)': 2*t**2+2*t+1, 't3=-1 partners (2t^2+t+1)': 2*t**2+t+1,
       'double roots g\'=0 (3t^2+3t+1)': 3*t**2+3*t+1, 'singular (t^2+1)': t**2+1, 'singular L1 (t^2+2t+2)': t**2+2*t+2,
       't3 of (i,-i): -3/2': 2*t+3, 't=0': t}
ctl = 13 in sp.factorint(abs(sp.resultant(2*t+3, t**2+1, t)))
print('CONTROL p=13 collision detected:', 'PASS' if ctl else 'FAIL')
fields = set(); bad = set()
for k, P in EXC.items():
    d = sp.discriminant(P, t) if sp.degree(P, t) > 1 else None
    if d is not None: fields.add(sp.sqrtdenest(sp.sqrt(d))); bad |= set(sp.factorint(abs(d)))
names = list(EXC)
for a in range(len(names)):
    for b in range(a+1, len(names)):
        r = sp.resultant(EXC[names[a]], EXC[names[b]], t)
        if r == 0: print('IDENTICAL/COMMON ROOT:', names[a], '&', names[b]); continue
        bad |= set(sp.factorint(abs(r)))
print('quadratic subfields from discriminants:', sorted(map(str, fields)))
print('bad primes (collisions) for c=1 exceptional set:', sorted(bad))
