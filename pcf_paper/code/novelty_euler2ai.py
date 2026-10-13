"""Novelty check: compare the limits of the 15 irreducible cases + 22 earlier candidates with the 149+22 PCFs of the euler2ai data set (read only, not redistributed).
Mobius comparison: PSLQ [1,x,y,xy], coefficients <= 1e4, 50 digits (y = euler2ai PCF value computed directly from a, b)"""
import json, pickle
import mpmath as mp, sympy as sp
import bf_search as BF
n = sp.Symbol('n')
E = []
for f in ["external/euler2ai/dataset/pcfs.pkl", "external/euler2ai/dataset/cmf_pcfs_compact.pkl"]:
    df = pickle.load(open(f, "rb"))
    for _, r in df.iterrows():
        try:
            a = sp.Poly(sp.sympify(str(r["a"])), n).all_coeffs()[::-1]; b = sp.Poly(sp.sympify(str(r["b"])), n).all_coeffs()[::-1]
            a = [sp.Rational(v) for v in a]; b = [sp.Rational(v) for v in b]
            if any(v.q != 1 for v in a + b): continue
            y = BF.cf_mp([int(v) for v in a], [int(v) for v in b], 3000, 70)
            if mp.isfinite(y) and y != 0: E.append((f.split("/")[-1], str(r["a"]), str(r["b"]), y))
        except Exception:
            pass
print("euler2ai PCFs evaluated:", len(E), flush=True)
R = [json.loads(l) for l in open("bf_runs/track_a/classify.jsonl")]
T = [r for r in R if r["ode_orders"] == [4] or r["src"] == "known23"]
hits = []
for t in T:
    x = BF.cf_mp(t["a"], t["b"], 3000, 70); mp.mp.dps = 50
    for src, ea, eb, y in E:
        mp.mp.dps = 50
        r = mp.pslq([1, x, y, x*y], maxcoeff=10**4, maxsteps=20000)
        if r and (r[1] or r[3]) and (r[2] or r[3]):
            hits.append({"a": t["a"], "b": t["b"], "src": t["src"], "euler2ai": [src, ea, eb], "rel": [int(v) for v in r]})
            print("HIT", t["src"], t["a"], t["b"], "<->", ea, "|", eb, r, flush=True)
json.dump(hits, open("bf_runs/track_a/novelty_euler2ai.json", "w"), indent=0)
print("targets", len(T), "hits", len(hits), "distinct targets", len({str(h['b']) for h in hits}))
