# Batch 11B (PLAN_BATCH11_2026-10-07, 68d92eb): numerical monodromy of the order-4 operators.
# Generators: loops from a common base point around every finite singular point (including 0). Test: traces of words of
# length 2..4 in the generators are algebraic of degree <= 4 (mpmath findpoly on real and imaginary parts, height <= 1e6).
# Single generators are skipped (their traces are sums of roots of unity because the local exponents are rational).
# Controls: F1, G1, G2 (registered) and the hypergeometric operator theta^4 - 256 z (theta+1/2)^4 (extra positive control).
from ore_algebra import OreAlgebra
import json, itertools, mpmath
exec(preparse(open("sage_connect.sage").read().split('if __name__ == "__main__":')[0]))   # op(a, b)

def generators(L, eps=1e-50):
    sing = sorted([CC(r) for r, _ in L.leading_coefficient().roots(QQbar)], key=lambda r: (abs(r), r.arg()))
    nz = [s for s in sing if abs(s) > 1e-30]
    base = CC(0, 1) * min(abs(s) for s in nz) / 3          # off the real axis, inside the smallest disc
    gens = []
    for s in sing:
        r = min([abs(s - t) for t in sing if t != s] + [abs(s - base)]) / 3
        pts = [base, s + CC(0, 1) * r, s - r, s - CC(0, 1) * r, s + r, s + CC(0, 1) * r, base]
        pts = [QQbar(QQ(round(p.real(), 12))) + QQbar(QQ(round(p.imag(), 12))) * QQbar(I) for p in pts]
        gens.append((str(s), L.numerical_transition_matrix(pts, eps)))
    return gens

def algebraic(v):
    mpmath.mp.dps = int(45)                               # python ints only: Sage Integers break mpmath internals
    for part in (v.real(), v.imag()):
        x = mpmath.mpf(str(part.center()))
        if abs(x) < mpmath.mpf(str("1e-35")): continue
        if mpmath.findpoly(x, int(4), maxcoeff=int(1000000)) is None: return False
    return True

def analyse(name, L):
    G = generators(L); res = {"name": name, "n_gen": len(G), "singular": [g[0] for g in G], "words": 0, "algebraic": 0}
    mats = [g[1] for g in G]
    for ln in (2, 3, 4):
        for w in itertools.product(range(len(mats)), repeat=ln):
            if any(w[i] == w[i + 1] for i in range(ln - 1)): continue
            M = mats[w[0]]
            for j in w[1:]: M = M * mats[j]
            res["words"] += 1; res["algebraic"] += algebraic(M.trace())
    res["frac_algebraic"] = res["algebraic"] / max(res["words"], 1)
    print(name, res["n_gen"], "generators | words", res["words"], "algebraic traces", res["algebraic"], flush=True); return res

T = json.load(open("bf_runs/track_a/irreducible15.json")); out = []
th = z * Dz
out.append(analyse("CTRL_hyp_4F3", th^4 - 256 * z * (th + 1/2)^4))
for name, (a, b) in [("F1", ([-3, 10, 4], [0, 0, 16, -8, -3])), ("G1", ([-3, 10, 4], [-15, 76, -93, -4, 12])),
                      ("G2", ([-3, 10, 4], [15, 26, -21, -20, 12]))]:
    out.append(analyse(name, op(a, b)))
for i, t in enumerate(T):
    out.append(analyse(f"C{i}", op(t["a"], t["b"])))
json.dump(out, open("bf_runs/track_a/monodromy11b.json", "w"), indent=0, default=str)
