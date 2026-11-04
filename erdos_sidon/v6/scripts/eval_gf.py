"""Evaluate gf_ncount.json outputs against the registered N3 laws (formula computed here, never hand-copied).
char 3: N3 = (q-3)^2 - [n even]*4(q-9)  (H-CH3-N3);  p >= 5: (N3) of P4_FULL_PROOF.md with b_q from b_p.
CONTROL: (N3) gives the Sage/brute-force values q=7 -> 6, q=49 -> 2022, q=125 -> 14778 (gf_ncount.py docstring); char 3: q=9 -> 36.
Usage: python eval_gf.py out_dir/gf_ncount.json [...]
"""
import sys, json
def chi(a, p, n):                      # quadratic character of a (in F_p) over F_{p^n}
    a %= p; l = pow(a, (p - 1) // 2, p); l = -1 if l == p - 1 else l
    return l if n % 2 else (1 if l else 0)
def bq(p, n):
    if p % 3 == 2: bp, ab = 0, -p * p
    else:
        x = next(x for x in range(1, p) if any(x*x + 3*y*y == p for y in range(1, p))); bp, ab = 4*x*x - 2*p, p * p
    s0, s1 = 2, bp                     # alpha^k + beta^k recurrence
    for _ in range(n - 1): s0, s1 = s1, bp * s1 - ab * s0
    return s1
def N3(p, n):
    q = p**n
    if p == 3: return (q - 3)**2 - (4*(q - 9) if n % 2 == 0 else 0)
    return q*q - 7*q + 19 + 18*chi(-1, p, n) + 9*chi(-2, p, n) + 6*(1 + chi(-3, p, n)) + bq(p, n)
ctl = N3(7, 1) == 6 and N3(7, 2) == 2022 and N3(5, 3) == 14778 and N3(3, 2) == 36
print('CONTROL (q=7,49,125,9):', 'PASS' if ctl else 'FAIL')
for f in sys.argv[1:]:
    for k, (N, secs) in json.load(open(f)).items():
        p, n = map(int, k.split('^')); pr = N3(p, n)
        print('%s q=%d N3=%d predicted %d -> %s' % (k, p**n, N[2], pr, 'EQUAL' if N[2] == pr else 'DIFF'))
