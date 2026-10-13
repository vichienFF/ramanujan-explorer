"""Batch 5 J3: identify |C_P|, |C_Q| (500-digit) as Gamma(j/d)/pi/prime-power products, independent basis, PSLQ at 480 digits.
Controls first: planted Gamma products (d=60, 84) and F1 C_P (algebraic)."""
import json, math
from fractions import Fraction
import mpmath as mp
import gamma_basis as GB
import os
DPS = 480
OUT = "bf_runs/track_a/identify500.json"
out = json.load(open(OUT)) if os.path.exists(OUT) else []  # resume: skip names already done
done = {r["name"] for r in out}
def ident(logc, B, maxc=2000):
    r = mp.pslq([logc] + [b for _, b in B], maxcoeff=maxc, maxsteps=10 ** 7)
    return ({"coef_logC": int(r[0]), "terms": {B[i][0]: int(c) for i, c in enumerate(r[1:]) if c}} if r and r[0] else None)
cache = {}
def basis(d):
    if d not in cache: cache[d] = GB.gamma_basis(d, dps=DPS + 20)
    return cache[d]
mp.mp.dps = DPS
for d, planted in [(60, mp.gamma(mp.mpf(7)/60)**2*mp.gamma(mp.mpf(1)/20)/mp.gamma(mp.mpf(11)/60)**3*mp.pi**(-mp.mpf(1)/2)*mp.mpf(3)**(mp.mpf(2)/5)),
                   (84, mp.gamma(mp.mpf(5)/84)*mp.gamma(mp.mpf(1)/12)/(mp.gamma(mp.mpf(25)/84)*mp.pi)*mp.mpf(7)**(mp.mpf(1)/3))]:
    B = basis(d); mp.mp.dps = DPS; print("control planted d", d, "->", "FOUND" if ident(mp.log(planted), B) else "MISSED", flush=True)
for l in open("bf_runs/track_a/cvalues500.jsonl"):
    r = json.loads(l)
    if r["name"] in done: continue
    d = Fraction(r["rho"]).denominator; d = d * 3 // math.gcd(d, 3); B = basis(d); mp.mp.dps = DPS
    rec = {"name": r["name"], "rho": r["rho"], "nbasis": len(B)}
    for lab in ("CPabs", "CQabs"):
        rec[lab] = ident(mp.log(mp.mpf(r[lab])), B) if r.get(lab) else "n/a"
    out.append(rec); print(rec["name"], rec["rho"], "CP:", bool(rec["CPabs"]) and rec["CPabs"] != "n/a", "CQ:", bool(rec["CQabs"]) and rec["CQabs"] != "n/a", flush=True)
    json.dump(out, open(OUT, "w"), indent=0)
print("DONE", flush=True)
