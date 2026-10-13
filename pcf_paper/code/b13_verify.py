"""12A verification (registered 8533de3: re-check at >= 120 digits). Recompute candidate x and every HIT PCF to 160 digits
(exact recurrence) and test the Mobius relation x = (p + q y)/(r + s y) as reported by the search."""
import json, glob, os, sys
import mpmath as mp
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "cmf"))
from deep_id import cf
C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
hits = []
for f in [f for k in sys.argv[1].split(",") for f in glob.glob(os.path.join(H, "kaggle_out", k, "**", "units_*.jsonl"), recursive=True)]:
    for l in open(f, encoding="utf-8"):
        try: u = json.loads(l)
        except ValueError: continue
        hits += [h for h in (u.get("hits") or []) if h.get("status") == "HIT" and h["const"][0] == "C" and h["const"] not in ("C10", "C11")]
X = {}
out = []
for h in hits:
    name = h["const"]
    if name[0] == "P": continue
    i = int(name[1:])
    if i not in X: X[i], _ = cf(C[i]["a"], C[i]["b"], 160)
    y, n = cf(h["a"], h["b"], 160); mp.mp.dps = 170
    p, q, r, s = h["mobius"]; x = X[i]
    pred_y = (p + q * x) / (r + s * x)          # bf_search table convention: PCF value y = (p + q c)/(r + s c), c = target
    best = ("y=(p+qx)/(r+sx)",); err = abs(pred_y - y); dig = float(-mp.log10(err / abs(y))) if err > 0 else 170.0
    out.append({"C": i, "a": h["a"], "b": h["b"], "mobius": h["mobius"], "digits_agree": round(dig, 1), "form": best[0], "y40": mp.nstr(y, 40)})
    print(name, h["a"], h["b"], h["mobius"], "agree", round(dig, 1), "digits", flush=True)
json.dump(out, open(os.path.join(H, sys.argv[2]), "w"), indent=1)
