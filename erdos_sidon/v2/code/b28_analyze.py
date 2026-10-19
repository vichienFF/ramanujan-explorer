"""Batch 28 analysis exactly as PLAN_BATCH28.md (frozen): inverse-variance pooled rho_k = sum w qR / sum w q pred, w=1/(q se)^2."""
import json, glob, numpy as np
R = [json.loads(l) for f in sorted(glob.glob("kaggle_out/*/b28_shard*.jsonl")) for l in open(f)]
S = [r for r in R if r["kind"] == "singer"]; Nn = [r for r in R if r["kind"] == "null"]
print("singer", len(S), "null", len(Nn), "q", min(r["q"] for r in S), max(r["q"] for r in S))
def pooled(rows, k):
    q = np.array([r["q"] for r in rows]); y = q * np.array([r[f"R{k}"] for r in rows]); se = q * np.array([r[f"se_R{k}"] for r in rows])
    pr = q * np.array([r[f"pred{k}"] for r in rows]); w = 1 / se**2
    rho = (w * y).sum() / (w * pr).sum(); serho = np.sqrt(1 / w.sum()) / abs((w * pr).sum() / w.sum())
    return rho, serho, (w * y).sum() / w.sum(), np.sqrt(1 / w.sum())
out = {}
for k in range(3, 7):
    rho, se, m, sm = pooled(S, k); lo = pooled([r for r in S if r["q"] < 1050], k); hi = pooled([r for r in S if r["q"] >= 1050], k)
    nm = pooled(Nn, k)
    out[k] = dict(rho=rho, se=se, ci=(rho - 1.96 * se, rho + 1.96 * se), mean_qR=m, se_qR=sm, rho_low=lo[0], rho_high=hi[0], null_qR=nm[2], null_se=nm[3])
    print(f"k={k} rho={rho:.3f}+-{se:.3f} CI[{rho-1.96*se:.2f},{rho+1.96*se:.2f}] mean qR={m:.2f}+-{sm:.2f} pred~{np.mean([r['q']*r[f'pred{k}'] for r in S]):.2f} | low {lo[0]:.2f} high {hi[0]:.2f} | null qR {nm[2]:.2f}+-{nm[3]:.2f} ({abs(nm[2])/nm[3]:.1f} se)")
T1 = 0.75 <= out[3]["rho"] <= 1.05
T2 = {k: (0.8 <= out[k]["rho"] <= 1.2) or (out[k]["ci"][0] <= 1 <= out[k]["ci"][1] and out[k]["ci"][0] >= 0.8 - 1e-9 and out[k]["ci"][1] <= 1.2 + 1e-9) for k in (4, 5, 6)}
NULL = all(abs(out[k]["null_qR"]) <= 3 * out[k]["null_se"] for k in range(3, 7))
print("T1", T1, "T2", T2, "NULL valid", NULL)
json.dump({str(k): v for k, v in out.items()} | {"T1": T1, "T2": {str(k): v for k, v in T2.items()}, "NULL": NULL}, open("b28_result.json", "w"), indent=1, default=float)
