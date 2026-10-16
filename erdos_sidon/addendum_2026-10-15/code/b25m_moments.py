"""Batch 25 M2 (PLAN_BATCH25): b24m_moments.py with the units() bug fixed (all classes when fewer than NT).
Batch 24 M (PLAN_BATCH24): factorial moments of interval counts in dilates of Singer sets.
Z_{t,s} = #{a in S : (t a + s) mod m in [0, l)}, S Singer (|S| = q + 1, m = q^2 + q + 1), l = C q, C in {2, 4, 6}.
For each set: all units t (one per class {+-t}) if q <= 61, else NT random units (seeded); all shifts s (prefix sums).
F_k = mean over (t, s) of (Z)_k = Z (Z-1) ... (Z-k+1), k = 1..6. Reference: hypergeometric factorial moment
H_k = (|S|)_k (l)_k / (m)_k (exact for a uniformly random |S|-subset). R_k = F_k / H_k - 1. Also k = 2 exact Singer identity
check: Var_s Z = q l/m (1 - l/m) for every t, and the spread over t of the per-t F_k.
Null: random subsets of Z_m of size q + 1 (2 per q). One jsonl line per (kind, q, rep, C)."""
import json, math, os, random, sys, time
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import b22c_gaps as B
T0 = time.time(); TLIM = float(os.environ.get("TLIM_H", "7.5")) * 3600; NT = int(os.environ.get("NT", "4000")); K = 6

def ff(z, k):
    out = np.ones_like(z, dtype=float)
    for i in range(k): out *= (z - i)
    return out

def hyper(n, l, m, k):
    v = 1.0
    for i in range(k): v *= (n - i) * (l - i) / (m - i)
    return v

def moments(S, m, q, C, ts):
    n = len(S); l = C * q; Fk = np.zeros(K + 1); per_t = np.zeros((len(ts), K + 1)); var_ok = True
    for j, t in enumerate(ts):
        ind = np.zeros(m, np.int64); ind[(t * S) % m] = 1
        c = np.concatenate([[0], np.cumsum(np.concatenate([ind, ind[:l]]))])
        Z = c[np.arange(m) + l] - c[np.arange(m)]                    # points in [s, s+l) for every s
        for k in range(1, K + 1): per_t[j, k] = ff(Z, k).mean()
        if j < 50 and abs(Z.var() - q * l / m * (1 - l / m)) > 1e-9 * max(1, Z.var()): var_ok = False
    F = per_t.mean(axis=0)
    return {f"F{k}": float(F[k]) for k in range(1, K + 1)} | {f"R{k}": float(F[k] / hyper(n, l, m, k) - 1) for k in range(1, K + 1)} | \
           {f"sd_t_R{k}": float((per_t[:, k] / hyper(n, l, m, k)).std()) for k in range(2, K + 1)} | {"var_identity_ok_first50": var_ok}

def units(m, q, rng):
    allc = [t for t in range(1, m // 2 + 1) if math.gcd(t, m) == 1]          # one per class {+-t}
    if q <= 61 or len(allc) <= NT: return np.array(allc, dtype=np.int64)
    return np.array(sorted(rng.sample(allc, NT)), dtype=np.int64)

if __name__ == "__main__":
    outf = sys.argv[1]; si, sk = map(int, os.environ.get("SHARD", "0/1").split("/")); kinds = os.environ.get("KINDS", "singer,null").split(",")
    lo, hi = (int(x) for x in os.environ.get("QRANGE", "31:211").split(":"))
    done = set()
    if os.path.exists(outf):
        for l in open(outf):
            try: r = json.loads(l); done.add((r["kind"], r["q"], r["rep"], r["C"]))
            except (ValueError, KeyError): pass
    jobs = [(kd, q, rep) for q in B.primes(lo, hi)[::int(os.environ.get("QSTEP", "1"))] for kd in kinds for rep in ((0,) if kd in ("singer", "ap") else tuple(range(1, int(os.environ.get("NULLREPS", "4")) + 1)))]
    for n_, (kd, q, rep) in enumerate(jobs):
        if n_ % sk != si: continue
        if time.time() - T0 > TLIM: print("time limit", flush=True); break
        m = q * q + q + 1
        if kd == "singer": S = B.singer_set(q, random.Random(1000003 * q))[0]
        elif kd == "ap": S = np.array(sorted({(i * m) // (q + 1) for i in range(q + 1)}), dtype=np.int64)     # negative control: equispaced set
        else: S = np.array(sorted(random.Random(91 * q + rep).sample(range(m), q + 1)), dtype=np.int64)
        ts = units(m, q, random.Random(5 * q + rep))
        for C in [int(c) for c in os.environ.get("CS", "2,4,6").split(",")]:
            if (kd, q, rep, C) in done: continue
            tt = time.time(); r = {"kind": kd, "q": q, "rep": rep, "C": C, "n_t": int(len(ts)), **moments(S, m, q, C, ts), "sec": round(time.time() - tt, 1)}
            if kd != "singer": r.pop("var_identity_ok_first50")
            open(outf, "a").write(json.dumps(r) + "\n"); print(json.dumps(r), flush=True)
