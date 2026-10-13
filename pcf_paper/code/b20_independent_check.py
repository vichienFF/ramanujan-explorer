"""Independent re-check of Batch 20A proofs: rebuild M1, M2 from irreducible15.json and the partner, parse V and lambda
from the jsonl, expand q*(M1(n) V(n) - lambda V(n-1) M2(n - s)) and require the zero matrix; also det V != 0."""
import json, sys, sympy as sp
n = sp.Symbol("n"); C = json.load(open("bf_runs/track_a/irreducible15.json"))
P = lambda c: sum(sp.Integer(v) * n ** k for k, v in enumerate(c))
M = lambda a, b, m: sp.Matrix([[0, b.subs(n, m)], [1, a.subs(n, m)]])
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if not r.get("proof"): continue
        i = int(r["job"][1:]); a1, b1 = P(C[i]["a"]), P(C[i]["b"]); a2, b2 = P(r["partner"][0]), P(r["partner"][1]); s = r["s"]
        V = sp.Matrix(2, 2, [sp.sympify(x, locals={"n": n}) for row in r["V"] for x in row]); lam = sp.sympify(r["lambda"], locals={"n": n})
        E = (M(a1, b1, n) * V - lam * V.subs(n, n - 1) * M(a2, b2, n - s)) if r["form"] == "row" else (M(a1, b1, n) * V.subs(n, n - 1) - lam * V * M(a2, b2, n - s))
        ok = all(sp.simplify(sp.together(e)) == 0 for e in E) and sp.expand(V.det()) != 0
        print(r["job"], "partner", r["partner"], "s", s, r["form"], "lambda", lam, "-> identity", "OK" if ok else "FAIL", "| deg V", max(sp.degree(x, n) for x in V))
