"""Amendment 22-4 Route B: largest gap over all dilations of Bose sets (primes q in [101, 2003]) and Singer sets (primes q in
[31, 211]); null model: random subsets of Z_m of the same size. One jsonl line per (kind, q) checkpoint; time check per batch.
Bose(q): F_{q^2} = F_q[x]/(x^2 - a1 x - b1) primitive; A = {a in [0, q^2-2] : x^a = u + 1*x}, m = q^2 - 1, |A| = q.
Singer(q): F_{q^3} = F_q[x]/(x^3 - c2 x^2 - c1 x - c0) primitive; A = {a mod m : coeff of x^2 in x^a is 0}, m = q^2 + q + 1, |A| = q+1.
Statistic per set: for every multiplier t (one per class {+-t, +-tq mod m}), largest cyclic gap of t*A mod m; G* = max,
plus median and 99th percentile over t; ruler excess from the best cut: |A| - sqrt(m - G* + 1).
Usage: python b22c_gaps.py <out.jsonl>   env SHARD=i/k, TLIM_H, KINDS (bose,singer,null)."""
import json, math, os, random, sys, time
import numpy as np
T0 = time.time(); TLIM = float(os.environ.get("TLIM_H", "7.5")) * 3600

def primes(lo, hi):
    s = bytearray([1]) * (hi + 1); s[:2] = b"\x00\x00"
    for i in range(2, int(hi ** 0.5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [p for p in range(lo, hi + 1) if s[p]]

def factor(n):
    f, d = set(), 2
    while d * d <= n:
        while n % d == 0: f.add(d); n //= d
        d += 1
    if n > 1: f.add(n)
    return f

def mulmod_poly(a, b, q, mod):          # polynomials as lists low->high over F_q, reduce by monic mod (x^k = sum mod[i] x^i)
    k = len(mod); r = [0] * (2 * k - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b): r[i + j] = (r[i + j] + ai * bj) % q
    for d in range(2 * k - 2, k - 1, -1):
        c = r[d]
        if c:
            r[d] = 0
            for i, mi in enumerate(mod): r[d - k + i] = (r[d - k + i] + c * mi) % q
    return r[:k]

def powmod_poly(e, q, mod):
    k = len(mod); res = [1] + [0] * (k - 1); base = [0, 1] + [0] * (k - 2)
    while e:
        if e & 1: res = mulmod_poly(res, base, q, mod)
        base = mulmod_poly(base, base, q, mod); e >>= 1
    return res

def primitive_mod(q, k, rng):
    order = q ** k - 1; fs = factor(order); one = [1] + [0] * (k - 1)
    while True:
        mod = [rng.randrange(q) for _ in range(k)]
        if mod[0] == 0: continue
        if powmod_poly(order, q, mod) != one: continue
        if all(powmod_poly(order // r, q, mod) != one for r in fs): return mod

def bose_set(q, rng):
    a1b1 = primitive_mod(q, 2, rng); b1, a1 = a1b1          # x^2 = b1 + a1 x
    u, v, out = 1, 0, []
    for a in range(q * q - 1):
        if v == 1: out.append(a)
        u, v = (b1 * v) % q, (u + a1 * v) % q
    return np.array(out, dtype=np.int64), q * q - 1

def singer_set(q, rng):
    c = primitive_mod(q, 3, rng); m = q * q + q + 1             # x^3 = c0 + c1 x + c2 x^2
    e0, e1, e2, res = 1, 0, 0, set()
    for a in range(q ** 3 - 1):
        if e2 == 0: res.add(a % m)
        e0, e1, e2 = (c[0] * e2) % q, (e0 + c[1] * e2) % q, (e1 + c[2] * e2) % q
    return np.array(sorted(res), dtype=np.int64), m

def is_sidon_mod(A, m):
    d = ((A[:, None] - A[None, :]) % m)[~np.eye(len(A), dtype=bool)]
    return len(np.unique(d)) == len(d)

def dilate_gaps(A, m, q, frob=True):
    ts = [t for t in range(1, m) if math.gcd(t, m) == 1 and t == min(t, m - t, (t * q) % m, m - (t * q) % m)] if frob else \
         [t for t in range(1, m // 2 + 1) if math.gcd(t, m) == 1]
    ts = np.array(ts, dtype=np.int64); best = np.empty(len(ts), dtype=np.int64); bs = max(1, 4_000_000 // len(A))
    for i in range(0, len(ts), bs):
        if time.time() - T0 > TLIM: return None
        B = np.sort((ts[i:i + bs, None] * A[None, :]) % m, axis=1)
        g = np.diff(B, axis=1).max(axis=1); w = B[:, 0] + m - B[:, -1]; best[i:i + bs] = np.maximum(g, w)
    return best

def record(kind, q, A, m, extra):
    tq = time.time(); g = dilate_gaps(A, m, q, frob=(kind != "null"))
    if g is None: return None
    G = int(g.max()); L = m - G                                   # ruler length after cutting at the best gap
    return {"kind": kind, "q": q, "m": m, "size": len(A), "G_star": G, "g_star_over_q": G / q, "median_gap_over_q": float(np.median(g)) / q,
            "p99_gap_over_q": float(np.percentile(g, 99)) / q, "excess_best_cut": len(A) - math.sqrt(L + 1), "n_mult": int(len(g)),
            "sec": round(time.time() - tq, 1), **extra}

if __name__ == "__main__":
    outf = sys.argv[1]; si, sk = map(int, os.environ.get("SHARD", "0/1").split("/")); kinds = os.environ.get("KINDS", "bose,singer,null").split(",")
    done = set()
    if os.path.exists(outf):
        for l in open(outf):
            try: r = json.loads(l); done.add((r["kind"], r["q"], r.get("rep", 0)))
            except (ValueError, KeyError): pass
    jobs = []
    if "singer" in kinds: jobs += [("singer", q, 0) for q in primes(31, 211)]
    if "bose" in kinds: jobs += [("bose", q, 0) for q in primes(101, 2003)]
    if "null" in kinds:
        sub = primes(101, 2003)[::max(1, len(primes(101, 2003)) // 20)][:20]
        jobs += [("null", q, r) for q in sub for r in (1, 2, 3)]
    jobs.sort(key=lambda j: (j[1], j[0]))
    for idx, (kind, q, rep) in enumerate(jobs):
        if idx % sk != si or (kind, q, rep) in done: continue
        if time.time() - T0 > TLIM: print("time limit", flush=True); break
        rng = random.Random(1000003 * q + rep)
        if kind == "bose": A, m = bose_set(q, rng)
        elif kind == "singer": A, m = singer_set(q, rng)
        else:
            m = q * q - 1; A = np.array(sorted(random.Random(77 * q + rep).sample(range(m), q)), dtype=np.int64)
        ok = is_sidon_mod(A, m) if kind != "null" else None
        if kind != "null" and (not ok or len(A) != (q if kind == "bose" else q + 1)):
            r = {"kind": kind, "q": q, "err": "construction failed", "size": len(A), "sidon": ok}
        else:
            r = record(kind, q, A, m, {"rep": rep, "sidon": ok})
            if r is None: print("time limit inside", kind, q, flush=True); break
        open(outf, "a").write(json.dumps(r) + "\n"); print(json.dumps(r), flush=True)
