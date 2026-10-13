"""Batch 20B analysis: fraction of wrapped degree-(1,2) PCFs per label, 95% Wilson intervals; budget/slow counted apart."""
import json, glob, math, collections
R = [json.loads(l) for f in sorted(glob.glob("kaggle_out/rama-b20b-r1-*/b20_out/res_*.jsonl")) for l in open(f)]
def wilson(k, m, z=1.96):
    if m == 0: return (float("nan"),) * 2
    p = k / m; d = 1 + z * z / m; c = (p + z * z / (2 * m)) / d; h = z * math.sqrt(p * (1 - p) / m + z * z / (4 * m * m)) / d
    return round(c - h, 3), round(c + h, 3)
cls = collections.defaultdict(collections.Counter)
for r in R:
    lab = r["name"].split("|")[-1]
    if r.get("err"): k = "slow_target"
    elif r.get("deadline"): k = "deadline"
    elif r["confirmed"]: k = "wrapped"
    elif r.get("budget"): k = "budget"
    elif r.get("slow_partners"): k = "slow_partner"
    elif r["n_float_hits"] > 10: k = "truncated"            # MAX_RECHECK = 10: unchecked float hits remain
    else: k = "negative"
    cls[lab][k] += 1
out = {"n_records": len(R), "names_unique": len({r["name"] for r in R})}
for lab, c in sorted(cls.items()):
    dec = c["wrapped"] + c["negative"]; out[lab] = dict(c, decided=dec, frac_wrapped=round(c["wrapped"] / dec, 3) if dec else None, wilson95=wilson(c["wrapped"], dec))
    print(lab, dict(c), "decided", dec, "frac", out[lab]["frac_wrapped"], "CI", out[lab]["wilson95"])
json.dump(out, open("b20B_result.json", "w"), indent=1)
