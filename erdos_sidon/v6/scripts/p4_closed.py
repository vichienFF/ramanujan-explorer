r"""P4 step 5b: fast exact correction sums + closed-form checks.  # LOCAL-OK: seconds
Hand facts used (derived 2026-11-02): degenerate members are d = -c (q-1 cubics). Repeated-root genuine members are exactly
  (c,d) = (y0^-3, (1-y0)^-3) for y0 in F_q \ {0,1} with c+d != 0 (double root at y0), plus (-1,-1) = -2(y^2-y+1)^2
  (the only member that is a constant times a square; it coincides with y0^3 = -1 members when phi(-3) = 1).
Here repeated-root members are detected exactly by gcd(f, f') != 1 over F_q (independent of the hand list), and the hand list is checked against it.
CONTROL: values equal p4_corr.py (sympy factor_list) output at q = 5..43 (REF below), and the total N1..N3 equal p4_n3.py closed forms."""
import sys
from sympy import Poly, symbols, gcd
y = symbols('y')
def leg(a, q): return 0 if a % q == 0 else (1 if pow(a % q, (q - 1) // 2, q) == 1 else -1)
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
def ff(k): return [0, k, k * (k - 1), k * (k - 1) * (k - 2)]
def corr(q):
    P4 = [pow(v, 4, q) for v in range(q)]; Q4 = [pow((1 - v) % q, 4, q) for v in range(q)]
    deg = [0] * 4; rep = [0] * 4; D3 = 0; reps = set()
    for c in range(1, q):                       # degenerate: d = -c, f = c(y^4-(1-y)^4) - 1, cubic
        k = sum(1 for v in range(q) if (c * (P4[v] - Q4[v]) - 1) % q == 0)
        for j in (1, 2, 3): deg[j] += ff(k)[j]
        P = Poly(c * y**4 - c * (1 - y)**4 - 1, y, modulus=q)
        D3 += any(f.degree() == 3 for f, e in P.factor_list()[1])
    for c in range(1, q):
        for d in range(1, q):
            if (c + d) % q == 0: continue
            P = Poly(c * y**4 + d * (1 - y)**4 - 1, y, modulus=q)
            if gcd(P, P.diff(y)).degree() > 0:
                reps.add((c, d)); k = sum(1 for v in range(q) if (c * P4[v] + d * Q4[v] - 1) % q == 0)
                for j in (1, 2, 3): rep[j] += ff(k)[j]
    hand = {(pow(y0, 3 * (q - 2), q), pow((1 - y0) % q, 3 * (q - 2), q)) for y0 in range(2, q)} | {(q - 1, q - 1)}
    hand = {m for m in hand if sum(m) % q}
    return deg, rep, D3, reps == hand, len(reps)
REF = {5: ([2, 0, 0], 2, 4, [9, 18, 18]), 13: ([10, 4, 0], 4, 8, [17, 26, 24]), 23: ([22, 24, 24], 8, 22, [45, 72, 72]), 43: ([42, 40, 36], 14, 38, [71, 98, 96])}
ok = all((lambda r: (r[0][1:], r[2], r[4], r[1][1:]) == v)(corr(q)) for q, v in REF.items())
print('CONTROL vs p4_corr.py (sympy factor_list) at q=5,13,23,43:', 'PASS' if ok else 'FAIL', flush=True)
if not ok: sys.exit(1)
QS = [int(a) for a in sys.argv[1:]] or [p for p in range(5, 110) if all(p % t for t in range(2, int(p ** .5) + 1))]
allok = True
for q in QS:
    deg, rep, D3, handok, nrep = corr(q); f1, f2, f3 = leg(-1, q), leg(-2, q), leg(-3, q)
    pred = {'degN1': q - 2 - f1, 'degN2': q - 4 - 3 * f1 - 2 * f3, 'degN3': q - 6 - 3 * f1 - 4 * f3, 'D3': (q - f3) // 3,
            'nrep': q - 3 - 2 * f3, 'repN1': 2 * q - 8 - 3 * f2 - 4 * f3,
            'repN3': 3 * (q - 5 - 3 * f2 - 3 * f3), 'repN2': 3 * (q - 5 - 3 * f2 - 3 * f3) + 1 + f3}
    got = {'degN1': deg[1], 'degN2': deg[2], 'degN3': deg[3], 'D3': D3, 'nrep': nrep, 'repN1': rep[1], 'repN2': rep[2], 'repN3': rep[3]}
    bad = [k for k in pred if pred[k] != got[k]]; allok &= not bad and handok
    print('q=%d (f-1 %+d f-2 %+d f-3 %+d) hand-list %s | closed forms %s | repN2 %d repN3 %d' % (
        q, f1, f2, f3, 'OK' if handok else 'NO', 'ALL EXACT' if not bad else 'FAIL ' + str(bad), rep[2], rep[3]), flush=True)
print('SUMMARY: all closed forms + hand list exact on %d primes: %s' % (len(QS), allok))
# Symbolic assembly: T = (N1-deg1-rep1) - (N2-deg2-rep2) + (N3-deg3-rep3)/3 + D3 must equal ((q-2)(q+1)+b)/3 identically in q, b
# for all 8 sign classes (f1,f2,f3); N1..N3 are the p4_n3.py closed forms.
from sympy import symbols as S, simplify, Rational
Q, B = S('q b')
for F1 in (1, -1):
    for F2 in (1, -1):
        for F3 in (1, -1):
            N1 = (Q - 2)**2 + 2 * (Q - 1); N2 = Q**2 - 4 * Q + 10 + 5 * F1; N3 = Q**2 - 7 * Q + 19 + 18 * F1 + 9 * F2 + 6 * (1 + F3) + B
            d1, d2, d3 = Q - 2 - F1, Q - 4 - 3 * F1 - 2 * F3, Q - 6 - 3 * F1 - 4 * F3
            r3 = 3 * (Q - 5 - 3 * F2 - 3 * F3); r1, r2 = 2 * Q - 8 - 3 * F2 - 4 * F3, r3 + 1 + F3
            T = (N1 - d1 - r1) - (N2 - d2 - r2) + Rational(1, 3) * (N3 - d3 - r3) + Rational(1, 3) * (Q - F3)
            print('class f-1 %+d f-2 %+d f-3 %+d: T - target =' % (F1, F2, F3), simplify(T - ((Q - 2) * (Q + 1) + B) / 3))
