"""Version 6: recompute the (N3) verification counts quoted in the paper (rule after E97: counts are computed, never typed).  # LOCAL-OK: ~10 min
(N3): N3 = q^2 - 7q + 19 + 18 phi(-1) + 9 phi(-2) + 6(1 + phi(-3)) + b_q, N3 = sum over (c,d) in (F_q^*)^2 of (#roots in F_q of c y^4 + d(1-y)^4 - 1)_3.
Local part: every prime 7 <= q < LIMIT (default 5000) with p4_n3.Ns. Kaggle part: ../kaggle_outputs/c9-n3-huge-{a,b}_n3_huge.json (fields lo, hi, tested, fails).
CONTROL: Ns matches the brute-force values REF of p4_n3.py (q = 5..19), and N1 = (q-2)^2 + 2(q-1) for every q.
Usage: python v6_counts.py [LIMIT]   (run from this folder)
"""
import sys, os, json
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
src = open('p4_n3.py', encoding='utf-8').read().split('QS = ')[0]; sys.argv = sys.argv[:2]; exec(src)   # defines bq, Ns, REF, ctl
LIM = int(sys.argv[1]) if sys.argv[1:] else 5000
def leg(a, q): return 0 if a % q == 0 else (1 if pow(a % q, (q - 1) // 2, q) == 1 else -1)
P = [p for p in range(7, LIM) if all(p % d for d in range(2, int(p ** .5) + 1))]
fails = []
for q in P:
    N = Ns(q); assert N[1] == (q - 2) ** 2 + 2 * (q - 1)
    if N[3] != q*q - 7*q + 19 + 18*leg(-1, q) + 9*leg(-2, q) + 6*(1 + leg(-3, q)) + bq(q): fails.append(q)
tot, kf = len(P), len(fails)
for k in ('a', 'b'):
    j = json.load(open(os.path.join(D, '..', 'kaggle_outputs', 'c9-n3-huge-%s_n3_huge.json' % k)))
    print('Kaggle %s: primes in [%d, %d) tested %d, failures %s' % (k, j['lo'], j['hi'], j['tested'], j['fails']))
    tot += j['tested']; kf += len(j['fails'])
print('CONTROL (brute-force REF q=5..19, N1 formula):', 'PASS' if ctl else 'FAIL')
print('local: %d primes 7..%d, failures %s' % (len(P), LIM - 1, fails))
print('TOTAL primes with (N3) checked: %d, failures %d' % (tot, kf))
