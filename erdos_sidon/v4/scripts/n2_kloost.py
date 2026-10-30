r"""N(-2) via F_{q^3}: alpha's min poly is in the l=-2 cubic family  <=>  (Tr a - 2)(Tr a^-1 - 2) = 1  (hand derivation 2026-10-30).  # LOCAL-OK: seconds
So I = (M - 1)/3, M = #{a in F_{q^3}^*: (Tr a-2)(Tr a^-1-2)=1} (a=1 is the only F-solution). Character sums give
q^2 M = (q^3-1)(q-1) - 2 + Main,  Main = sum_{m!=0} Kl(4m) Kl(m)^2 (Kl(m)^2 - 3q)  (Hasse-Davenport Kl_3 = Kl^3 - 3q Kl).
Claim to test: N(-2) = (q-2)(q+1)/3  <=>  Main = -q^2 + q + 1.
CONTROL: (a) brute-force M over F_{q^3} (q=5,11) must give 3*N(-2)+1 with N(-2) = 6, 36 from n1_cubic.py; (b) Main from the formula must equal q^2 M - (q^3-1)(q-1) + 2."""
import sys, cmath
def kl(q, a):
    return sum(cmath.exp(2j * cmath.pi * ((x + a * pow(x, -1, q)) % q) / q) for x in range(1, q)).real
def brute_M(q):  # F_{q^3} = F_q[t]/(irreducible cubic t^3 - t - k)
    k = next(k for k in range(1, q) if all((x**3 - x - k) % q for x in range(q)))
    def mul(u, v):
        p = [0] * 5
        for i in range(3):
            for j in range(3): p[i + j] += u[i] * v[j]
        for i in (4, 3): p[i - 2] += p[i]; p[i - 3] += k * p[i]; p[i] = 0  # t^3 = t + k
        return [x % q for x in p[:3]]
    def tr(u):  # Tr(1)=3, Tr(t)=0, Tr(t^2)=2 (e1=0, e2=-1)
        return (3 * u[0] + 2 * u[2]) % q
    els = [[a, b, c] for a in range(q) for b in range(q) for c in range(q) if (a, b, c) != (0, 0, 0)]
    one = [1, 0, 0]; inv = {}
    for u in els:
        if tuple(u) in inv: continue
        for v in els:
            if mul(u, v) == one: inv[tuple(u)] = v; inv[tuple(v)] = u; break
    return sum(((tr(u) - 2) * (tr(inv[tuple(u)]) - 2) - 1) % q == 0 for u in els)
for q in map(int, sys.argv[1:]):
    K = {m: kl(q, m) for m in range(1, q)}
    main = sum(K[4 * m % q] * K[m]**2 * (K[m]**2 - 3 * q) for m in range(1, q))
    Mform = ((q**3 - 1) * (q - 1) - 2 + main) / q**2
    line = 'q=%d (q mod 3 = %d) Main %.4f target %d ; M(formula) %.4f -> N %.4f (pred %d)' % (q, q % 3, main, -q*q + q + 1, Mform, (Mform - 1) / 3, (q-2)*(q+1)//3)
    if q in (5, 11):
        Mb = brute_M(q); ref = {5: 6, 11: 36}[q]
        line += ' | CONTROL brute M %d: %s' % (Mb, 'PASS' if Mb == 3 * ref + 1 and abs(Mform - Mb) < 1e-6 else 'FAIL')
    print(line)
