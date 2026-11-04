r"""R2 (FFA math referee S2): the determinant of Frob_p on T, eta(p) p^2, eta a quadratic character unramified outside {2,3,5}, equals (-3/p) p^2.  # LOCAL-OK: < 20 min
Argument: T is 2-dimensional, orthogonal, pure of weight 2 (|alpha| = |beta| = p). If tr(Frob_p|T) != 0 then det = +p^2 (det = -p^2 would force real
eigenvalues {p, -p} and trace 0). For the test primes p = 1 mod 3, tr = (3/p) b_p != 0 (b_p = 4x^2 - 2p), so det = p^2 = (-3/p) p^2. For the test primes
p = 2 mod 3 we compute det = (tr_p^2 - tr_{p^2})/2 = -tr_{p^2}/2 with tr_{p^2} = B(p^2) - 3p^2 from (5.3) (chi_{p^2}(-1) = 1): det = -p^2 <=> B(p^2) = 5p^2.
Since eta and eps_K = (-3/.) are quadratic characters unramified outside {2,3,5}, agreement at representatives of all 16 Frobenius classes of
Q(i, sqrt2, sqrt3, sqrt5) (the Livne test set 7,...,241) gives eta = eps_K.
B(q) = sum_{s,m in F_q} chi(s m H(s,m)), H = m^3+8m^2-3ms^2+6ms+13m+2s^3+2s^2-10s+6, computed over GF(p^2) (numpy, log tables).
CONTROL: B(17^2) = 1445, B(23^2) = 2645, B(29^2) = 4205 must equal the Sage values in p4_ppB.out (independent code), and B(p) for prime p must equal
2p + chi(-1)p + chi(3) b_p at p = 7, 13 (Theorem B, independently verified in p4_trT.py)."""
import sys, re, numpy as np
from sympy import factorint
from sympy.polys.galoistools import gf_irreducible_p, gf_pow_mod
from sympy.polys.domains import ZZ
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
def field(p, n):
    q = p**n; N = q - 1; W = p ** np.arange(n)
    if n == 1:
        g = next(g for g in range(2, p) if all(pow(g, N//r, p) != 1 for r in factorint(N))); exp = np.array([pow(g, i, p) for i in range(N)], np.int64)
    else:
        fac = list(factorint(N))
        for t in range(p**n):
            c = [(t // p**i) % p for i in range(n)]; P = [1] + c[::-1]
            if c[0] and gf_irreducible_p(P, p, ZZ) and all(gf_pow_mod([1, 0], N//r, P, p, ZZ) != [1] for r in fac): break
        exp = np.zeros(N, np.int64); v = [1] + [0]*(n-1)
        for i in range(N):
            exp[i] = sum(d * p**k for k, d in enumerate(v)); top = v[-1]; v = [0] + v[:-1]; v = [(v[k] - top*c[k]) % p for k in range(n)]
    log = np.full(q, -1, np.int64); log[exp] = np.arange(N); DIG = (np.arange(q)[:, None] // W) % p
    add = lambda a, b: ((DIG[a] + DIG[b]) % p) @ W
    mul = lambda a, b: np.where((a == 0) | (b == 0), 0, exp[(log[a] + log[b]) % N])
    chi = lambda a: np.where(a == 0, 0, np.where(log[a] % 2 == 0, 1, -1))
    I = lambda k: np.int64(k % p)
    return q, add, mul, chi, I
def B(p, n):
    q, add, mul, chi, I = field(p, n); m = np.arange(q); tot = 0
    m2 = mul(m, m); m3 = mul(m2, m)
    for s in range(q):
        S = np.full(q, s, np.int64); s2 = mul(S, S); s3 = mul(s2, S)
        H = add(m3, mul(np.full(q, I(8)), m2))
        H = add(H, mul(np.full(q, I(-3)), mul(m, s2))); H = add(H, mul(np.full(q, I(6)), mul(m, S))); H = add(H, mul(np.full(q, I(13)), m))
        H = add(H, mul(np.full(q, I(2)), s3)); H = add(H, mul(np.full(q, I(2)), s2)); H = add(H, mul(np.full(q, I(-10)), S)); H = add(H, np.full(q, I(6)))
        tot += int(chi(mul(mul(S, m), H)).sum())
    return tot
def leg(a, p): a %= p; return 0 if a == 0 else (1 if pow(a, (p-1)//2, p) == 1 else -1)
def bp(p):
    if p % 3 == 2: return 0
    x = next(x for x in range(1, p) if any(x*x + 3*y*y == p for y in range(1, p))); return 4*x*x - 2*p
ppB = open('p4_ppB.out', encoding='utf-8', errors='replace').read()
ref = {int(q): int(v) for q, v in re.findall(r'q=(\d+)\D[^\n]*?B=(-?\d+)', ppB)}
ctl = all(B(p, 1) == 2*p + leg(-1, p)*p + leg(3, p)*bp(p) for p in (7, 13))
ctl2 = {qq: (ref.get(qq), B(int(round(qq ** 0.5)), 2)) for qq in (289, 529, 841)}
ok2 = all(a is not None and a == b for a, b in ctl2.values())
print('CONTROL Theorem B at p=7,13:', 'PASS' if ctl else 'FAIL', '| CONTROL vs p4_ppB.out (Sage) at 289,529,841:', ctl2, 'PASS' if ok2 else 'FAIL/MISSING', flush=True)
T2 = [11, 17, 23, 29, 41, 53, 71, 83]          # Livne test primes = 2 mod 3
for p in T2:
    b = B(p, 2); print('p=%d: B(p^2)=%d, 5p^2=%d, det = -tr_{p^2}/2 = %d -> %s' % (p, b, 5*p*p, -(b - 3*p*p)//2, 'det = -p^2' if b == 5*p*p else 'MISMATCH'), flush=True)
T1 = [7, 13, 19, 31, 43, 61, 73, 241]
print('test primes = 1 mod 3: b_p =', {p: bp(p) for p in T1}, '(all nonzero -> det = +p^2 by weight)')
