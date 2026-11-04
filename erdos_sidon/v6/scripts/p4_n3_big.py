# H-N3-BIG / H-N3-HUGE (registered): N3 formula at every prime in [LO, HI).  # LOCAL-OK: benchmark q=2003 0.3 s -> [211,5000) ~5 min
# CONTROL: p4_n3 REF brute-force values reproduced first.
import sys
LO, HI = int(sys.argv[1]), int(sys.argv[2]); sys.argv = ['x', '0']
exec(open('p4_n3.py', encoding='utf-8').read().split("QS = ")[0])
print('CONTROL REF:', 'PASS' if ctl else 'FAIL', flush=True)
def chi(a, p): return 1 if pow(a % p, (p-1)//2, p) == 1 else -1
fails = []; n = 0
for q in range(LO, HI):
    if q < 2 or any(q % d == 0 for d in range(2, int(q**.5)+1)): continue
    N3 = Ns(q)[3]; pred = q*q - 7*q + 19 + 18*chi(-1, q) + 9*chi(-2, q) + 6*(1 + chi(-3, q)) + bq(q); n += 1
    if N3 != pred: fails.append(q)
print('primes tested %d in [%d,%d); failures %s -> %s' % (n, LO, HI, fails, ('PASS' if not fails else 'FAIL') if ctl else 'VOID'), flush=True)
