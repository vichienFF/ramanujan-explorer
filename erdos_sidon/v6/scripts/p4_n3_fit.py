# Fit each N3-exclusion category over primes 7..61 to integer combos of {1,f1,f2,f3,f1f2} x {1,q}; report exact fits (read-off, to be proved by hand).  # LOCAL-OK: seconds
# CONTROL: the fit of the total E reproduces the derived closed form -(10+6f1)q+25+18f1+9f2+4f3.
import re, ast, itertools, numpy as np
from fractions import Fraction
rows = []
import subprocess
for line in open('p4_n3_assembly.out', encoding='utf-8'):
    m = re.match(r'q=(\d+) .*f1,f2,f3=(-?\d),(-?\d),(-?\d) \| (\{.*\})', line)
    if m: rows.append((int(m[1]), int(m[2]), int(m[3]), int(m[4]), ast.literal_eval(m[5])))
for line in ["q=7 x | f1,f2,f3=-1,-1,1 | {'c+d=0': -4, 'c=0 or d=0': 0, 'c=1 (root y=1)': -2, 'diagonal u^2=4v': -10, 'generic': 0, 'pairs with y=1': 4, 'repeated/other': -4, 'singular t1^4=t2^4': 0, 't=-1 (y=inf)': -10}",
             "q=11 x | f1,f2,f3=-1,1,-1 | {'c+d=0': -6, 'c=0 or d=0': 0, 'c=1 (root y=1)': -2, 'diagonal u^2=4v': -8, 'generic': 0, 'pairs with y=1': 16, 'repeated/other': -12, 'singular t1^4=t2^4': 0, 't=-1 (y=inf)': -20}",
             "q=13 x | f1,f2,f3=1,-1,1 | {'c=0 or d=0': -108, 'diagonal u^2=4v': -16, 'generic': 0, 'pairs with y=1': 8, 'repeated/other': -8, 'singular t1^4=t2^4': -22, 't=-1 (y=inf)': -24}"]:
    m = re.match(r'q=(\d+) .*f1,f2,f3=(-?\d),(-?\d),(-?\d) \| (\{.*\})', line); rows.append((int(m[1]), int(m[2]), int(m[3]), int(m[4]), ast.literal_eval(m[5])))
rows.sort(); cats = sorted({k for r in rows for k in r[4]} | {'TOTAL'})
names = ['1', 'f1', 'f2', 'f3', 'f1f2', 'f1f3', 'q', 'q f1', 'q f2', 'q f3', 'q f1f2', 'q^2', 'q^2 f1']
def basis(q, a, b, c): return [1, a, b, c, a*b, a*c, q, q*a, q*b, q*c, q*a*b, q*q, q*q*a]
M = np.array([basis(*r[:4]) for r in rows], float)
for k in cats:
    y = np.array([sum(r[4].values()) if k == 'TOTAL' else r[4].get(k, 0) for r in rows], float)
    x, *_ = np.linalg.lstsq(M, y, rcond=None); xr = np.round(x * 2) / 2; exact = np.allclose(M @ xr, y)
    print('%-22s %s %s' % (k, 'EXACT' if exact else 'NO FIT', ' + '.join('%g*%s' % (c, n) for c, n in zip(xr, names) if c)))
