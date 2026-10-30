r"""Step 7 (q==1 mod 3) by hand (2026-10-30): qB := J(phi chi3, chi3^2) + J(phi chi3^2, chi3) = 2 Re J(phi chi3, conj chi3).  # LOCAL-OK: seconds
Hasse-Davenport g(chi3)g(phi chi3) = conj(chi3)(4) g(chi3^2) g(phi) and g(chi3)g(chi3^2) = q give
J(phi chi3, conj chi3) = chi3(2) * conj(J(chi3,chi3)).  Classical (cubic reciprocity, 2 supplement): the associate chi3(2)*J(chi3,chi3)
has even 'b' coordinate, so 2 Re = +-2x with q = x^2 + 3y^2  =>  (qB)^2 = 4x^2 = 2q + b_q  (needed for q^2 3F2(4) = q + b_q).
CONTROL: |J(chi3,chi3)|^2 = q and J(chi3,chi3) = a + b w with a == -1, b == 0 mod 3 (Ireland-Rosen Prop. 8.3.4) checked numerically."""
import cmath, sys
from n2_eta import b as bq
for q in map(int, sys.argv[1:]):
    g = next(g for g in range(2, q) if all(pow(g, (q - 1) // p, q) != 1 for p in range(2, q) if (q - 1) % p == 0 and all(p % e for e in range(2, p))))
    lg = {pow(g, j, q): j for j in range(q - 1)}; n = q - 1; t = n // 3; h = n // 2
    ch = lambda k, x: 0 if x % q == 0 else cmath.exp(2j * cmath.pi * k * lg[x % q] / n)
    J = lambda A, B: sum(ch(A, y) * ch(B, 1 - y) for y in range(q))
    J33 = J(t, t); w = cmath.exp(2j * cmath.pi / 3)
    bb = J33.imag / w.imag; aa = J33.real - bb * w.real
    ctl = abs(abs(J33)**2 - q) < 1e-6 and round(aa) % 3 == 2 and round(bb) % 3 == 0
    lhs = J((h + t) % n, 2 * t) + J((h + 2 * t) % n, t)
    hd = ch(t, 2) * J33.conjugate()
    x = next(x for x in range(1, q) if any(x * x + 3 * y * y == q for y in range(1, q)))
    print('q=%d CONTROL J33 primary %s | qB=%.4f%+.4fi  2Re(chi3(2)conjJ33)=%.4f | HD step %s | (qB)^2=%.1f vs 4x^2=%d, 2q+b_q=%d' % (
        q, 'PASS' if ctl else 'FAIL', lhs.real, lhs.imag, 2 * hd.real, 'MATCH' if abs(lhs - 2 * hd.real) < 1e-6 else 'NO', (lhs.real)**2, 4 * x * x, 2 * q + bq(q)))
