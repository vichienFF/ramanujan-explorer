# rama-pp-nb: numba port of pp-hist (Singer set for q = p^k via F_{p^{3k}}; N(rho) over unit differences; M = N/3k stats).
import os, sys, json, time, math
import numpy as np
try:
    from numba import njit
    NUMBA = True
except ImportError:  # local fallback for correctness tests
    NUMBA = False
    def njit(*a, **k):
        return (lambda f: f) if not (a and callable(a[0])) else a[0]
T0 = time.time(); W = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
QS = [int(x) for x in os.environ.get("QS", "4913,6859").split(",")]

def factorize(n):
    fs, d = set(), 2
    while d * d <= n:
        while n % d == 0: fs.add(d); n //= d
        d += 1
    if n > 1: fs.add(n)
    return fs

def polymulmod(a, b, f, p):
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

def primitive_poly(p, n, seed):
    import random
    rng = random.Random(seed); order = p ** n - 1; fs = factorize(order); x = [0, 1] + [0] * (n - 2)
    while True:
        f = [rng.randrange(p) for _ in range(n)] + [1]
        if f[0] == 0: continue
        if polypow(x, order, f, p) != [1] + [0] * (n - 1): continue
        if all(polypow(x, order // r, f, p) != [1] + [0] * (n - 1) for r in fs): return f

@njit(cache=False)
def singer_scan(f, T, p, n, m):
    """S = {i in [0,m) : T @ x^i == 0 (mod p)} where x^i iterated in F_p[x]/(f)."""
    out = np.empty(m, np.int64); cnt = 0
    g = np.zeros(n, np.int64); g[0] = 1
    for i in range(m):
        ok = True
        for r in range(n):
            s = 0
            for c in range(n): s += T[r, c] * g[c]
            if s % p != 0:
                ok = False; break
        if ok:
            out[cnt] = i; cnt += 1
        top = g[n - 1]
        for c in range(n - 1, 0, -1): g[c] = g[c - 1]
        g[0] = 0
        if top:
            for c in range(n): g[c] = (g[c] - top * f[c]) % p
    return out[:cnt]

@njit(cache=False)
def inv_mod(a, m):
    t, nt, r, nr = 0, 1, m, a
    while nr:
        qq = r // nr
        t, nt = nt, t - qq * nt
        r, nr = nr, r - qq * nr
    if r != 1: return -1
    return t % m

@njit(cache=False)
def count_N(S, m):
    n = S.shape[0]; N = np.zeros(m, np.int32)
    for i in range(n):
        a = S[i]
        for j in range(n):
            if j == i: continue
            d = (S[j] - a) % m; iv = inv_mod(d, m)
            if iv < 0: continue
            for l in range(n):
                if l == i or l == j: continue
                r = ((S[l] - a) % m) * iv % m
                N[r] += 1
    return N

@njit(cache=False)
def good_mask(m):
    g = np.zeros(m, np.bool_)
    for x in range(2, m):
        if inv_mod(x, m) >= 0 and inv_mod(x - 1, m) >= 0: g[x] = True
    return g

def ppk(q):
    for p in range(2, q + 1):
        if q % p == 0:
            k, t = 0, q
            while t % p == 0: t //= p; k += 1
            return (p, k) if t == 1 else None

OUT = os.path.join(W, "pp_nb.jsonl"); done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)["q"])
for q in QS:
    if q in done: continue
    if time.time() - T0 > 10.5 * 3600: print("time guard", flush=True); break
    t0 = time.time(); p, k = ppk(q); n = 3 * k; m = q * q + q + 1
    f = primitive_poly(p, n, 1000003 * q)
    xq = polypow([0, 1] + [0] * (n - 2), q, f, p); cols = []; cur = [1] + [0] * (n - 1)
    for j in range(n): cols.append(cur); cur = polymulmod(cur, xq, f, p)
    F = np.array(cols, dtype=np.int64).T % p; T = (np.eye(n, dtype=np.int64) + F + F @ F) % p
    S = singer_scan(np.array(f, np.int64), T, p, n, m)
    assert len(S) == q + 1, (q, len(S))
    t1 = time.time()
    N = count_N(S, m); good = good_mask(m)
    Ng = N[good].astype(np.int64)
    ok3k = bool((Ng % (3 * k) == 0).all()); Mv = Ng // (3 * k)
    hist = np.bincount(Mv).tolist(); mu = float(Mv.mean()); var = float(Mv.var())
    gi = np.nonzero(good)[0]; order = np.argsort(-N[gi])[:12]
    top = [[int(gi[j]), int(N[gi[j]] // (3 * k))] for j in order]
    def cub(x): return [int((x * x % m * x - 3 * x + 1) % m == 0), int((x * x % m * x - 3 * x * x + 1) % m == 0)]
    top_cubic = [cub(t[0]) for t in top]
    rec_top = {"top12": top, "top12_cubic_roots": top_cubic}
    rec = {"q": q, "p": p, "k": k, "m": m, **rec_top, "n_good": int(good.sum()), "all_div_3k": ok3k, "M_mean": mu, "M_var": var,
           "VoverE": var / mu, "M_hist": hist, "numba": NUMBA, "sec_singer": round(t1 - t0, 1), "sec": round(time.time() - t0, 1)}
    open(OUT, "a").write(json.dumps(rec) + chr(10))
    print(json.dumps({x: rec[x] for x in ("q", "k", "all_div_3k", "VoverE", "sec_singer", "sec")}), flush=True)
print("finished", round((time.time() - T0) / 60, 1), "min", flush=True)
