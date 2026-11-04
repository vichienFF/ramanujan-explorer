r"""P4 step 5: corrections. T = #(c,d) with an irreducible cubic factor = n1 + D3, where n1 = N1g - N2g + N3g/3 over genuine simple members and
D3 = #degenerate members (d = -c) that are irreducible cubics. Ng = N - (degenerate contribution) - (repeated-root contribution).  # LOCAL-OK: seconds
Prints each correction so closed forms can be read off; checks the assembled identity T = (N1-N2+N3/3) - corr + D3 exactly.
CONTROL: T equals the target ((q-2)(q+1)+b_q)/3 (observed) and N1..N3 equal p4_n3 values."""
import sys
from sympy import Poly, symbols
y = symbols('y')
def bq(q):
    if q % 3 == 2: return 0
    x = next(x for x in range(1, q) if any(x * x + 3 * t * t == q for t in range(1, q))); return 4 * x * x - 2 * q
def leg(a, q): return 0 if a % q == 0 else (1 if pow(a % q, (q - 1) // 2, q) == 1 else -1)
for q in map(int, sys.argv[1:] or [5, 7, 11, 13, 17, 19, 23, 29, 31]):
    tot = [0, 0, 0, 0]; deg = [0, 0, 0, 0]; rep = [0, 0, 0, 0]; T = 0; D3 = 0; nrep = 0
    for c in range(1, q):
        for d in range(1, q):
            P = Poly(c * y**4 + d * (1 - y)**4 - 1, y, modulus=q); fl = P.factor_list()[1]
            k = sum(1 for v in range(q) if P.eval(v) % q == 0); kk = [0, k, k * (k - 1), k * (k - 1) * (k - 2)]
            for j in (1, 2, 3): tot[j] += kk[j]
            cub = any(f.degree() == 3 for f, e in fl); T += cub
            if (c + d) % q == 0:
                for j in (1, 2, 3): deg[j] += kk[j]
                D3 += cub
            elif any(e > 1 for f, e in fl):
                nrep += 1
                for j in (1, 2, 3): rep[j] += kk[j]
    g = [tot[j] - deg[j] - rep[j] for j in range(4)]
    asm = g[1] - g[2] + g[3] // 3 + D3
    target = ((q - 2) * (q + 1) + bq(q)) // 3
    print('q=%d (phi-1 %+d, phi-2 %+d, phi-3 %+d) | assembled %d target %d %s | deg N1..3 %s D3 %d | rep members %d rep N1..3 %s' % (
        q, leg(-1, q), leg(-2, q), leg(-3, q), asm, target, 'MATCH' if asm == target == T else 'NO', deg[1:], D3, nrep, rep[1:]), flush=True)
