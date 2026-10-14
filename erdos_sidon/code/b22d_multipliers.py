"""Amendment 22-5: do the multipliers giving record gaps have structure? For each Bose set (same construction/seeds as
b22c_gaps.py) and each null random set: top-10 multipliers by largest gap vs ALL admissible multipliers (exact).
Statistics: u = (t mod (q+1))/(q+1), v = (t mod (q-1))/(q-1), w = log(ord_m t)/log m. Pooled two-sample KS, Bonferroni 0.01/3.
Control: null random sets must not reject (all p > 0.01) else VOID."""
import json, math, os, random, sys
import numpy as np
from scipy.stats import ks_2samp
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import b22c_gaps as B

def lam_factors(m):
    f, n, d = {}, m, 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    lam = 1
    for p, e in f.items():
        c = (p - 1) * p ** (e - 1) if p > 2 else (1 if e == 1 else 2 if e == 2 else 2 ** (e - 2))
        lam = lam * c // math.gcd(lam, c)
    return lam, sorted(B.factor(lam))

def vpow(t, e, m):
    r = np.ones_like(t); b = t % m
    while e:
        if e & 1: r = (r * b) % m
        b = (b * b) % m; e >>= 1
    return r

def orders(t, m):
    lam, ps = lam_factors(m); d = np.full(len(t), lam, dtype=np.int64)
    for p in ps:
        while True:
            cand = d % p == 0
            if not cand.any(): break
            idx = np.nonzero(cand)[0]; dd = d[idx] // p
            ok = np.array([pow(int(x), int(y), m) == 1 for x, y in zip(t[idx], dd)]) if len(idx) < 2000 else None
            if ok is None:                                    # vectorised for large batches, grouped by exponent
                ok = np.zeros(len(idx), bool)
                for e in np.unique(dd): sel = dd == e; ok[sel] = vpow(t[idx][sel], int(e), m) == 1
            if not ok.any(): break
            d[idx[ok]] = dd[ok]
    return d

def stats(t, q, m):
    return (t % (q + 1)) / (q + 1), (t % (q - 1)) / (q - 1), np.log(orders(t, m).astype(float)) / math.log(m)

def gaps_all(A, m, q, frob):
    ts = np.array([t for t in range(1, m) if math.gcd(t, m) == 1 and t == min(t, m - t, (t * q) % m, m - (t * q) % m)] if frob else
                  [t for t in range(1, m // 2 + 1) if math.gcd(t, m) == 1], dtype=np.int64)
    g = np.empty(len(ts), np.int64); bs = max(1, 4_000_000 // len(A))
    for i in range(0, len(ts), bs):
        Bm = np.sort((ts[i:i + bs, None] * A[None, :]) % m, axis=1)
        g[i:i + bs] = np.maximum(np.diff(Bm, axis=1).max(axis=1), Bm[:, 0] + m - Bm[:, -1])
    return ts, g

def run(kind):
    rec, ref = [[], [], []], [[], [], []]
    qs = B.primes(101, 2003) if kind == "bose" else B.primes(101, 2003)[::max(1, len(B.primes(101, 2003)) // 20)][:20]
    for q in qs:
        reps = [0] if kind == "bose" else [1, 2, 3]
        for rep in reps:
            if kind == "bose": A, m = B.bose_set(q, random.Random(1000003 * q))
            else: m = q * q - 1; A = np.array(sorted(random.Random(77 * q + rep).sample(range(m), q)), dtype=np.int64)
            ts, g = gaps_all(A, m, q, kind == "bose"); top = ts[np.argsort(-g)[:10]]
            for i, s in enumerate(stats(top, q, m)): rec[i].append(s)
            for i, s in enumerate(stats(ts, q, m)): ref[i].append(s)
        print(kind, q, flush=True)
    out = {}
    for i, name in enumerate(("u_mod_q_plus_1", "v_mod_q_minus_1", "w_rel_order")):
        a, b = np.concatenate(rec[i]), np.concatenate(ref[i]); k = ks_2samp(a, b)
        out[name] = {"ks": float(k.statistic), "p": float(k.pvalue), "record_mean": float(a.mean()), "all_mean": float(b.mean()), "n_record": len(a)}
    return out

if __name__ == "__main__":
    res = {"null": run("null"), "bose": run("bose")}
    res["control_ok"] = all(v["p"] > 0.01 for v in res["null"].values())
    sig = {k: v["p"] < 0.01 / 3 for k, v in res["bose"].items()}
    res["significant_bose"] = sig
    res["verdict"] = "VOID" if not res["control_ok"] else ("STRUCTURE FOUND: " + ", ".join(k for k, s in sig.items() if s) if any(sig.values()) else "NO STRUCTURE")
    print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(H, "b22d_result.json"), "w"), indent=1)
