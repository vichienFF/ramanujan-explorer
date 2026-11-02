r"""Assembly check of the hand inclusion-exclusion (2026-10-30).  # LOCAL-OK: seconds
Types: N=(1)(3), E=(1)^2(2), A=(1)(1)(2), B=(1)^4 split, C=(1)(1)(1)^2, D=(1)^2(1)^2. Hand identities:
 sum k = N+E+2A+2D+3C+4B = (q-2)^2 ; P = A+D+3C+6B ; S2 = -A+D+2C+6B
 => N = (q-2)^2 - E - 4P/3 + 2S2/3 - C/3 - 4D/3, and with P=(q-3)(q-5)/2, S2=(b-3q+15)/2,
    E=(q+1)/2, C=(q-5)/2, D=0 (q==2 mod 3) or E=(q-1)/2, C=(q-7)/2, D=1 (q==1 mod 3)  => N = ((q-2)(q+1)+b)/3.
CONTROL: every type count, P and S2 taken from independent brute force (n2_types census, n2_pairs) must satisfy the 3 identities."""
import sys
from fractions import Fraction as F
from n2_types import census
from n2_pairs import pairs
from n2_eta import b
for q in map(int, sys.argv[1:]):
    t = census(q); g = lambda *k: t.get(tuple(sorted(k)), 0)
    N, E, A = g((1, 1), (3, 1)), g((1, 2), (2, 1)), g((1, 1), (1, 1), (2, 1))
    B, C, D = g((1, 1), (1, 1), (1, 1), (1, 1)), g((1, 1), (1, 1), (1, 2)), g((1, 2), (1, 2))
    P, S2 = pairs(q)
    ids = (N + E + 2*A + 2*D + 3*C + 4*B == (q - 2)**2, P == A + D + 3*C + 6*B, S2 == -A + D + 2*C + 6*B)
    small = (E, C, D) == (((q + 1)//2, (q - 5)//2, 0) if q % 3 == 2 else ((q - 1)//2, (q - 7)//2, 1))
    closed = (P == (q - 3)*(q - 5)//2, 2*S2 == b(q) - 3*q + 15)
    Nf = F((q - 2)*(q + 1) + b(q), 3)
    print('q=%d CONTROL identities %s | E,C,D closed forms %s | P,S2 closed %s | N=%d formula %s -> %s' % (q, 'PASS' if all(ids) else ids, small, closed, N, Nf, 'MATCH' if N == Nf else 'MISMATCH'))
