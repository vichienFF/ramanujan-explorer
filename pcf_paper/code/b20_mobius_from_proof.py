"""Derive the exact Mobius map implied by each coboundary proof and compare with the numerically identified relation.
Row convention: W(N) = A M(1)...M(N) = [[P_{N-1}, P_N], [Q_{N-1}, Q_N]], A = [[1, a(0)], [0, 1]].
Proof M1(n) V(n) = lam V(n-1) M2(n-s)  =>  M1(1..N) = Lam V(0) M2(1-s..N-s) V(N)^-1, so W1(N) ~ G W2(N-s) V(N)^-1 with
G = A1 V(0) K, K = (A2 M2(1)..M2(-s))^-1 (s <= 0) or M2(1-s)..M2(0) A2^-1 (s > 0); then (x, 1)^T ~ G (y, 1)^T."""
import json, sympy as sp, mpmath as mp, b20_rational as B, b18_mechanism as M18
n = sp.Symbol("n"); C = json.load(open("bf_runs/track_a/irreducible15.json"))
P = lambda c: sum(sp.Integer(v) * n ** k for k, v in enumerate(c))
Mx = lambda a, b, m: sp.Matrix([[0, b.subs(n, m)], [1, a.subs(n, m)]])
rows = []
for f in ("b20_C1.jsonl", "b20_a201_C5.jsonl", "b20_a201_C7.jsonl", "b20_a201_C14.jsonl", "b20_a201_control.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if r.get("proof") and r["job"] in ("C1", "C5", "C7", "C14", "pos1_C0"): rows.append(r)
mp.mp.dps = 80
for r in rows:
    i = 0 if r["job"] == "pos1_C0" else int(r["job"][1:]); a1, b1 = P(C[i]["a"]), P(C[i]["b"]); a2, b2 = P(r["partner"][0]), P(r["partner"][1]); s = r["s"]
    V0 = sp.Matrix(2, 2, [sp.sympify(x, locals={"n": n}).subs(n, 0) for row in r["V"] for x in row])
    A1 = sp.Matrix([[1, a1.subs(n, 0)], [0, 1]]); A2 = sp.Matrix([[1, a2.subs(n, 0)], [0, 1]])
    if s <= 0:
        K = A2
        for m in range(1, -s + 1): K = K * Mx(a2, b2, m)
        K = K.inv()
    else:
        K = sp.eye(2)
        for m in range(1 - s, 1): K = K * Mx(a2, b2, m)
        K = K * A2.inv()
    G = (A1 * V0 * K).applyfunc(sp.nsimplify)
    fa = lambda c: (lambda m: sum(v * m ** k for k, v in enumerate(c)))
    x, _ = M18.limit_mp(fa(C[i]["a"]), fa(C[i]["b"]), 60, 64000); y, _ = M18.limit_mp(fa(r["partner"][0]), fa(r["partner"][1]), 60, 64000)
    mp.mp.dps = 90; g = [mp.mpf(sp.Rational(v).p) / sp.Rational(v).q for v in G]
    xp = (g[0] * y + g[1]) / (g[2] * y + g[3])
    # exact inverse map y = (g22 x - g12)/(-g21 x + g11)
    print(r["job"], "G =", G.tolist(), "| x from proof vs x:", mp.nstr(abs(xp - x), 3), "| y =", sp.simplify((G[1,1]*sp.Symbol('x') - G[0,1]) / (-G[1,0]*sp.Symbol('x') + G[0,0])))
