# rama-v4-identity: k=3,4 dilate-intersection moments over ALL unit lambda (exact identity: sum N(rho)^2 = sum (I)_3, and
# the k=4 analogue sum N(rho1,rho2)^2 = sum (I)_4). Compares non-multiplier totals with the random-set expectation.
import os, sys, json, time, base64, random, math
T0 = time.time(); W = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
MODS = json.loads(base64.b64decode("__MODS__").decode())
for n_, src in MODS.items(): open(os.path.join(W, n_), "w").write(src)
sys.path.insert(0, W)
import numpy as np, b22c_gaps as B
from c3r_fast import singer_fast
QLO, QHI = int(os.environ.get("QLO", "40")), int(os.environ.get("QHI", "420"))
OUT = os.path.join(W, "v4_identity.jsonl"); done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)["q"])
def isprime(x): return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))
def ff(n, k):
    v = 1
    for i in range(k): v *= (n - i)
    return v
for q in [q for q in B.primes(QLO, QHI) if isprime(q * q + q + 1)]:
    if q in done: continue
    if time.time() - T0 > 10 * 3600: print("time guard", flush=True); break
    t0 = time.time(); S, m = singer_fast(q, random.Random(1000003 * q)); n = len(S)
    mult = {1, q % m, (q * q) % m}; X = {3: 0.0, 4: 0.0}; Xm = {3: 0.0, 4: 0.0}
    for lam in range(1, m):
        I = np.bincount(((S[:, None] - (lam * S)[None, :]) % m).ravel(), minlength=m).astype(np.int64)
        for k in (3, 4):
            v = float(np.sum(I * (I - 1) * (I - 2) * (I - 3 if k == 4 else 1)))
            (Xm if lam in mult else X)[k] += v
    rec = {"q": q, "m": m, "sec": 0}
    for k in (3, 4):
        exp_nonmult = (m - 1 - 3) * m * ff(n, k) ** 2 / ff(m, k)      # random-set expectation per lambda
        rec[f"X{k}_nonmult"] = X[k]; rec[f"X{k}_mult"] = Xm[k]; rec[f"exp{k}"] = exp_nonmult
        rec[f"ratio{k}"] = X[k] / exp_nonmult; rec[f"dev{k}_over_mult"] = (X[k] - exp_nonmult) / Xm[k]
    rec["sec"] = round(time.time() - t0, 1)
    open(OUT, "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec), flush=True)
for n_ in MODS: os.remove(os.path.join(W, n_))
print("finished", round((time.time() - T0) / 60, 1), "min", flush=True)
