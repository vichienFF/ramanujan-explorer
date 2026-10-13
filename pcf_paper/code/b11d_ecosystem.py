"""Batch 11D (PLAN_BATCH11_2026-10-07, exploratory): "ecosystem" clustering of the 5,274 full-FR PCFs + the 15 candidates.
Features: a-coefficients, leading b coefficient, dominant singular point z1 of L, local exponent rho at z1 (Fuchs relation:
exponents 0,1,2,rho with rho = 3 - p3(z1)/p4'(z1)), rho mod 1, FR rate S800 (convergence digits dropped: missing for part of stage 3). Standardised; k-means
k = 5..40 (numpy, 10 restarts), best silhouette. For each candidate: labels of the PCFs in its cluster (drop reason of stage 3,
Euler-type from hyper_check, survivors). Control 1: rho formula must reproduce the 15 registered rho values exactly.
Control 2: column-shuffled features -> silhouette clearly lower. Output: hypotheses only."""
import json, math, os
from collections import Counter
import numpy as np, sympy as sp
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(H, "bf_runs", "track_a")
z, th = sp.symbols("z th")

def stirling2(k, j): return sp.functions.combinatorial.numbers.stirling(k, j)

def rho_and_z1(a, b):
    ap = sum(sp.Rational(c) * (th + 1) ** j for j, c in enumerate(a)); bp = sum(sp.Rational(c) * (th + 2) ** j for j, c in enumerate(b))
    Lth = sp.expand(th ** 2 * (th - 1) ** 2 - z * ap * th ** 2 - z ** 2 * bp)
    P = sp.Poly(Lth, th); p = {4: 0, 3: 0}
    for (k,), c in P.terms():
        for j in (3, 4):
            if k >= j: p[j] += c * stirling2(k, j) * z ** j
    p4, p3 = sp.expand(p[4]), sp.expand(p[3])
    q = sp.Poly(sp.cancel(p4 / z ** 4), z); roots = [r for r in sp.roots(q, multiple=True)]
    z1 = min(roots, key=lambda r: abs(complex(r)))
    rho = sp.nsimplify(sp.simplify(3 - p3.subs(z, z1) / sp.diff(p4, z).subs(z, z1)))
    return complex(z1), rho

def kmeans(X, k, rng, it=60):
    best = None
    for _ in range(10):
        C = X[rng.choice(len(X), k, replace=False)]
        for _ in range(it):
            lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(2), 1)
            C = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        inert = ((X - C[lab]) ** 2).sum()
        if best is None or inert < best[0]: best = (inert, lab)
    return best[1]

def silhouette(X, lab):
    D = np.sqrt(((X[:, None, :] - X[None]) ** 2).sum(2)); s = []
    for i in range(len(X)):
        same = lab == lab[i]; a = D[i, same].sum() / max(same.sum() - 1, 1)
        b = min(D[i, lab == j].mean() for j in set(lab) if j != lab[i]); s.append((b - a) / max(a, b))
    return float(np.mean(s))

if __name__ == "__main__":
    S = json.load(open(os.path.join(T, "stage3.json")))["all"]; C15 = json.load(open(os.path.join(T, "irreducible15.json")))
    sch = {r["name"]: r["rho"] for r in map(json.loads, open(os.path.join(T, "cvalues500.jsonl")))}
    ctrl = []
    for i, c in enumerate(C15):
        z1, rho = rho_and_z1(c["a"], c["b"]); ctrl.append(str(rho) == sch[f"C{i}"])
    print("control 1 (rho reproduces registered values):", sum(ctrl), "/ 15", flush=True)
    hyp = json.load(open(os.path.join(T, "hyper_check.json"))); euler = {(tuple(r["a"]), tuple(r["b"])) for r in hyp if r.get("hyper_factor")}
    cand = {(tuple(c["a"]), tuple(c["b"])): f"C{i}" for i, c in enumerate(C15)}
    rows, feats = [], []
    for r in S:
        a, b = json.loads(r["a"]) if isinstance(r["a"], str) else r["a"], json.loads(r["b"]) if isinstance(r["b"], str) else r["b"]
        try: z1, rho = rho_and_z1(a, b)
        except Exception: continue
        rv = float(sp.re(rho)) if rho.is_real else float("nan")
        if not math.isfinite(rv) or abs(z1.imag) > 1e-12: continue
        key = (tuple(a), tuple(b))
        lab = cand.get(key) or ("euler" if key in euler else (r.get("drop") or "survivor"))
        rows.append({"a": a, "b": b, "label": lab})
        feats.append([a[2], a[1], a[0], b[-1], 1 / z1.real, rv, rv % 1, float(r["S800"])])
    X = np.array(feats, float); X = (X - X.mean(0)) / np.where(X.std(0) > 0, X.std(0), 1)
    print("PCFs with features", len(X), Counter(r["label"] for r in rows).most_common(8), flush=True)
    rng = np.random.default_rng(20261015); idx = rng.choice(len(X), min(1500, len(X)), replace=False)
    best = None
    for k in (5, 8, 12, 16, 20, 30, 40):
        lab = kmeans(X, k, rng); s = silhouette(X[idx], lab[idx]); print("k", k, "silhouette", round(s, 3), flush=True)
        if best is None or s > best[0]: best = (s, k, lab)
    Xs = X.copy()
    for j in range(X.shape[1]): Xs[:, j] = rng.permutation(Xs[:, j])
    ls = kmeans(Xs, best[1], rng); s_sh = silhouette(Xs[idx], ls[idx])
    out = {"plan": "PLAN_BATCH11_2026-10-07 (11D, exploratory)", "control_rho": sum(ctrl), "n": len(X), "best_k": best[1],
           "silhouette": best[0], "silhouette_shuffled": s_sh, "clusters": {}}
    lab = best[2]
    for i, r in enumerate(rows):
        if r["label"].startswith("C"):
            comp = Counter(rows[j]["label"] for j in np.nonzero(lab == lab[i])[0])
            out["clusters"][r["label"]] = {"cluster": int(lab[i]), "size": int((lab == lab[i]).sum()), "composition": comp.most_common(8)}
            print(r["label"], "cluster", lab[i], "size", int((lab == lab[i]).sum()), comp.most_common(6), flush=True)
    print("silhouette best", round(best[0], 3), "shuffled", round(s_sh, 3))
    json.dump(out, open(os.path.join(H, "b11d_result.json"), "w"), indent=1)
