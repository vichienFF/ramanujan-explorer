# rama-v3-large: Conjecture V3 at large q (m prime): V/((m-2)E) and per-lambda 3rd factorial moment errors
# X_lam = sum_mu (|S cap (lam S + mu)|)_3 vs random-set value m (n)_3^2/(m)_3, for NL random non-multiplier lambda.
# Checkpoint per q; no new q after 10 h.
import os, sys, json, time, base64, random, math
T0 = time.time(); W = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
MODS = json.loads(base64.b64decode("__MODS__").decode())
for n_, src in MODS.items(): open(os.path.join(W, n_), "w").write(src)
sys.path.insert(0, W)
import numpy as np, b22c_gaps as B
from c3r_fast import singer_fast, ratio_counts, inv_table
QLO, QHI, NL = int(os.environ.get("QLO", "1400")), int(os.environ.get("QHI", "3000")), int(os.environ.get("NL", "1500"))
OUT = os.path.join(W, "v3_large.jsonl"); done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)["q"])
def isprime(x): return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))
qs = [q for q in B.primes(QLO, QHI) if isprime(q * q + q + 1)]
print("q list", qs, flush=True)
for q in qs:
    if q in done: continue
    if time.time() - T0 > 10 * 3600: print("time guard", flush=True); break
    t0 = time.time(); S, m = singer_fast(q, random.Random(1000003 * q)); n = len(S)
    N = ratio_counts(S, m, inv_table(m)).astype(float); Nr = N[2:]; E = n * (n - 1) * (n - 2) / (m - 2)
    V = float(((Nr - E) ** 2).sum()); mod3 = float((Nr % 3 == 0).mean())
    mult = {1, q % m, (q * q) % m}; rng = random.Random(7 * q); lams = []
    while len(lams) < NL:
        l = rng.randrange(2, m)
        if l not in mult: lams.append(l)
    pred = m * (n * (n - 1) * (n - 2)) ** 2 / (m * (m - 1) * (m - 2)); errs = []
    for lam in lams:
        I = np.bincount(((S[:, None] - (lam * S)[None, :]) % m).ravel(), minlength=m).astype(float)
        errs.append(float((I * (I - 1) * (I - 2)).sum() - pred))
    e = np.array(errs)
    r = {"q": q, "m": m, "V_over_mE": V / ((m - 2) * E), "frac_mod3": mod3, "NL": NL, "X_pred": pred,
         "err_mean": float(e.mean()), "err_sd": float(e.std()), "err_mean_over_q": float(e.mean() / q), "err_sd_over_q": float(e.std() / q),
         "sec": round(time.time() - t0, 1)}
    open(OUT, "a").write(json.dumps(r) + "\n"); print(json.dumps(r), flush=True)
for n_ in MODS: os.remove(os.path.join(W, n_))
print("finished", round((time.time() - T0) / 60, 1), "min", flush=True)
