"""Batch 23B (PLAN_BATCH23): conditional Route C follow-up. env BRANCH = struct | none.
struct: env STAT in {u, v, w}, DECILE (0..9 = enriched decile from Amendment 22-5); every 20th prime in (2003, 6000]; share of
        the top-10 multipliers in that decile (Bose) vs random sets (3 per q).
none:   3-term relations e1 L1 + e2 L2 + e3 L3 = 0 mod m, distinct elements, e in [-6, 6]^3 without zeros; Bose sets for every
        5th prime in [101, 401] and 3 random sets of the same size per q; counts per set.
Checkpoint: one jsonl line per (q, kind, rep)."""
import json, math, os, random, sys, time
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import b22c_gaps as B, b22d_multipliers as D
T0 = time.time(); TLIM = float(os.environ.get("TLIM_H", "7.5")) * 3600; E = 6

def sets_for(q):
    out = [("bose", 0, *B.bose_set(q, random.Random(1000003 * q)))]
    m = q * q - 1
    for rep in (1, 2, 3): out.append(("null", rep, np.array(sorted(random.Random(77 * q + rep).sample(range(m), q)), dtype=np.int64), m))
    return out

def relations(L, m):
    """number of (i<j<k distinct, e1,e2,e3 in [-E,E]\\{0}) with e1 L_i + e2 L_j + e3 L_k = 0 mod m (unordered triples counted once
    per exponent vector up to global sign)."""
    n = len(L); ev = np.array([e for e in range(-E, E + 1) if e], dtype=np.int64)
    third = {}                                         # value -> list of indices k  (for e3 * L_k)
    vals = (ev[:, None] * L[None, :]) % m             # shape (12, n)
    keys = vals.ravel(); idx = np.tile(np.arange(n), len(ev)); order = np.argsort(keys, kind="stable"); ks = keys[order]; ix = idx[order]
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = (ev[:, None] * L[i] + ev[None, :] * L[j]) % m          # 12 x 12
            need = (-s.ravel()) % m
            lo = np.searchsorted(ks, need, "left"); hi = np.searchsorted(ks, need, "right")
            for a, b in zip(lo, hi):
                if b > a: total += int(np.sum((ix[a:b] > j)))           # k > j: each unordered triple once per (e1,e2) and e3
    return total // 2                                  # global sign (e -> -e) counted twice

if __name__ == "__main__":
    outf = sys.argv[1]; br = os.environ["BRANCH"]; si, sk = map(int, os.environ.get("SHARD", "0/1").split("/"))
    done = set()
    if os.path.exists(outf):
        for l in open(outf):
            try: r = json.loads(l); done.add((r["q"], r["kind"], r["rep"]))
            except (ValueError, KeyError): pass
    qs = B.primes(2004, 6000)[::20] if br == "struct" else B.primes(101, 401)[::5]
    for n_, q in enumerate(qs):
        if n_ % sk != si: continue
        for kind, rep, A, m in sets_for(q):
            if (q, kind, rep) in done: continue
            if time.time() - T0 > TLIM: print("time limit", flush=True); sys.exit(0)
            t = time.time()
            if br == "struct":
                ts, g = D.gaps_all(A, m, q, kind == "bose"); st = {"u": 0, "v": 1, "w": 2}[os.environ["STAT"]]
                X = D.stats(ts, q, m)[st]; qd = np.quantile(X, np.linspace(0, 1, 11)); dec = int(os.environ["DECILE"])
                inR = (X >= qd[dec]) & (X <= qd[dec + 1]); top = np.argsort(-g)[:10]
                r = {"q": q, "kind": kind, "rep": rep, "share_top10_in_R": float(inR[top].mean()), "share_all_in_R": float(inR.mean())}
            else:
                L = np.sort(A) if kind == "bose" else A
                r = {"q": q, "kind": kind, "rep": rep, "relations_k3": relations(L, m)}
            r["sec"] = round(time.time() - t, 1); open(outf, "a").write(json.dumps(r) + "\n"); print(json.dumps(r), flush=True)
