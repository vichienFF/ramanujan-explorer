"""Amendment 10B-1 (f44cb80): step k_i, m in [-80, 80], second positive control with k = 2.
Based on Batch 10B (PLAN_BATCH10B_2026-10-07): deform the 15 candidates along t_i -> t_i + m and test for a Mobius-type relation
A(m) + B(m) x(m) + C(m) x(m+1) + D(m) x(m) x(m+1) = 0 with polynomials of degree d <= 4 in m.
Controls: Euler-type family (must be accepted); 15 random non-FR PCFs, 60 families (<= 3 accepted)."""
import json, math, os, random, sys, time
import mpmath as mp
import sympy as sp

H = os.path.dirname(os.path.abspath(__file__)); DPS = 90
n_ = sp.Symbol("n")

def limit_value(a, b, need=80, dmax=6000):
    """exact integer recurrence; returns (x, digits) with digits estimated from depth d vs 2d."""
    def conv(depth):
        p0, p1, q0, q1 = 1, a(0), 0, 1
        for n in range(1, depth + 1):
            an, bn = a(n), b(n)
            p0, p1, q0, q1 = p1, an * p1 + bn * p0, q1, an * q1 + bn * q0
        return p1, q1
    depth = 500
    while depth <= dmax:
        p, q = conv(depth); p2, q2 = conv(2 * depth)
        if q == 0 or q2 == 0: return None, 0
        mp.mp.dps = DPS + 20; x1, x2 = mp.mpf(p) / q, mp.mpf(p2) / q2
        dig = int(-mp.log10(abs(x1 - x2) / max(abs(x2), mp.mpf(1)))) if x1 != x2 else DPS
        if dig >= need: return x2, min(dig, DPS)
        depth *= 2
    return None, 0

def poly_fn(coeffs):           # coeffs low -> high
    return lambda n: sum(c * n ** i for i, c in enumerate(coeffs))

def family_values(a_coeffs, s, facs, i, mrange):
    a = poly_fn(a_coeffs); vals = {}
    for m in mrange:
        f2 = [(k, t + m) if j == i else (k, t) for j, (k, t) in enumerate(facs)]
        if any(t % k == 0 and -t // k >= 1 for k, t in f2 if k > 0) or any(k < 0 and t % k == 0 and -t // k >= 1 for k, t in f2):
            continue                                               # b(n) = 0 for some n >= 1 -> terminating
        b = lambda n, f2=f2: s * math.prod(k * n + t for k, t in f2)
        x, dig = limit_value(a, b)
        if x is not None: vals[m] = x
    return vals

def find_relation(vals, dmax=4, step=1):
    ms = sorted(m for m in vals if m + step in vals)
    for d in range(1, dmax + 1):
        nu = 4 * (d + 1); fit, held = ms[:nu + 8], ms[nu + 8:]
        if len(held) < 10: return {"status": "too_few_pairs", "pairs": len(ms)}
        mp.mp.dps = DPS
        rows = []
        for m in fit:
            x, y = vals[m], vals[m + step]
            rows.append([mp.mpf(m) ** j * f for f in (1, x, y, x * y) for j in range(d + 1)])
        M = mp.matrix(rows); U, S, V = mp.svd_r(M)
        sv = sorted([abs(S[i]) for i in range(len(S))], reverse=True)
        if not (sv[-1] < mp.mpf(10) ** -60 * sv[0] and sv[-2] > mp.mpf(10) ** -20 * sv[0]): continue
        v = [V[V.rows - 1, j] for j in range(V.cols)]           # right singular vector of the smallest singular value
        def coef(blk, m): return sum(v[blk * (d + 1) + j] * mp.mpf(m) ** j for j in range(d + 1))
        worst = mp.inf
        for m in held:
            A, B, C, D = (coef(k, m) for k in range(4)); x = vals[m]; den = C + D * x
            if den == 0: continue
            pred = -(A + B * x) / den; err = abs(pred - vals[m + step]) / max(abs(vals[m + step]), mp.mpf(1))
            worst = min(worst, -mp.log10(err) if err > 0 else DPS)
        if worst >= 40: return {"status": "ACCEPTED", "d": d, "heldout_digits": float(worst), "n_fit": len(fit), "n_held": len(held)}
    return {"status": "none"}

def factor_b(bc):
    poly = sp.Poly(sum(c * n_ ** i for i, c in enumerate(bc)), n_); s, fl = sp.factor_list(poly.as_expr())
    facs = []
    for f, e in fl:
        p = sp.Poly(f, n_)
        if p.degree() != 1: return None
        k, t = [int(c) for c in p.all_coeffs()]; facs += [(k, t)] * e
    return int(s), facs

if __name__ == "__main__":
    t0 = time.time(); out = {"plan": "PLAN_BATCH10B_2026-10-07", "positive_control": None, "candidates": [], "negative": []}
    mr = range(-80, 81)
    # positive control: Euler family h1 = (n+1)(n+m+2), h2 = n(2n+1); a(n) = h1(n) + h2(n+1), b(n) = -h1(n) h2(n)
    vals = {}
    for m in mr:
        if m + 2 <= -1: continue
        a = lambda n, m=m: (n + 1) * (n + m + 2) + (n + 1) * (2 * n + 3)
        b = lambda n, m=m: -(n + 1) * (n + m + 2) * n * (2 * n + 1)
        x, dig = limit_value(a, b)
        if x is not None: vals[m] = x
    out["positive_control"] = find_relation(vals); print("positive control:", out["positive_control"], flush=True)
    vals = {}
    for m in mr:                                                   # control 2: factor (2n + m + 3), step 2
        if any((2 * n + m + 3) == 0 for n in range(1, 200)): continue
        a = lambda n, m=m: (n + 1) * (2 * n + m + 3) + (n + 1) * (2 * n + 3)
        b = lambda n, m=m: -(n + 1) * (2 * n + m + 3) * n * (2 * n + 1)
        x, dig = limit_value(a, b)
        if x is not None: vals[m] = x
    out["positive_control_2"] = find_relation(vals, step=2); print("positive control 2 (step 2):", out["positive_control_2"], flush=True)
    if sys.argv[1:] == ["control"]: sys.exit()
    C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
    for ci, c in enumerate(C):
        fb = factor_b(c["b"])
        if fb is None: out["candidates"].append({"C": ci, "status": "b not product of linear factors"}); continue
        s, facs = fb
        for i in range(len(facs)):
            r = find_relation(family_values(c["a"], s, facs, i, mr), step=abs(facs[i][0])); r.update(C=ci, dir=i, fac=facs[i])
            out["candidates"].append(r); print("C", ci, "dir", i, r, f"{time.time()-t0:.0f}s", flush=True)
    rng = random.Random(20261012)
    for ci, c in enumerate(C):                                     # negative control: same a(n), random b factors
        facs = [(rng.randint(1, 6), rng.randint(-10, 10)) for _ in range(4)]; s = rng.choice([-1, 1]) * 4
        for i in range(4):
            r = find_relation(family_values(c["a"], s, facs, i, mr), step=abs(facs[i][0])); r.update(C=ci, dir=i, fac=facs[i])
            out["negative"].append(r); print("NEG", ci, i, r["status"], flush=True)
    acc = sum(r.get("status") == "ACCEPTED" for r in out["candidates"]); neg = sum(r.get("status") == "ACCEPTED" for r in out["negative"])
    out["summary"] = {"accepted_candidates": acc, "accepted_negative": neg, "positive_control_ok": out["positive_control"].get("status") == "ACCEPTED" and out["positive_control_2"].get("status") == "ACCEPTED",
                      "success": bool(acc >= 1 and neg <= 3 and out["positive_control"].get("status") == "ACCEPTED" and out["positive_control_2"].get("status") == "ACCEPTED"), "sec": round(time.time() - t0)}
    print(json.dumps(out["summary"])); json.dump(out, open(os.path.join(H, "b10b1_result.json"), "w"), indent=1, default=str)
