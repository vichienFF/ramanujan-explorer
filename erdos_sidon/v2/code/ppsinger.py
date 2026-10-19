"""Singer sets for prime-power q = p^k via F_{p^{3k}} = F_p[x]/(f), f primitive of degree 3k; line = ker Tr_{F_{q^3}/F_q}."""
import random, numpy as np
def polymulmod(a, b, f, p):          # a,b coefficient lists (low->high), f monic degree n
    n = len(f) - 1; r = [0] * (2 * n - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b): r[i + j] = (r[i + j] + ai * bj) % p
    for d in range(len(r) - 1, n - 1, -1):
        c = r[d]
        if c:
            for j in range(n + 1): r[d - n + j] = (r[d - n + j] - c * f[j]) % p
    return r[:n]
def polypow(a, e, f, p):
    res = [1] + [0] * (len(f) - 2); base = a[:]
    while e:
        if e & 1: res = polymulmod(res, base, f, p)
        base = polymulmod(base, base, f, p); e >>= 1
    return res
def factorize(n):
    fs, d = set(), 2
    while d * d <= n:
        while n % d == 0: fs.add(d); n //= d
        d += 1
    if n > 1: fs.add(n)
    return fs
def primitive_poly(p, n, rng):
    order = p ** n - 1; fs = factorize(order); x = [0, 1] + [0] * (n - 2)
    while True:
        f = [rng.randrange(p) for _ in range(n)] + [1]
        if f[0] == 0: continue
        if polypow(x, order, f, p) != [1] + [0] * (n - 1): continue
        if all(polypow(x, order // r, f, p) != [1] + [0] * (n - 1) for r in fs): return f
def singer_pp(p, k, rng):
    q = p ** k; n = 3 * k; f = primitive_poly(p, n, rng); m = q * q + q + 1
    # Frobenius x -> x^q as an F_p-linear map: columns = (x^j)^q
    xq = polypow([0, 1] + [0] * (n - 2), q, f, p)
    cols = []; cur = [1] + [0] * (n - 1)
    for j in range(n): cols.append(cur); cur = polymulmod(cur, xq, f, p)
    F = np.array(cols, dtype=np.int64).T % p; T = (np.eye(n, dtype=np.int64) + F + F @ F) % p
    S = []; g = [1] + [0] * (n - 1); xx = [0, 1] + [0] * (n - 2)
    for i in range(m):
        if not np.any((T @ np.array(g)) % p): S.append(i)
        g = polymulmod(g, xx, f, p)
    return np.array(S, dtype=np.int64), m, q
if __name__ == "__main__":
    for p, k in ((2, 2), (2, 3), (3, 2), (3, 3), (5, 2), (2, 5)):
        S, m, q = singer_pp(p, k, random.Random(7))
        d = ((S[:, None] - S[None, :]) % m)[~np.eye(len(S), dtype=bool)]
        print(q, "m", m, "|S|", len(S), "== q+1:", len(S) == q + 1, "perfect difference set:", len(np.unique(d)) == m - 1)
