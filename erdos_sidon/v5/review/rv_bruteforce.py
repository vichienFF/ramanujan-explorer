"""Independent referee brute force for N2_PROOF.md (does not import authors' code).
CONTROL: known-answer asserts -- Legendre symbol table vs Euler criterion, sum_x chi(x^2+3) = -1,
and |J(chi1,chi2)|^2 = q for nontrivial chi1,chi2,chi1*chi2 in the Greene part.
Usage: python rv_bruteforce.py 5 7 11 ...
For each prime q: counts factorisation types of Q_{c,d} by direct evaluation, computes P, S2 (via explicit
polynomial division), T (direct (u,v) sum), G(4), Greene 3F2(phi,phi,phi;eps,eps|4) from the definition,
and compares with every closed form claimed in N2_PROOF.md.
"""
import sys, cmath
from fractions import Fraction

def legendre_table(q):
    t = [0]*q
    for x in range(1, q):
        t[(x*x) % q] = 1
    return [0] + [1 if t[x] else -1 for x in range(1, q)]

def bq(q):
    if q % 3 == 2:
        return 0
    for x in range(1, q):
        r = q - x*x
        if r <= 0: break
        if r % 3 == 0:
            y2 = r // 3
            y = int(round(y2**0.5))
            if y*y == y2:
                return 4*x*x - 2*q
    raise ValueError

def polydivmod(a, b, q):
    # a,b coefficient lists highest-first, b monic
    a = a[:]; out = []
    while len(a) >= len(b):
        c = a[0] % q; out.append(c)
        for i in range(len(b)):
            a[i] = (a[i] - c*b[i]) % q
        a.pop(0)
    return out, a

def run(q):
    chi = legendre_table(q)
    # CONTROL
    for x in range(q):
        assert chi[x] == (0 if x == 0 else (1 if pow(x, (q-1)//2, q) == 1 else -1))
    assert sum(chi[(x*x+3) % q] for x in range(q)) == -1
    inv = lambda a: pow(a, q-2, q)
    S = range(2, q)  # F_q minus {0,1}
    types = {}
    roots_total = 0; pairs_total = 0; S2 = 0
    for c in range(1, q):
        for d in range(1, q):
            Q = [1, q-2, (1-c-d) % q, (2*c) % q, (-c) % q]
            roots = [y for y in range(q) if (((((y-2)*y + (1-c-d))*y + 2*c)*y - c) % q) == 0]
            assert all(y not in (0, 1) for y in roots)
            # multiplicities
            mult = []
            for y in roots:
                m = 0; P = Q[:]
                while True:
                    qq, r = polydivmod(P, [1, (-y) % q], q)
                    if any(r): break
                    m += 1; P = qq
                mult.append(m)
            # degree pattern of non-linear part: deg of cofactor after removing all linear factors
            rest = 4 - sum(mult)
            # rest in {0,2,3,4}: 2 -> irreducible quadratic or square? (no roots => irreducible quad);
            # 4 -> (2)(2), (4), or (2)^2 ; 3 -> irreducible cubic
            key = (tuple(sorted(mult)), rest)
            types[key] = types.get(key, 0) + 1
            roots_total += len(roots)
            for i in range(len(roots)):
                for j in range(i+1, len(roots)):
                    y1, y2 = roots[i], roots[j]
                    u, v = (y1+y2) % q, (y1*y2) % q
                    quo, rem = polydivmod(Q, [1, (-u) % q, v], q)
                    assert not any(rem)
                    s, p = (-quo[1]) % q, quo[2]
                    S2 += chi[(s*s - 4*p) % q]
                    pairs_total += 1
                    # admissibility formula check
                    assert u != 0 and u != 2 and (2*v - u) % q != 0
                    # disc formula check: disc = u(u-2)(2v-u+2)/(2v-u)
                    assert (s*s-4*p) % q == (u*(u-2)*(2*v-u+2)*inv((2*v-u) % q)) % q
    N = types.get(((1,), 3), 0)
    A = types.get(((1, 1), 2), 0)
    E = types.get(((2,), 2), 0)
    B = types.get(((1, 1, 1, 1), 0), 0)
    C = types.get(((1, 1, 2), 0), 0)
    D = types.get(((2, 2), 0), 0)
    bad = [k for k in types if k[0] and (3 in k[0] or 4 in k[0])]
    assert not bad, bad
    b = bq(q)
    z0 = 1 + chi[(-3) % q]
    # admissible pairs by direct definition: distinct y1,y2 in S with a (c,d) in (F*)^2 having both as roots
    Pdirect = 0
    for y1 in S:
        for y2 in S:
            if y2 <= y1: continue
            # solve 2x2 system directly
            a11, a12, r1 = (1-y1)**2 % q, y1*y1 % q, (y1*y1*(1-y1)**2) % q
            a21, a22, r2 = (1-y2)**2 % q, y2*y2 % q, (y2*y2*(1-y2)**2) % q
            det = (a11*a22 - a12*a21) % q
            if det == 0:
                continue  # parallel distinct lines (checked by hand); verify no solution below
            cc = ((r1*a22 - r2*a12) * inv(det)) % q
            dd = ((a11*r2 - a21*r1) * inv(det)) % q
            if cc and dd: Pdirect += 1
    # T directly in (u,v)
    T = sum(chi[(u*u-4*v) % q]*chi[(u*(u-2)*(2*v-u)*(2*v-u+2)) % q] for u in range(q) for v in range(q))
    G4 = sum(chi[x]*chi[y]*chi[(1-x) % q]*chi[(1-y) % q]*chi[(x-4*y) % q] for x in range(q) for y in range(q))
    # Greene 3F2 from definition
    g = next(gg for gg in range(2, q) if all(pow(gg, (q-1)//pf, q) != 1 for pf in primefactors(q-1)))
    dlog = {}
    x = 1
    for j in range(q-1):
        dlog[x] = j; x = x*g % q
    def ch(k, a):
        a %= q
        if a == 0: return 0
        return cmath.exp(2j*cmath.pi*k*dlog[a]/(q-1))
    h = (q-1)//2  # phi = character index h
    def J(k1, k2):
        return sum(ch(k1, x)*ch(k2, 1-x) for x in range(q))
    # CONTROL: |J|^2 = q for k1,k2,k1+k2 nontrivial
    assert abs(abs(J(1, 2 % (q-1) or 1))**2 - q) < 1e-6 or (1+ (2 % (q-1) or 1)) % (q-1) == 0
    def binom(kA, kB):
        return ch(kB, -1)/q * J(kA, (-kB) % (q-1))
    F = 0
    for k in range(q-1):
        F += binom((h+k) % (q-1), k)**3 * ch(k, 4)
    F *= q/(q-1)
    lhs = q*q*F
    rhs = chi[q-1]*G4
    res = dict(q=q, N=N, A=A, B=B, C=C, D=D, E=E, other={k: v for k, v in types.items()
               if k not in [((1,),3),((1,1),2),((2,),2),((1,1,1,1),0),((1,1,2),0),((2,2),0)]},
               roots=roots_total, P=pairs_total, Pdirect=Pdirect, S2=S2, T=T, G4=G4, b=b, F=F)
    checks = {
        'N formula': 3*N == (q-2)*(q+1) + b,
        'roots=(q-2)^2': roots_total == (q-2)**2,
        'P=(q-3)(q-5)/2': 2*pairs_total == (q-3)*(q-5) and Pdirect == pairs_total,
        'S2=(T-4q+14)/2': 2*S2 == T - 4*q + 14,
        'T=1+phi(-1)G4': T == 1 + chi[q-1]*G4,
        'T=q+1+b': T == q+1+b,
        'E': 2*E == q+1-z0, 'C': 2*C == q-5-z0, 'D': 2*D == z0,
        'id roots': roots_total == N+E+2*A+2*D+3*C+4*B,
        'id pairs': pairs_total == A+D+3*C+6*B,
        'id S2': S2 == -A+D+2*C+6*B,
        'q^2 3F2(4)=phi(-1)G4': abs(lhs - rhs) < 1e-6,
        # Version 5: a dummy entry 'P(-2)': True (always passed) was removed; P(-2) is checked in scripts/n2_height.py and scripts/v5_lemma_I3.py.
    }
    if q % 3 == 2:
        checks['3F2(4)=1/q'] = abs(F - 1/q) < 1e-9
    return res, checks

def primefactors(n):
    out = []; p = 2
    while p*p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0: n //= p
        p += 1
    if n > 1: out.append(n)
    return out

if __name__ == '__main__':
    # known-answer CONTROL for b_q: q=7=2^2+3 -> 16-14=2; q=13=1+12 -> 4-26=-22
    assert bq(7) == 2 and bq(13) == -22 and bq(5) == 0
    nfail = 0
    if not sys.argv[1:]: print('usage: python rv_bruteforce.py q1 q2 ... (primes >= 5)'); sys.exit(1)
    for a in sys.argv[1:]:
        res, ch = run(int(a))
        F = res.pop('F')
        print(res, 'F=%.6f%+.6fi' % (F.real, F.imag))
        print('   ', 'ALL PASS' if all(ch.values()) else {k: v for k, v in ch.items() if not v})
        nfail += not all(ch.values())
    sys.exit(1 if nfail else 0)  # Version 5: non-zero exit on any failed check
