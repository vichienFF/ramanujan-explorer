"""Stage-3 bug fix: Mobius check against the 36 constants redone with full-precision x (before: x80 at dps 110 -> PSLQ missed)"""
import json
import mpmath as mp
import bf_search as BF
BF.use_const_set("ext")
CV = BF.const_values(110)
T = json.load(open("bf_runs/track_a/survivors.json"))
out = []
for t in T:
    x = BF.cf_mp(t["a"], t["b"], 4000, 130); mp.mp.dps = 110
    t["x110"] = mp.nstr(x, 110); t["const"] = None
    for name, c in CV.items():
        r = mp.pslq([1, x, c, x * c], maxcoeff=10**5, maxsteps=10**5)
        if r and (r[2] or r[3]) and (r[1] or r[3]):
            t["const"] = [name, [int(v) for v in r]]; break
    out.append(t)
json.dump(out, open("bf_runs/track_a/survivors_constfix.json", "w"), indent=0)
from collections import Counter
print("matched", sum(1 for t in out if t["const"]), "/", len(out), Counter(t["const"][0] for t in out if t["const"]))
