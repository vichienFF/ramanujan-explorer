# rama-b28-ck-SHARD: Batch 28 (PLAN_BATCH28.md, frozen, sha in lane_b/LEDGER.md). Checkpoint per (kind, q); stop new q after 10 h.
import os, sys, json, time, base64, random
T0 = time.time(); W = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
MODS = json.loads(base64.b64decode("__MODS__").decode())
for n, src in MODS.items(): open(os.path.join(W, n), "w").write(src)
sys.path.insert(0, W)
import numpy as np, b22c_gaps as B, b28_moments as F, ck_pred as P
def singer_fast(q, rng):   # = c3r_fast.singer_fast: same set as B.singer_set, only m steps
    c = B.primitive_mod(q, 3, rng); m = q * q + q + 1
    e0, e1, e2, res = 1, 0, 0, []
    for a in range(m):
        if e2 == 0: res.append(a)
        e0, e1, e2 = (c[0] * e2) % q, (e0 + c[1] * e2) % q, (e1 + c[2] * e2) % q
    return np.array(res, dtype=np.int64), m
SHARD, NSH = __SHARD__, __NSH__
NT = int(os.environ.get("NT", "3000")); QLO, QHI = int(os.environ.get("QLO", "607")), int(os.environ.get("QHI", "1499"))
OUT = os.path.join(W, "b28_shard%d.jsonl" % SHARD)
done = set()
if os.path.exists(OUT):
    for l in open(OUT): r = json.loads(l); done.add((r["kind"], r["q"]))
qs = B.primes(QLO, QHI + 1)[::2]
jobs = [("singer", q) for q in qs] + [("null", q) for q in qs[::8]]
jobs = [j for i, j in enumerate(jobs) if i % NSH == SHARD]
import math
for kind, q in jobs:
    if (kind, q) in done: continue
    if time.time() - T0 > 10 * 3600: print("time guard: stop new q", flush=True); break
    m = q * q + q + 1; tt = time.time()
    S = singer_fast(q, random.Random(1000003 * q))[0] if kind == "singer" else np.array(sorted(random.Random(91 * q + 1).sample(range(m), q + 1)), dtype=np.int64)
    allc = [t for t in range(1, m // 2 + 1) if math.gcd(t, m) == 1]
    ts = np.array(sorted(random.Random(5 * q).sample(allc, min(NT, len(allc)))), dtype=np.int64)
    r = {"kind": kind, "q": q, "C": 2, "n_t": int(len(ts)), **F.moments(S, m, q, 2, ts)}
    r |= {f"pred{k}": P.pred(k, 2 * q) for k in range(3, 7)}; r["sec"] = round(time.time() - tt, 1)
    open(OUT, "a").write(json.dumps(r) + "\n"); print(kind, q, round(q * r["R4"], 3), r["sec"], flush=True)
for n in MODS: os.remove(os.path.join(W, n))
print("finished", round((time.time() - T0) / 60, 1), "min", flush=True)
