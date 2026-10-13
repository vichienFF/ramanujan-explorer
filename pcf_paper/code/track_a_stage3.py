"""Track A stages 3-4 (per TRACK_A_PLAN.md): remove the Conjecture 1.3 family (index shifts -2..2) -> limits to 120 digits
-> remove rational/quadratic limits -> remove Mobius of the 36 constants (PSLQ <= 1e5) -> deflate_all -> Mobius clustering (incl. the 23 earlier cases)
Output: bf_runs/track_a/stage3.json (+ survivors.json in the form {a,b,x80} for the Cohen / 3F2 checks)"""
import glob, itertools, json, sys
import mpmath as mp
import sympy as S
import bf_search as BF
from conj13_check import in_conj13

D = "bf_runs/track_a"
n = S.Symbol("n")


def shifted(c, s):
    p = S.Poly(sum(int(v) * (n + s) ** i for i, v in enumerate(c)), n)
    return [int(v) for v in reversed(p.all_coeffs())]


def conj13_any(a, b):
    for s in range(-2, 3):
        r = in_conj13(shifted(a, s), shifted(b, s))
        if r:
            return {"shift": s, **r}
    return None


def deflates(a, b):
    try:
        from ramanujantools.pcf import PCF
        p = PCF(sum(v * n ** i for i, v in enumerate(a)), sum(v * n ** i for i, v in enumerate(b)))
        q = p.deflate_all()
        return S.degree(q.b_n, n) < S.degree(p.b_n, n) or S.degree(q.a_n, n) < S.degree(p.a_n, n)
    except Exception as e:  # noqa
        return None


def main():
    H = [h for f in glob.glob(f"{D}/*.jsonl") for l in open(f) for h in json.loads(l)["hits"] if h.get("fullFR")]
    print("fullFR hits", len(H), flush=True)
    st = {"fullFR": len(H)}
    out = []
    for h in H:
        c = conj13_any(h["a"], h["b"])
        if c:
            h["drop"] = "conj13"; out.append(h); continue
        x1, x2 = BF.cf_mp(h["a"], h["b"], 2000, 130), BF.cf_mp(h["a"], h["b"], 4000, 130)
        dig = int(-mp.log10(abs(x1 - x2) / max(1, abs(x2)) + mp.mpf(10) ** -125))
        h["digits"] = dig; h["x80"] = mp.nstr(x2, 80)
        if dig < 60:
            h["drop"] = "slow_convergence"; out.append(h); continue
        mp.mp.dps = 110
        x = x2
        r = [0, 1, 0] if abs(x) < mp.mpf(10) ** -100 else mp.pslq([1, x, x * x], maxcoeff=10 ** 8, maxsteps=10 ** 5)
        if r:
            h["drop"] = "rational_or_quadratic"; h["rel"] = r; out.append(h); continue
        out.append(h)
    st["conj13"] = sum(h.get("drop") == "conj13" for h in out)
    st["slow"] = sum(h.get("drop") == "slow_convergence" for h in out)
    st["lowdeg"] = sum(h.get("drop") == "rational_or_quadratic" for h in out)
    BF.use_const_set("ext")
    CV = BF.const_values(110)
    for h in out:
        if h.get("drop"):
            continue
        mp.mp.dps = 110
        x = mp.mpf(h["x80"])
        for name, c in CV.items():
            r = mp.pslq([1, x, c, x * c], maxcoeff=10 ** 5, maxsteps=10 ** 5)
            if r and (r[2] or r[3]) and (r[1] or r[3]):
                h["drop"] = "const:" + name; h["rel"] = r; break
    st["const"] = sum(str(h.get("drop", "")).startswith("const") for h in out)
    for h in out:
        if not h.get("drop") and deflates(h["a"], h["b"]):
            h["drop"] = "deflates"
    st["deflates"] = sum(h.get("drop") == "deflates" for h in out)
    # Mobius clustering (PSLQ [1,x,y,xy] <= 1e4 - stricter than the plan (<= 12), so fewer new clusters are counted), the 23 earlier cases as reference clusters
    known = [{"a": t[0], "b": t[1], "x80": None, "known": True} for t in json.load(open("bf_runs/test_fr/final_candidates_23.json"))]
    K45 = {(tuple(m["a"]), tuple(m["b"])): m["x80"] for m in json.load(open("bf_runs/test_fr/mystery_fullFR45.json"))}
    for k in known:
        k["x80"] = K45.get((tuple(k["a"]), tuple(k["b"])))
    known = [k for k in known if k["x80"]]
    live = [h for h in out if not h.get("drop")]
    items = known + live
    mp.mp.dps = 75
    X = [mp.mpf(m["x80"]) for m in items]
    par = list(range(len(items)))
    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for i, j in itertools.combinations(range(len(items)), 2):
        if find(i) == find(j):
            continue
        r = mp.pslq([1, X[i], X[j], X[i] * X[j]], maxcoeff=10 ** 4, maxsteps=20000)
        if r and (r[1] or r[3]) and (r[2] or r[3]):
            par[find(j)] = find(i)
    groups = {}
    for i in range(len(items)):
        groups.setdefault(find(i), []).append(i)
    new_clusters, extend_known = [], []
    for g in groups.values():
        mem = [items[i] for i in g]
        if any(m.get("known") for m in mem):
            if any(not m.get("known") for m in mem):
                extend_known.append(mem)
            continue
        new_clusters.append(mem)
    st["survivors"] = len(live); st["known_clusters_extended"] = len(extend_known); st["new_clusters"] = len(new_clusters)
    reps = [min(c, key=lambda m: sum(map(abs, m["a"] + m["b"]))) for c in new_clusters]
    json.dump({"stats": st, "all": out, "new_clusters": new_clusters, "extend_known": extend_known},
              open(f"{D}/stage3.json", "w"), indent=0, default=str)
    json.dump([{"a": r["a"], "b": r["b"], "x80": r["x80"]} for r in reps], open(f"{D}/survivors.json", "w"), indent=0)
    print(json.dumps(st), flush=True)
    for c in new_clusters[:30]:
        r = min(c, key=lambda m: sum(map(abs, m["a"] + m["b"])))
        print(len(c), r["a"], S.factor(sum(v * n ** i for i, v in enumerate(r["b"]))), r["x80"][:30])


if __name__ == "__main__":
    main()
