"""Test whether |C_P|, |C_Q| of the 18 cases (F1, G1, G2, C0..C14) are products of Gamma(k/d), pi and rational powers of rationals (independent basis, 150 digits)"""
import json
from fractions import Fraction
import mpmath as mp
from gamma_basis import gamma_basis
mp.mp.dps = 160
cache, out = {}, []
for l in open("bf_runs/track_a/cvalues.jsonl"):
    r = json.loads(l); d = Fraction(r["rho"]).denominator
    d = d * 3 // __import__("math").gcd(d, 3)
    if d not in cache: cache[d] = gamma_basis(d)
    B = cache[d]; rec = {"name": r["name"], "rho": r["rho"], "nbasis": len(B)}
    for lab in ("CPabs", "CQabs"):
        if not r[lab]: rec[lab] = "n/a"; continue
        mp.mp.dps = 150
        rel = mp.pslq([mp.log(mp.mpf(r[lab]))] + [b for _, b in B], maxcoeff=500, maxsteps=10**6)
        rec[lab] = {"coef_logC": int(rel[0]), "terms": {B[i][0]: int(c) for i, c in enumerate(rel[1:]) if c}} if rel and rel[0] else None
    out.append(rec); print(rec, flush=True)
json.dump(out, open("bf_runs/track_a/cvalues_identified.json", "w"), indent=0)
