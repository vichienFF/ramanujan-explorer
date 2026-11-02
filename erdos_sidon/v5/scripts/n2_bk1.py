r"""q == 1 mod 3 case of Barman-Kalita Thm 1.7 with S = phi (transcribed from ar5iv): 3F2(4) = S(-16/27) J(Sbar,Sbar)/J(S^-3,S)
* [ (S chi3 over chi3) + (S chi3^2 over chi3^2) ]^2 - phi(-3) S(16)/q ; with S = phi: J ratio = 1, S(-16/27) = phi(-3) = 1.  # LOCAL-OK: seconds
PREDICTION: q^2 * BK value = q + b_q (our numerics), i.e. q^2 [B1+B2]^2 = q + b_q + q... (checked directly).
CONTROL: binomial helper reproduces |J|^2 = q and the q==2 case value 1/q (from n2_greene_norm)."""
import cmath, sys
from n2_eta import b
def setup(q):
    g = next(g for g in range(2, q) if all(pow(g, (q - 1) // p, q) != 1 for p in range(2, q) if (q - 1) % p == 0 and all(p % e for e in range(2, p))))
    lg = {pow(g, j, q): j for j in range(q - 1)}; n = q - 1
    ch = lambda k, x: 0 if x % q == 0 else cmath.exp(2j * cmath.pi * k * lg[x % q] / n)
    J = lambda A, B: sum(ch(A, y) * ch(B, 1 - y) for y in range(q))
    binom = lambda A, B: ch(B, -1) / q * J(A, (-B) % n)
    return n, ch, J, binom
for q in map(int, sys.argv[1:]):
    n, ch, J, binom = setup(q); h = n // 2
    ok = abs(abs(J(1, 2))**2 - q) < 1e-6 if (q - 1) > 3 else True
    if q % 3 == 1:
        t = n // 3
        B = binom((h + t) % n, t) + binom((h + 2*t) % n, 2*t)
        val = B**2 - ch(h, -3).real * ch(h, 16).real / q
        print('q=%d CONTROL |J|^2 %s | q^2*BK(4) = %.4f%+.4fi | q + b_q = %d | %s' % (q, 'PASS' if ok else 'FAIL', (q*q*val).real, (q*q*val).imag, q + b(q), 'MATCH' if abs(q*q*val - (q + b(q))) < 1e-6 else 'NO'))
