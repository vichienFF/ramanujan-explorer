r"""Hand proof of N(3) = (q-2)(q+1)/3, q == 2 mod 3 (2026-10-29), checked here.  # LOCAL-OK: seconds
(1) c y^3 + d(1-y)^3 = 1, y in K\F  <=>  y root of g = x^3 + b x^2 - b x + e, (c,d) <-> (b,e) bijective onto b not in {0,-3}, b != 3e.
(2) Family x^3 + b(x^2-x) + e (q^2 polys, e1 = e2 of roots): triple root a in {0,1} (2 polys); double root a,a,t: t=(a^2-2a)/(1-2a),
    a not in {0,1,1/2} (q-3 polys); ordered distinct roots (a,b) with a+b != 1 fix the 3rd root (a+b=1 needs a^2-a+1=0: none as -3 non-square)
    -> 6S + 2(q-3) = (q-1)^2; root-incidence q^2 = 2 + 2(q-3) + 3S + R  => S=(q^2-4q+7)/6, R=(q^2+1)/2, I=(q-2)(q+1)/3.
(3) Excluded b=0 (x^3+e), b=-3 ((x-1)^3+1+e), b=3e ((1+e)x^3 - e(x-1)^3) always have an F-root (cubing bijective) -> N(3) = I.
=> P(3) = (q-2)^2 + 3 N(3) = (q-2)(2q-1).  Test: S, R, I, and irreducibles at excluded b, by brute force."""
import sys
for q in map(int, sys.argv[1:]):
    cnt = {0: 0, 1: 0, 2: 0, 3: 0}; T = D = exc_irr = 0
    for b in range(q):
        for e in range(q):
            f = lambda x: (x**3 + b*x*x - b*x + e) % q
            rts = [x for x in range(q) if f(x) == 0]
            fp = lambda x: (3*x*x + 2*b*x - b) % q
            mult = [x for x in rts if fp(x) == 0]
            if len(rts) == 1 and mult: T += 1 if (6*rts[0] + 2*b) % q == 0 else 0; D += 0 if (6*rts[0] + 2*b) % q == 0 else 1
            elif len(rts) == 2: D += 1
            elif len(rts) == 3: cnt[3] += 1
            elif len(rts) == 1: cnt[1] += 1
            else:
                cnt[0] += 1
                if b in (0, (-3) % q) or b == 3 * e % q: exc_irr += 1
    print('q=%d triple %d (2) double %d (%d) S %d (%s) R %d (%s) I %d (%s) irreducible-at-excluded %d (0)' % (
        q, T, D, q - 3, cnt[3], (q*q-4*q+7)/6, cnt[1], (q*q+1)/2, cnt[0], (q-2)*(q+1)/3, exc_irr))
