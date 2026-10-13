"""Batch 11C (PLAN_BATCH11_2026-10-07): CMF-style trajectories - two factors shifted together,
(t_i, t_j) -> (t_i + k_i m, t_j + k_j m), m in [-60, 60], Mobius relation test of 10B-1 with step 1 (in m), d <= 4.
Positive control: Euler family h1(n) = (n+m+1)(2n+2m+3) (two factors shifted together = index shift), h2(n) = 2n(2n+1) -> ACCEPTED.
Negative control: 90 random two-factor families -> <= 4 accepted."""
import itertools, json, math, os, random, sys, time
import b10b1_deform as B

def fam(a_coeffs, s, facs, i, j, mr):
    a = B.poly_fn(a_coeffs); vals = {}
    for m in mr:
        f2 = [(k, t + k * m) if q in (i, j) else (k, t) for q, (k, t) in enumerate(facs)]
        if any(k != 0 and t % k == 0 and -t // k >= 1 for k, t in f2): continue
        b = lambda n, f2=f2: s * math.prod(k * n + t for k, t in f2)
        x, dig = B.limit_value(a, b)
        if x is not None: vals[m] = x
    return vals

if __name__ == "__main__":
    t0 = time.time(); mr = range(-60, 61); out = {"plan": "PLAN_BATCH11_2026-10-07 (11C)"}
    vals = {}
    for m in mr:
        if any((n + m + 1) == 0 or (2 * n + 2 * m + 3) == 0 for n in range(1, 400)): continue
        a = lambda n, m=m: (n + m + 1) * (2 * n + 2 * m + 3) + 2 * (n + 1) * (2 * n + 3)
        b = lambda n, m=m: -(n + m + 1) * (2 * n + 2 * m + 3) * 2 * n * (2 * n + 1)
        x, dig = B.limit_value(a, b)
        if x is not None: vals[m] = x
    out["positive_control"] = B.find_relation(vals); print("positive control:", out["positive_control"], flush=True)
    if sys.argv[1:] == ["control"]: sys.exit()
    C = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bf_runs", "track_a", "irreducible15.json")))
    out["candidates"], out["negative"] = [], []; rng = random.Random(20261014)
    for ci, c in enumerate(C):
        s, facs = B.factor_b(c["b"])
        for i, j in itertools.combinations(range(4), 2):
            r = B.find_relation(fam(c["a"], s, facs, i, j, mr)); r.update(C=ci, pair=[i, j]); out["candidates"].append(r)
            print("C", ci, (i, j), r.get("status"), r.get("d"), f"{time.time()-t0:.0f}s", flush=True)
        rf = [(rng.randint(1, 6), rng.randint(-10, 10)) for _ in range(4)]; rs = rng.choice([-1, 1]) * 4
        for i, j in itertools.combinations(range(4), 2):
            r = B.find_relation(fam(c["a"], rs, rf, i, j, mr)); r.update(C=ci, pair=[i, j]); out["negative"].append(r)
    acc = sum(r.get("status") == "ACCEPTED" for r in out["candidates"]); neg = sum(r.get("status") == "ACCEPTED" for r in out["negative"])
    out["summary"] = {"accepted": acc, "negative_accepted": neg, "control_ok": out["positive_control"].get("status") == "ACCEPTED",
                      "success": bool(acc >= 1 and neg <= 4 and out["positive_control"].get("status") == "ACCEPTED"), "sec": round(time.time() - t0)}
    print(json.dumps(out["summary"])); json.dump(out, open("b11c_result.json", "w"), indent=1, default=str)
