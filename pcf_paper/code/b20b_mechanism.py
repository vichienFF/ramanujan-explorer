"""Batch 20B (PLAN_BATCH20_2026-10-12): b18_mechanism + Amendment 18-2 evaluator, capped target depth (TGT_DMAX) and a global
deadline checked inside the float and re-check loops (5-point timer standard). Batch 18 (PLAN_BATCH18_2026-10-07) generalised from Batch 17 (PLAN_BATCH17_2026-10-07): mechanism-based filter. For a target PCF (a1, b1) with limit x, partners
b2(n) = kappa * pair(n + s) where pair = product of two linear factors of b1, a2 = alpha n + beta. Vectorised float64
evaluation (depth D and 2D), hash against Mobius images (|coef| <= 8) of x, re-check matches at 120 digits (exact recurrence).
Usage: python b17_mechanism.py targets <json of {name: {"a":[..], "b":[..]}}> <out.json> [--random K]"""
import itertools, json, math, os, sys, time
import numpy as np, sympy as sp
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, "..", "cmf"))
import b10b1_deform as B10
n_ = sp.Symbol("n")
CFG = {"wide": dict(K=(1,2,3,4,6,8,9,12,16,18,24,25,27,32,36,48,49,50,64,72,81,100,144), A=24, B=1000, S=2, CHECK=160),
       "narrow": dict(K=(1,2,3,4,6,9), A=6, B=60, S=1, CHECK=60),
       "b17": dict(K=(1,2,3,4,6,8,9,12,16,18,24,36), A=12, B=300, S=2, CHECK=120)}[os.environ.get("CFG", "b17")]
KAPPA = [s * k for k in CFG["K"] for s in (1, -1)]
ALPHA = range(1, CFG["A"] + 1); BETA = range(-CFG["B"], CFG["B"] + 1); SHIFTS = range(-CFG["S"], CFG["S"] + 1); R = 8; DEPTH = 600

DEADLINE = time.time() + float(os.environ.get("TLIM_H", "1e9")) * 3600

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

def limit_mp(a, b, need, dmax):
    """Amendment 18-2: mpf forward recurrence at need+30 digits (B10.limit_value worked at 110 digits, so any need > 110
    could never be met and every partner was logged slow). Value at depths 1000, 2000, 4000, ...; accepted when two
    consecutive checkpoints agree to need digits, else (None, digits reached)."""
    mp = B10.mp; mp.mp.dps = need + 30; p0, p1, q0, q1 = mp.mpf(1), mp.mpf(a(0)), mp.mpf(0), mp.mpf(1)
    nxt, prev, dig = 1000, None, 0
    for n in range(1, dmax + 1):
        an, bn = a(n), b(n); p0, p1, q0, q1 = p1, an * p1 + bn * p0, q1, an * q1 + bn * q0
        if n % 64 == 0:
            sc = max(abs(p1), abs(q1))
            if sc: p0, p1, q0, q1 = p0 / sc, p1 / sc, q0 / sc, q1 / sc
        if n == nxt:
            if q1 == 0: return None, 0
            v = p1 / q1
            if prev is not None:
                dig = need + 30 if v == prev else int(-mp.log10(abs(v - prev) / max(abs(v), mp.mpf(1))))
                if dig >= need: return v, dig
            prev, nxt = v, 2 * nxt
    return None, dig

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
                    if time.time() > DEADLINE: return {"name": name, "deadline": True}
                    y1 = cf_vec(al, beta, b2, DEPTH); y2 = cf_vec(al, beta, b2, 2 * DEPTH)
                    ok = np.isfinite(y1) & (np.abs(y1 - y2) < 1e-11 * np.maximum(1, np.abs(y2)))
                    for i in np.nonzero(ok)[0]:
                        key = round(float(y2[i]), 8)
                        for kk in (key, round(key + 1e-8, 8), round(key - 1e-8, 8)):
                            if kk in tab: hits.append({"a2": [int(beta[i]), al], "b2": b2, "pair": [[k1, t1], [k2, t2]], "s": s, "mob": tab[kk][0]})
    # exact re-check at 120 digits
    conf = []; slow = []; t_rc = time.time(); budget = float(os.environ.get("BUDGET_S", "1e12")); maxrc = int(os.environ.get("MAX_RECHECK", "1000000"))
    if len(hits) > maxrc: hits = hits[:maxrc]
    for h in hits:
        if time.time() > DEADLINE: return {"name": name, "deadline": True, "hits": hits}
        if time.time() - t_rc > budget: return {"name": name, "n_float_hits": len(hits), "confirmed": conf, "slow_partners": len(slow), "budget": True, "hits": hits}
        A = lambda m, h=h: h["a2"][0] + h["a2"][1] * m; Bf = lambda m, h=h: sum(c * m ** j for j, c in enumerate(h["b2"]))
        need = CFG["CHECK"]                         # capped evaluator (Kaggle lesson #2): slow partners are logged, not waited for
        A_ = lambda m, h=h: h["a2"][0] + h["a2"][1] * m; B_ = lambda m, h=h: sum(c * m ** j for j, c in enumerate(h["b2"]))
        y, _dig = limit_mp(A_, B_, need, int(os.environ.get("RC_DMAX", "64000")))   # Amendment 18-2: own precision
        if y is None: h["slow_partner"] = True; h["slow_digits"] = _dig; slow.append(h); continue
        p, q, r, s = h["mob"]; B10.mp.mp.dps = need + 10; pred = (p + q * x) / (r + s * x)
        d = float(-B10.mp.log10(abs(pred - y) / max(abs(y), 1))) if pred != y else need
        if d >= need - 15: h["digits"] = round(d, 1); conf.append(h)
    return {"name": name, "n_float_hits": len(hits), "confirmed": conf, "slow_partners": len(slow), "hits": hits}

if __name__ == "__main__":
    T = json.load(open(sys.argv[2])); out = []; t0 = time.time(); outf = sys.argv[3]
    shard = os.environ.get("SHARD", "0/1"); si, sk = map(int, shard.split("/")); TL = float(os.environ.get("TLIM_H", "1e9"))
    done = set()
    if outf.endswith(".jsonl") and os.path.exists(outf):
        for l in open(outf):
            try: done.add(json.loads(l)["name"])
            except (ValueError, KeyError): pass
    for idx, (name, t) in enumerate(T.items()):
        if idx % sk != si or name in done: continue
        if (time.time() - t0) / 3600 > TL: print("time limit", flush=True); break
        if "x_override" in t: B10.mp.mp.dps = 130; x = B10.mp.mpf(t["x_override"])
        elif "x_from" in t:                              # mismatch control: limit of ANOTHER PCF, factor pairs of this one
            A_ = lambda m, c=t["x_from"]["a"]: sum(v * m ** j for j, v in enumerate(c)); B_ = lambda m, c=t["x_from"]["b"]: sum(v * m ** j for j, v in enumerate(c))
            x, _d = limit_mp(A_, B_, int(os.environ.get("XDIG", CFG["CHECK"] + 20)), int(os.environ.get("TGT_DMAX", "64000")))
        else:                                              # capped target depth: slow targets are logged, not waited for
            A_ = lambda m, c=t["a"]: sum(v * m ** j for j, v in enumerate(c)); B_ = lambda m, c=t["b"]: sum(v * m ** j for j, v in enumerate(c))
            x, _d = limit_mp(A_, B_, int(os.environ.get("XDIG", CFG["CHECK"] + 20)), int(os.environ.get("TGT_DMAX", "64000")))
            if x is not None: B10.mp.mp.dps = int(os.environ.get("XDIG", CFG["CHECK"] + 20)) + 30
        if x is None:
            r = {"name": name, "err": "slow target"}; out.append(r); print(name, "SKIPPED: slow target", flush=True)
            if outf.endswith(".jsonl"): open(outf, "a").write(json.dumps(r) + chr(10))
            continue
        if (time.time() - t0) / 3600 > TL: print("time limit", flush=True); break
        r = search(name, t["a"], t["b"], x); out.append(r)
        if r.get("deadline"): print(name, "deadline reached - not recorded, next round redoes it", flush=True); break
        if outf.endswith(".jsonl"): open(outf, "a").write(json.dumps(r, default=str) + chr(10))
        print(name, "float hits", r["n_float_hits"], "confirmed", len(r["confirmed"]), [(c["a2"], c["b2"], c["mob"], c.get("digits")) for c in r["confirmed"][:3]], f"{time.time()-t0:.0f}s", flush=True)
    if not outf.endswith(".jsonl"): json.dump(out, open(outf, "w"), indent=1, default=str)
