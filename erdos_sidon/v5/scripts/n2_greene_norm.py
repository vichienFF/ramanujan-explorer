r"""Normalisation check (2026-10-30): Greene's 3F2(phi,phi,phi; eps,eps | x) := q/(q-1) * sum_chi (phi*chi over chi)^3 chi(x),
binomial (A over B) := B(-1)/q * J(A, conj B), J(A,B) = sum_y A(y) B(1-y)  [definition quoted from Barman-Kalita arXiv:1208.0495].  # LOCAL-OK: seconds
Claims tested: (i) q^2 * 3F2(4) = phi(-1) * G(4), G(4) = sum_{x,y} phi(x y (1-x)(1-y)(x-4y)) (n2_greene);
(ii) Barman-Kalita Thm 1.7 with S=phi, q==2 mod 3: 3F2(4) = -phi(-3)phi(16)/q = 1/q.
CONTROL: the code's Jacobi sum must satisfy |J(chi,psi)|^2 = q for chi, psi, chi*psi nontrivial (classical), checked on random pairs."""
import sys, cmath, random
def chars(q):
    g = next(g for g in range(2, q) if all(pow(g, (q - 1) // p, q) != 1 for p in {f for f in range(2, q) if (q - 1) % f == 0 and all(f % e for e in range(2, f))}))
    log = {pow(g, j, q): j for j in range(q - 1)}
    return lambda k, x: 0 if x % q == 0 else cmath.exp(2j * cmath.pi * k * log[x % q] / (q - 1)), log
def run(q):
    ch, log = chars(q); n = q - 1; h = n // 2  # phi = ch(h, .)
    J = lambda A, B: sum(ch(A, y) * ch(B, 1 - y) for y in range(q))
    binom = lambda A, B: ch(B, -1) / q * J(A, (-B) % n)
    rnd = random.Random(q); ok = True
    for _ in range(5):
        a, b_ = rnd.randrange(1, n), rnd.randrange(1, n)
        if (a + b_) % n: ok &= abs(abs(J(a, b_))**2 - q) < 1e-6
    F = q / n * sum(binom((h + k) % n, k)**3 * ch(k, 4) for k in range(n))
    phi = lambda x: ch(h, x).real
    G = sum(phi(x*y*(1-x)*(1-y)*(x-4*y)) for x in range(q) for y in range(q))
    return ok, F, G, phi(-1)
for q in map(int, sys.argv[1:]):
    ok, F, G, m1 = run(q)
    print('q=%d CONTROL |J|^2=q %s | q^2*3F2(4) = %.4f%+.4fi | phi(-1)*G(4) = %d | (i) %s | (ii) q==2 mod 3: 3F2(4)*q = %.4f (BK: 1) %s' % (
        q, 'PASS' if ok else 'FAIL', (q*q*F).real, (q*q*F).imag, m1*G, 'MATCH' if abs(q*q*F - m1*G) < 1e-6 else 'NO', (F*q).real, ('MATCH' if abs(F*q - 1) < 1e-6 else 'NO') if q % 3 == 2 else '-'))
