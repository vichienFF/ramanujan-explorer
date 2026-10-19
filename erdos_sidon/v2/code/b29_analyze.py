import json, glob, numpy as np
R = [json.loads(l) for f in sorted(glob.glob("kaggle_out/*/b29_shard*.jsonl")) for l in open(f)]
def pooled(rows, k):
    q = np.array([r["q"] for r in rows]); y = q * np.array([r[f"R{k}"] for r in rows]); se = q * np.array([r[f"se_R{k}"] for r in rows])
    pr = q * np.array([r[f"pred{k}"] for r in rows]); w = 1 / se**2
    rho = (w * y).sum() / (w * pr).sum(); s = np.sqrt(1 / w.sum()) / abs((w * pr).sum() / w.sum())
    return rho, s, (w * y).sum() / w.sum(), np.sqrt(1 / w.sum())
res = {}
for C in (2, 4):
    S = [r for r in R if r["kind"] == "singer" and r["C"] == C]; Nl = [r for r in R if r["kind"] == "null" and r["C"] == C]
    print(f"C={C}: singer {len(S)} null {len(Nl)}")
    for k in range(3, 9):
        rho, s, m, sm = pooled(S, k); nr = pooled(Nl, k)
        ok = 0.8 <= rho <= 1.2 and rho - 1.96 * s <= 1.2 and rho + 1.96 * s >= 0.8
        nullok = abs(nr[2]) <= 3 * nr[3]
        res[f"C{C}k{k}"] = dict(rho=rho, se=s, pass_=ok, null_ok=nullok)
        print(f"  k={k} rho={rho:.3f}+-{s:.3f} CI[{rho-1.96*s:.2f},{rho+1.96*s:.2f}] {'PASS' if ok else 'FAIL'} | null {nr[2]:.2f}+-{nr[3]:.2f} {'ok' if nullok else 'NULL-FAIL'}")
json.dump(res, open("b29_result.json", "w"), indent=1, default=float)
