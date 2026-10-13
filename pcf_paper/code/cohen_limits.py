"""Limits of all constant entries in Cohen's database (closures "()->..."), evaluated through a sandbox (AST whitelist, no direct eval),
then Mobius comparison (<= R) with our values - covers all CF forms (period 2, families, slow convergence)"""
import itertools, json, re, sys
import mpmath as mp
from sandbox import compile_safe, ev

SRC = __import__("os").environ.get("COHEN_SRC", "external/cohen_pcf_db/CFfile2.tex")
REN = [(r"\bPi\b", "pi"), (r"\bCatalan\b", "catalan"), (r"\bEuler\b", "euler"), (r"\blngamma\b", "loggamma"),
       (r"\bI\b", "j"), (r"\^", "**")]
txt = open(SRC, encoding="utf-8").read()
exprs = set()
for m in re.finditer(r"\(\)->", txt):
    s, depth, out = m.end(), 0, ""
    for ch in txt[s:s + 400]:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            if depth == 0:
                break
            depth -= 1
        if ch == "," and depth == 0:
            break
        out += ch
    exprs.add(out.strip())
vals = []
for e in exprs:
    x = e
    for a, b in REN:
        x = re.sub(a, b, x)
    try:
        v = ev(compile_safe(x), 45)
        if isinstance(v, mp.mpc) or not mp.isfinite(v) or v == 0:
            continue
        vals.append((e, v))
    except Exception:
        pass
print("closures", len(exprs), "evaluated", len(vals), flush=True)
targets = []
for f in sys.argv[1:]:
    for t in json.load(open(f)):
        targets.append((f.split("/")[-1], t["a"], t["b"], mp.mpf(t["x80"][:45])))
R, rng = 6, range(-6, 7)
H = {}
for ti, (_, a, b, x) in enumerate(targets):
    xf = float(x)
    for p, q, r, s in itertools.product(rng, rng, rng, rng):
        if p * s - q * r == 0 or abs(r + s * xf) < 1e-9:
            continue
        H.setdefault(round((p + q * xf) / (r + s * xf), 10), []).append((ti, (p, q, r, s)))
mp.mp.dps = 45
hits = []
for e, v in vals:
    for ti, (p, q, r, s) in H.get(round(float(v), 10), []):
        x = targets[ti][3]
        if abs((p + q * x) / (r + s * x) - v) < mp.mpf(10) ** -30:
            hits.append({"target": list(targets[ti][:3]), "cohen_limit": e, "mobius": [p, q, r, s]})
json.dump(hits, open(__import__("os").environ.get("COHEN_OUT", "bf_runs/test_fr/cohen_limit_hits.json"), "w"), indent=0)
print("targets", len(targets), "hits", len(hits), "distinct", len({str(h["target"]) for h in hits}))
for h in hits[:20]:
    print(h["target"], "->", h["cohen_limit"][:70], h["mobius"])
