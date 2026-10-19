# rama-pp-v3-SHARD: Conjecture V3 for PRIME-POWER q (Singer sets built in F_{p^{3k}}), any m (good rho only).
import os, sys, json, time, base64, random, math
T0 = time.time(); W = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
MODS = json.loads(base64.b64decode("__MODS__").decode())
for n_, src in MODS.items(): open(os.path.join(W, n_), "w").write(src)
sys.path.insert(0, W)
import numpy as np
from ppsinger import singer_pp
QS = [int(x) for x in os.environ.get("QS", "__QS__").split(",")]
OUT = os.path.join(W, "pp_v3.jsonl"); done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)["q"])
def ppk(q):
    for p in range(2, q + 1):
        if q % p == 0:
            k = 0; t = q
            while t % p == 0: t //= p; k += 1
            return (p, k) if t == 1 else None
for q in QS:
    if q in done: continue
    if time.time() - T0 > 10 * 3600: print("time guard", flush=True); break
    t0 = time.time(); p, k = ppk(q); S, m, _ = singer_pp(p, k, random.Random(1000003 * q)); n = len(S)
    inv = np.zeros(m, np.int64); units = np.array([math.gcd(x, m) == 1 for x in range(m)])
    for x in np.nonzero(units)[0]: inv[x] = pow(int(x), -1, m)
    N = np.zeros(m, np.int64)
    for i in range(n):
        d = np.delete((S - S[i]) % m, i); du = d[units[d]]
        r = (d[None, :] * inv[du][:, None]) % m
        N += np.bincount(r.ravel(), minlength=m); N[1] -= len(du)
    good = units & np.roll(units, 1); good[0] = good[1] = False        # rho and rho-1 units
    Ng = N[good].astype(float); E = Ng.mean(); V = ((Ng - E) ** 2).sum()
    rec = {"q": q, "p": p, "k": k, "m": m, "n": n, "n_good": int(good.sum()), "E": E, "V_over_mE": V / (good.sum() * E),
           "frac_mod3": float((Ng % 3 == 0).mean()), "sec": round(time.time() - t0, 1)}
    open(OUT, "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
for n_ in MODS: os.remove(os.path.join(W, n_))
print("finished", round((time.time() - T0) / 60, 1), "min", flush=True)
