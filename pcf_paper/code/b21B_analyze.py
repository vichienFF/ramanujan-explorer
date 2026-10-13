"""Batch 21B analysis: per target confirmed partners, hits, slow partners; unit coverage check against b21b units()."""
import json, glob, collections, b21b_mechanism as M
T = json.load(open("b21B_targets.json")); exp = {(n, pi, s1) for n, t, pi, pr, s1 in M.units(T)}
R = [json.loads(l) for f in sorted(glob.glob("kaggle_out/rama-b21b-r1-*/b21_out/res_*.jsonl")) for l in open(f)]
got = {(r["name"], r["pair_i"], r["s1"]) for r in R}
print("units expected", len(exp), "recorded", len(R), "unique", len(got), "missing", len(exp - got))
S = collections.defaultdict(lambda: {"hits": 0, "slow": 0, "conf": []})
for r in R:
    s = S[r["name"]]; s["hits"] += r["n_hits"]; s["slow"] += r["n_slow"]; s["conf"] += r["confirmed"]
out = {}
for n in T:
    s = S[n]; best = sorted(s["conf"], key=lambda c: (abs(c["a2"][1]) + sum(abs(v) for v in c["b2"])))[:3]
    out[n] = {"hits": s["hits"], "slow": s["slow"], "n_confirmed": len(s["conf"]), "simplest": best}
    print(n, "hits", s["hits"], "slow", s["slow"], "confirmed", len(s["conf"]), [(c["a2"], c["b2"], c["s"], c["mob"], c["digits"]) for c in best[:2]])
json.dump(out, open("b21B_result.json", "w"), indent=1, default=str)
