"""Identification-and-proof pipeline for a polynomial continued fraction x = a(0) + b(1)/(a(1) + b(2)/(a(2) + ...)).
Stages run from cheap to expensive and stop at the first identification unless --all is given (lessons of Batches 1-18):
  1 basic      : limit to DIG digits; rational / quadratic; Mobius (|coef| <= 1e4) of ~40 standard constants
  2 structure  : Ben David et al. Conjecture 1.3 family; hypergeometric (Euler-type) solution of the recurrence
  3 mechanism  : "wrapped degree-(1,2)" filter of Batch 17/18 (partner b = kappa x pair of linear factors of b)
  4 low-degree : brute-force Mobius search over low-degree PCFs - too heavy here; prints the Kaggle command (Batches 12-15)
  5 library    : optional (--deep) 21,984-constant PSLQ library of cmf/deep_id.py
  6 operator   : not run here (SageMath: sage_factor.sage, sage_monodromy.sage, identify500.py)
  7 proof      : for every partner found in stage 3, exact coboundary search of Batch 16 -> polynomial identity = proof
Usage: python identify_pipeline.py "a0,a1,a2" "b0,b1,b2,b3,b4" [--all] [--deep] [--out report.json]
       python identify_pipeline.py --selftest    (Apery zeta(3) must be found in stage 1, C0 in stages 3 and 7, a random
                                                   real must stay unidentified)"""
import json, os, sys, time
import mpmath as mp
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H, os.path.join(H, "..", "cmf")]
from deep_id import cf

DIG = 120
STD = {"pi": "pi", "e": "e", "zeta3": "zeta(3)", "zeta5": "zeta(5)", "catalan": "catalan", "log2": "log(2)", "log3": "log(3)",
       "log5": "log(5)", "sqrt2": "sqrt(2)", "sqrt3": "sqrt(3)", "sqrt5": "sqrt(5)", "phi": "phi", "euler": "euler", "pi2": "pi**2",
       "pi3": "pi**3", "pi4": "pi**4", "pi_sqrt3": "pi*sqrt(3)", "pi_sqrt2": "pi*sqrt(2)", "pi_log2": "pi*log(2)", "log2sq": "log(2)**2",
       "zeta3_pi2": "zeta(3)/pi**2", "catalan_pi": "catalan/pi", "L2chi3": "(zeta(2, mpf(1)/3) - zeta(2, mpf(2)/3))/9",
       "gamma13_3_pi": "gamma(mpf(1)/3)**3/pi", "gamma14_2": "gamma(mpf(1)/4)**2/sqrt(pi)", "lemniscate": "gamma(mpf(1)/4)**2/(2*sqrt(2*pi))",
       "gauss": "1/agm(1, sqrt(2))", "e_pi": "exp(pi)", "log_phi": "log(phi)", "log1p_sqrt2": "log(1+sqrt(2))", "li2_13": "polylog(2, mpf(1)/3)",
       "li3_12": "polylog(3, mpf(1)/2)", "khinchin": "khinchin", "sqrt_pi": "sqrt(pi)", "pi_inv": "1/pi", "e2": "exp(2)", "zeta7": "zeta(7)"}

def stage1(x):
    mp.mp.dps = DIG
    if mp.pslq([1, x], maxcoeff=10 ** 12, maxsteps=10 ** 5): return {"rational": [int(v) for v in mp.pslq([1, x], maxcoeff=10 ** 12, maxsteps=10 ** 5)]}
    r = mp.pslq([1, x, x * x], maxcoeff=10 ** 8, maxsteps=10 ** 5)
    if r and r[2]: return {"quadratic": [int(v) for v in r]}
    ns = {k: getattr(mp, k) for k in dir(mp) if not k.startswith("_")}
    for name, expr in STD.items():
        c = mp.mpmathify(eval(expr, {"__builtins__": {}}, ns))
        r = mp.pslq([1, x, c, x * c], maxcoeff=10 ** 4, maxsteps=10 ** 5)
        if r and (r[1] or r[3]) and (r[2] or r[3]): return {"mobius_of": name, "rel": [int(v) for v in r]}
    return None

def stage2(a, b):
    out = {}
    try:
        from conj13_check import in_conj13; out["conj13"] = bool(in_conj13(a, b))
    except Exception as e: out["conj13"] = "not run: " + type(e).__name__
    try:
        from hyper_check import has_hyper; out["euler_type"] = has_hyper(a, b)
    except Exception as e: out["euler_type"] = "not run: " + type(e).__name__
    hit = out.get("conj13") is True or out.get("euler_type") is True
    return out if hit else None, out

def stage3(name, a, b, x):
    os.environ.setdefault("CFG", "narrow")
    import b18_mechanism as M
    if len(M.lin_factors(b)) < 2: return None, {"note": "b has fewer than two rational linear factors"}
    r = M.search(name, a, b, x); return (r["confirmed"] or None), {"float_hits": r["n_float_hits"]}

def stage7(a, b, partners):
    import sympy as sp, b16_coboundary as B
    proofs = []
    for p in partners[:4]:
        res = B.solve(B.poly(a), B.poly(b), B.poly(p["a2"]), sp.expand(B.poly(p["b2"])))
        proofs.append({"partner_a": p["a2"], "partner_b": p["b2"], "mobius": p["mob"], "proof": res})
        if res: break
    return proofs

def run(a, b, name="target", run_all=False, deep=False, x_override=None):
    t0 = time.time(); rep = {"a": a, "b": b, "stages": {}}
    if x_override is not None: mp.mp.dps = DIG + 10; x = mp.mpf(x_override)
    else: x, _ = cf(a, b, DIG)
    if x is None: rep["error"] = "no convergence"; return rep
    rep["x50"] = mp.nstr(x, 50)
    s1 = stage1(x); rep["stages"]["1_basic"] = s1
    if s1 and not run_all: rep["verdict"] = "identified (stage 1)"; return rep
    s2, info2 = stage2(a, b); rep["stages"]["2_structure"] = info2
    if s2 and not run_all: rep["verdict"] = "known structure (stage 2)"; return rep
    s3, info3 = stage3(name, a, b, x); rep["stages"]["3_mechanism"] = {"matches": s3, **info3}
    if s3:
        rep["stages"]["7_proof"] = stage7(a, b, s3)
        rep["verdict"] = "identified (stage 3)" + (", PROVEN" if any(p["proof"] for p in rep["stages"]["7_proof"]) else ", numerical only")
        if not run_all: return rep
    rep["stages"]["4_low_degree"] = ("not run here; Kaggle: bf_search_b12a.py --const_set targets (see kaggle_b13/kaggle_b15 builders)")
    if deep:
        from deep_id import library
        L = library(); mp.mp.dps = DIG; hits = []
        for nm, c in L.items():
            r = mp.pslq([1, x, c, x * c], maxcoeff=10 ** 8, maxsteps=10 ** 5)
            if r and (r[1] or r[3]) and (r[2] or r[3]): hits.append({"const": nm, "rel": [int(v) for v in r]})
        rep["stages"]["5_library"] = {"n_constants": len(L), "hits": hits[:10]}
    rep["stages"]["6_operator"] = "not run here (SageMath scripts)"
    rep.setdefault("verdict", "UNIDENTIFIED after stages 1-3" + (" and 5" if deep else ""))
    rep["sec"] = round(time.time() - t0); return rep

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        tests = {"Apery_zeta3": ([5, 27, 51, 34], [0, 0, 0, 0, 0, 0, -1]),
                 "C0": ([-3, 10, 4], [24, 38, -69, -68, 60])}
        res = {k: run(a, b, k) for k, (a, b) in tests.items()}
        res["random"] = run([-3, 10, 4], [24, 38, -69, -68, 60], "random", x_override="3.14159" + "27182818284590452353602874713526624977572470936999" * 3)
        ok = (res["Apery_zeta3"].get("verdict", "").startswith("identified (stage 1)") and "PROVEN" in res["C0"].get("verdict", "")
              and res["random"].get("verdict", "").startswith("UNIDENTIFIED"))
        for k, v in res.items(): print(k, "->", v.get("verdict"), flush=True)
        print("SELFTEST", "PASSED" if ok else "FAILED"); sys.exit(0 if ok else 1)
    a = [int(v) for v in sys.argv[1].split(",")]; b = [int(v) for v in sys.argv[2].split(",")]
    rep = run(a, b, "target", "--all" in sys.argv, "--deep" in sys.argv); print(json.dumps(rep, indent=1, default=str))
    if "--out" in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1, default=str)
