import json
exec(preparse(open("sage_connect.sage").read().split('if __name__ == "__main__":')[0]))
T = json.load(open("bf_runs/track_a/irreducible15.json")); out = []
for i, t in enumerate(T):
    M, b1, vP, vQ = x_from_connection(t["a"], t["b"], eps=1e-60)
    k = [j for j, m in enumerate(b1) if "^(" in str(m) and "log" not in str(m)]
    k = k[0] if k else 0
    CP, CQ = vP[k], vQ[k]
    xr = (CP/CQ).real()
    rec = {"i": i, "mono": str(b1[k]), "basis": [str(m) for m in b1], "CP": str(CP.real()), "CQ": str(CQ.real()),
           "x_conn": str(xr), "x_cf": t["x50"], "match": abs(RealField(200)(t["x50"]) - xr.center()) < 1e-40}
    out.append(rec); print(i, rec["mono"], "match", rec["match"], "| CQ", str(CQ.real())[:40], flush=True)
json.dump(out, open("bf_runs/track_a/connect15.json", "w"), indent=0)
