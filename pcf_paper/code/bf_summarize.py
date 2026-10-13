"""Summarise brute-force results: python bf_summarize.py <result dir> -> <dir>/summary.json + table"""
import glob, json, os, sys
from collections import Counter, defaultdict

d = sys.argv[1]
units = [json.load(open(f)) for f in glob.glob(os.path.join(d, "unit_*.json"))]
for f in glob.glob(os.path.join(d, "**", "units_*.jsonl"), recursive=True):  # Kaggle output (one line per unit)
    for line in open(f):
        try:
            units.append(json.loads(line))
        except ValueError:
            pass  # last line truncated because the run was cut
H = [h for u in units for h in u["hits"]]
real = [h for h in H if h["status"] == "HIT" and not h.get("periodic_trivial")]
by = defaultdict(list)
for h in real:
    by[h["const"]].append(h)
summary = {"units": len(units), "cf_total": sum(u["n_cf"] for u in units),
           "cf_converged": sum(u["n_converged"] for u in units), "hits_all": len(H),
           "status": dict(Counter(h["status"] for h in H)), "periodic_trivial": sum(bool(h.get("periodic_trivial")) for h in H),
           "hits_by_const": {k: len(v) for k, v in by.items()},
           "float_coincidence": sum(u["n_float_coincidence"] for u in units),
           # example with the smallest coefficients for each constant (for manual novelty checks)
           "examples": {k: sorted(v, key=lambda h: sum(map(abs, h["a"] + h["b"])))[:8] for k, v in by.items()}}
json.dump(summary, open(os.path.join(d, "summary.json"), "w"), indent=1)
print({k: v for k, v in summary.items() if k != "examples"})
for k, v in summary["examples"].items():
    for h in v[:4]:
        print(f"{k:8s} a={h['a']} b={h['b']} mobius={h['mobius']} conv={h['conv_digits']}")
