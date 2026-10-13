"""Batch 17 (PLAN_BATCH17_2026-10-07): mechanism-based filter. For a target PCF (a1, b1) with limit x, partners
b2(n) = kappa * pair(n + s) where pair = product of two linear factors of b1, a2 = alpha n + beta. Vectorised float64
evaluation (depth D and 2D), hash against Mobius images (|coef| <= 8) of x, re-check matches at 120 digits (exact recurrence).
Usage: python b17_mechanism.py targets <json of {name: {"a":[..], "b":[..]}}> <out.json> [--random K]"""
import itertools, json, math, os, sys, time
import numpy as np, sympy as sp
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, "..", "cmf"))
import b10b1_deform as B10
n_ = sp.Symbol("n")
KAPPA = [s * k for k in (1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36) for s in (1, -1)]
ALPHA = range(1, 13); BETA = range(-300, 301); SHIFTS = range(-2, 3); R = 8; DEPTH = 600

def lin_factors(bc):
    c, fl = sp.factor_list(sum(sp.Integer(v) * n_ ** k for k, v in enumerate(bc)), n_); out = []
    for f, e in fl:
        p = sp.Poly(f, n_)
        if p.degree() == 1: out += [tuple(int(v) for v in p.all_coeffs())] * e     # (k, t) for k n + t
    return out

def mobius_table(x):
    tab = {}
    for p, q, r, s in itertools.product(range(-R, R + 1), repeat=4):
        if p * s - q * r == 0 or math.gcd(math.gcd(p, q), math.gcd(r, s)) != 1: continue
        den = r + s * x
        if abs(den) < 1e-9: continue
        v = (p + q * x) / den
        if 1e-6 < abs(v) < 1e6: tab.setdefault(round(v, 8), []).append((p, q, r, s))
    return tab

def cf_vec(alpha, beta_arr, b2coef, depth):
    """values of a(n) = alpha n + beta (vector over beta), fixed b2(n); forward recurrence with renormalisation."""
    m = len(beta_arr); P0, P1 = np.ones(m), beta_arr.astype(float); Q0, Q1 = np.zeros(m), np.ones(m)
    for n in range(1, depth + 1):
        an = alpha * n + beta_arr; bn = sum(c * n ** k for k, c in enumerate(b2coef))
        P0, P1, Q0, Q1 = P1, an * P1 + bn * P0, Q1, an * Q1 + bn * Q0
        sc = np.maximum(np.abs(P1), np.abs(Q1)); sc[sc == 0] = 1; P0, P1, Q0, Q1 = P0 / sc, P1 / sc, Q0 / sc, Q1 / sc
    with np.errstate(divide="ignore", invalid="ignore"): return P1 / Q1

def search(name, a1, b1, x):
    facs = lin_factors(b1); tab = mobius_table(float(x)); hits = []; beta = np.array(list(BETA))
    pairs = {tuple(sorted(pq)) for pq in itertools.combinations(facs, 2)}
    for (k1, t1), (k2, t2) in pairs:
        for s in SHIFTS:
            base = [ (t1 + k1 * s) * (t2 + k2 * s), k1 * (t2 + k2 * s) + k2 * (t1 + k1 * s), k1 * k2 ]   # pair(n + s)
            for kap in KAPPA:
                b2 = [kap * c for c in base]
                if any(sum(c * m ** j for j, c in enumerate(b2)) == 0 for m in range(1, 40)): continue
                for al in ALPHA:
                    y1 = cf_vec(al, beta, b2, DEPTH); y2 = cf_vec(al, beta, b2, 2 * DEPTH)
                    ok = np.isfinite(y1) & (np.abs(y1 - y2) < 1e-11 * np.maximum(1, np.abs(y2)))
                    for i in np.nonzero(ok)[0]:
                        key = round(float(y2[i]), 8)
                        for kk in (key, round(key + 1e-8, 8), round(key - 1e-8, 8)):
                            if kk in tab: hits.append({"a2": [int(beta[i]), al], "b2": b2, "pair": [[k1, t1], [k2, t2]], "s": s, "mob": tab[kk][0]})
    # exact re-check at 120 digits
    conf = []
    for h in hits:
        A = lambda m, h=h: h["a2"][0] + h["a2"][1] * m; Bf = lambda m, h=h: sum(c * m ** j for j, c in enumerate(h["b2"]))
        y, dig = B10.limit_value(A, Bf, need=110, dmax=8000)
        if y is None: continue
        p, q, r, s = h["mob"]; B10.mp.mp.dps = 130; pred = (p + q * x) / (r + s * x)
        d = float(-B10.mp.log10(abs(pred - y) / max(abs(y), 1))) if pred != y else 130
        if d >= 100: h["digits"] = round(d, 1); conf.append(h)
    return {"name": name, "n_float_hits": len(hits), "confirmed": conf}

if __name__ == "__main__":
    T = json.load(open(sys.argv[2])); out = []; t0 = time.time()
    for name, t in T.items():
        if "x_override" in t: B10.mp.mp.dps = 130; x = B10.mp.mpf(t["x_override"])
        else:
            from deep_id import cf                     # no depth cap (slowly converging targets, e.g. C2, C4)
            x, _n = cf(t["a"], t["b"], 120)
        if x is None: out.append({"name": name, "err": "no convergence"}); print(name, "SKIPPED: no convergence", flush=True); continue
        r = search(name, t["a"], t["b"], x); out.append(r)
        print(name, "float hits", r["n_float_hits"], "confirmed", len(r["confirmed"]), [(c["a2"], c["b2"], c["mob"], c.get("digits")) for c in r["confirmed"][:3]], f"{time.time()-t0:.0f}s", flush=True)
    json.dump(out, open(sys.argv[3], "w"), indent=1, default=str)
