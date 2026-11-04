# Char-3 lead (Step 4zn), exploratory: N1,N2,N3 = sum_{c,d in F*} (r)_k for q = 3^n, to see whether they are simple in q and (-1)^n.  # LOCAL-OK: O(q^2), q<=243 est. < 5 min
# CONTROL: same code reproduces the prime-field values N1,N2,N3 = 37,26,6 at q=7 (p4_n3.py REF).
from sage.all import GF
from collections import Counter
def Ns(q):
    F = GF(q, 'a'); N = [0, 0, 0, 0]
    for c in F:
        if c == 0: continue
        cnt = Counter((1 - c*y**4) / (1-y)**4 for y in F if y != 1)
        for d in F:
            if d == 0: continue
            r = cnt.get(d, 0) + (1 if c == 1 else 0)
            for k in (1, 2, 3):
                v = 1
                for i in range(k): v *= (r - i)
                N[k] += v
    return N[1:]
print('CONTROL q=7:', 'PASS' if Ns(7) == [37, 26, 6] else 'FAIL', flush=True)
import sys
for n in ([int(a) for a in sys.argv[1:]] or (1, 2, 3, 4, 5)):
    q = 3**n; N1, N2, N3 = Ns(q); print('q=%d N1=%d N2=%d N3=%d | N1-(q-2)^2-2(q-1)=%d' % (q, N1, N2, N3, N1 - (q-2)**2 - 2*(q-1)), flush=True)
