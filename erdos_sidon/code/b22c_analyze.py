"""Amendment 22-4 Route B analysis (registered): g*(q) = G*/q for Bose sets; bounded vs log, train q <= 1000, test q > 1000,
test RMSE (within 5% -> bounded); controls synthetic bounded / log (b = 1), resampled residuals, 1000 replicates, >= 80%.
Positive control: Bose q = 829 excess >= 0.9 * 10.279. Null model and Singer reported descriptively."""
import json, os
import numpy as np
from scipy.optimize import curve_fit
H = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(20261015)
R = [json.loads(l) for l in open(os.path.join(H, "b22c_run.jsonl"))]
bose = sorted((r for r in R if r["kind"] == "bose" and "G_star" in r), key=lambda r: r["q"])
q = np.array([r["q"] for r in bose], float); g = np.array([r["g_star_over_q"] for r in bose])
models = {"bounded": (lambda x, c: c + 0 * x, [1.0]), "log": (lambda x, a, b: a + b * np.log(x), [0.0, 1.0])}
tr, te = q <= 1000, q > 1000
def select(Y):
    out = {}
    for m, (f, p0) in models.items():
        p, _ = curve_fit(f, q[tr], Y[tr], p0=p0); r = Y[te] - f(q[te], *p)
        out[m] = {"params": [float(v) for v in p], "test_rmse": float(np.sqrt(np.mean(r ** 2)))}
    s = "bounded" if out["bounded"]["test_rmse"] <= 1.05 * out["log"]["test_rmse"] else "log"
    return s, out
sel, fits = select(g); f, _ = models[sel]; resid = g - f(q, *fits[sel]["params"])
ctrl = {"bounded": sum(select(np.full(len(q), g.mean()) + rng.choice(resid, len(q)))[0] == "bounded" for _ in range(1000)) / 1000,
        "log": sum(select(1.0 * np.log(q) + rng.choice(resid, len(q)))[0] == "log" for _ in range(1000)) / 1000}
pc = next(r for r in bose if r["q"] == 829)["excess_best_cut"]
res = {"n_bose": len(bose), "construction_errors": [r for r in R if "err" in r], "all_sidon": all(r.get("sidon") for r in R if r["kind"] != "null" and "G_star" in r),
       "positive_control_q829_excess": pc, "positive_control_ok": pc >= 0.9 * 10.279, "fits": fits, "selected": sel, "controls": ctrl,
       "controls_ok": all(v >= 0.8 for v in ctrl.values())}
res["verdict"] = ("VOID" if not (res["controls_ok"] and res["positive_control_ok"] and res["all_sidon"]) else
                  f"{sel} [INFERENCE: Bose sets, q in [101, 2003]]")
for lo, hi in ((101, 300), (300, 1000), (1000, 2003)):
    s = [r for r in bose if lo <= r["q"] < hi or (hi == 2003 and r["q"] == 2003)]
    res[f"bose_{lo}_{hi}"] = {"median_g_star_over_q": float(np.median([r["g_star_over_q"] for r in s])),
                              "median_excess": float(np.median([r["excess_best_cut"] for r in s])),
                              "median_p99_gap_over_q": float(np.median([r["p99_gap_over_q"] for r in s])),
                              "median_median_gap_over_q": float(np.median([r["median_gap_over_q"] for r in s]))}
nul = [r for r in R if r["kind"] == "null"]; res["null_vs_bose"] = []
for qq in sorted({r["q"] for r in nul}):
    b = next((r for r in bose if r["q"] == qq), None); n = [r["g_star_over_q"] for r in nul if r["q"] == qq]
    res["null_vs_bose"].append({"q": qq, "bose_g": b and round(b["g_star_over_q"], 2), "null_g_mean": round(float(np.mean(n)), 2)})
res["singer"] = [{"q": r["q"], "g": round(r["g_star_over_q"], 2), "excess": round(r["excess_best_cut"], 2)} for r in R if r["kind"] == "singer" and "G_star" in r]
print(json.dumps(res, indent=1)); json.dump(res, open(os.path.join(H, "b22c_result.json"), "w"), indent=1)
