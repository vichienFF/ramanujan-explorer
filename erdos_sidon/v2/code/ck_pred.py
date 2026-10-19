"""Batch 28 prediction: factorial-moment deficit of dilated Singer (Sidon, 3-AP-free mod m) sets in a window [0,l).
Forbidden k-tuples of window positions: (i) a 3-term AP inside some 3-subset, (ii) a nontrivial parallelogram x_i+x_j = x_k+x_l
inside some 4-subset. First-order prediction (overlaps O(1/l^2) ignored):  R_k ~ -[ C(k,3) P3(l) + C(k,4) P4(l) ],
P3 = P(ordered distinct triple contains a 3-AP), P4 = P(ordered distinct 4-tuple is a parallelogram), exact for finite l.
Asymptotically R_k ~ -[ (3/2) C(k,3) + 2 C(k,4) ] / l,  l = C q."""
from math import comb
import numpy as np
def P3(l):
    E = (l + 1) // 2; O = l // 2
    return 3 * (E * E + O * O - l) / (l * (l - 1) * (l - 2))
def P4(l):
    a = np.arange(l)
    r = np.convolve(np.ones(l), np.ones(l)).astype(np.int64)          # ordered pairs (a,b) with a+b = s, incl. a = b
    r[0::2] -= 1                                                       # remove a = b (s even)
    cnt = int((r.astype(object) ** 2).sum()) - 2 * l * (l - 1)
    return 3 * cnt / (l * (l - 1) * (l - 2) * (l - 3))
def pred(k, l):
    return -(comb(k, 3) * P3(l) + comb(k, 4) * P4(l))
if __name__ == "__main__":
    for C in (2, 4):
        q = 607; l = C * q
        print(C, [round(q * pred(k, l), 3) for k in range(3, 7)], "asym", [round(-(1.5 * comb(k, 3) + 2 * comb(k, 4)) / C, 3) for k in range(3, 7)])
