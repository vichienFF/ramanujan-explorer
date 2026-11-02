r"""Lemma (Version 5): for every unit l mod m,  P(l) - (q-2)^2 = sum_mu (I_l(mu))_3,  I_l(mu) = |S cap (l S + mu)|.  # LOCAL-OK: seconds
Found by the 2026-11-01 referee (own code); this script is a separate implementation for the release.
Field F_{q^3} = F_q[t]/(cubic) with t primitive; S = {log(x) mod m : x in span(1, t)} (a line of PG(2,q), i.e. a Singer set).
CONTROLS (theory, independent of the lemma): (i) l = 1: P(1) - (q-2)^2 = q^3 - q (direct count: c = d = 1, plus c != d) and the
third moment is 3 (n)_3 / 3 = (n)_3 from mu = 0 only (Sidon); (ii) l = -1 and 2: third moment 0 (conic/Bezout, Section 6).
Usage: python v5_lemma_I3.py q1 q2 ...   (odd primes)"""
import sys, numpy as np, sympy
def field(q):
    n = q ** 3 - 1
    for f0 in range(1, q):
        for f1 in range(q):
            for f2 in range(q):
                exp = np.empty(n, np.int64); a = (1, 0, 0); ok = True
                for i in range(n):
                    c = a[0] + a[1] * q + a[2] * q * q
                    if i and c == 1: ok = False; break
                    exp[i] = c; a = ((f0 * a[2]) % q, (a[0] + f1 * a[2]) % q, (a[1] + f2 * a[2]) % q)
                if ok and a == (1, 0, 0):
                    log = np.full(q ** 3, -1, np.int64); log[exp] = np.arange(n); return log
bad = 0
for q in map(int, sys.argv[1:] or [5, 7, 11, 13]):
    m = q * q + q + 1; n = q + 1; log = field(q)
    c = np.arange(q ** 3); one_minus = ((1 - c % q) % q) + ((-(c // q % q)) % q) * q + ((-(c // q // q)) % q) * q * q
    ys = np.arange(2, q ** 3); A = log[ys] % m; B = log[one_minus[ys]] % m
    cnt = np.bincount(A * m + B, minlength=m * m)
    P = lambda l: int(cnt[((l * A) % m) * m + (l * B) % m].sum())
    S = np.array(sorted({int(log[a + b * q]) % m for a in range(q) for b in range(q) if a or b})); assert len(S) == n
    ind = np.zeros(m, np.int64); ind[S] = 1
    def mom3(l):
        lS = (l * S) % m; I = np.array([ind[(lS + mu) % m].sum() for mu in range(m)])
        return int((I * (I - 1) * (I - 2)).sum())
    ctl = P(1) - (q - 2) ** 2 == q ** 3 - q and mom3(1) == n * (n - 1) * (n - 2) and mom3(m - 1) == 0 and mom3(2) == 0
    ls = [l for l in [1, 2, -1, -2, 3, 4, 5, 7, q, (q + 3) % m] if np.gcd(l % m, m) == 1]
    res = [(l, P(l % m) - (q - 2) ** 2, mom3(l % m)) for l in ls]
    ok = all(a == b for _, a, b in res); bad += not (ok and ctl)
    print('q=%d CONTROL %s | lemma %s on l=%s' % (q, 'PASS' if ctl else 'FAIL', 'MATCH' if ok else 'MISMATCH ' + str(res), [l for l, _, _ in res]))
sys.exit(1 if bad else 0)
