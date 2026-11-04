# Step 4zm coverage: N3 formula (Step 4a) at primes whose Frobenius in Q(i,sqrt2,sqrt-3,sqrt-7) is trivial (all four symbols +1), up to 1000,
# so every class of the tentative L has >= 2 verified primes.  # LOCAL-OK: numpy O(q^2), est. < 10 min
# CONTROL: p4_n3.Ns reproduces the sympy brute-force REF values (its own control) before use.
import sys
sys.argv = ['x', '0']
src = open('p4_n3.py', encoding='utf-8').read(); exec(src.split("QS = ")[0])
print('CONTROL p4_n3 REF:', 'PASS' if ctl else 'FAIL')
def chi(a, p): return 1 if pow(a % p, (p-1)//2, p) == 1 else -1
P = [p for p in range(200, 1000) if all(p % d for d in range(2, int(p**.5)+1)) and all(chi(a, p) == 1 for a in (-1, 2, -3, -7))]
ok = True
for q in P:
    N = Ns(q); pred = q*q - 7*q + 19 + 18 + 9 + 12 + bq(q); ok &= N[3] == pred
    print('q=%d N3=%d formula %d %s' % (q, N[3], pred, 'EQUAL' if N[3] == pred else 'DIFF'), flush=True)
print('identity-class primes 200..1000:', P, '-> all equal:', ok)
