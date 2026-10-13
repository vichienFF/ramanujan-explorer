"""Batch 21B (PLAN_BATCH21_2026-10-13): mechanism-guided filter.
Partners b2(n) = kappa (k1 (n+s1) + t1)(k2 (n+s2) + t2) for every pair of linear factors of the candidate's b, independent
shifts s1, s2 in -6..6, kappa in +-{wide list}; alpha fixed by alpha^2 = lead(b2) A^2 / B (A = lead a1, B = lead b1);
alpha = u/d with d in {1,2,3} -> integer partner a2 = u n + beta, b2 -> d^2 b2 (|beta| <= 1000, <= 3000 for d = 3);
Mobius |coef| <= 12. Float match (depth 600 / 1200), 160-digit re-check (Amendment 18-2 evaluator, slow partners logged).
Checkpoint: one jsonl line per sub-unit (target, pair, s1); time check inside the kappa loop (TLIM_H; unit not recorded if cut).
Usage: python b21b_mechanism.py <targets.json> <out.jsonl>     targets: {name: {"a": [...], "b": [...], "x": "<180 digits>"}}
env: SHARD=i/k (over sub-units), TLIM_H, RC_DMAX (default 64000)."""
import itertools, json, math, os, sys, time
from fractions import Fraction
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import b20b_mechanism as M20
mp = M20.B10.mp
KS = (1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 25, 27, 32, 36, 48, 49, 50, 64, 72, 81, 100, 144)
SH = range(-6, 7); R = 12; DEPTH = 600; CHECK = 160
DEADLINE = time.time() + float(os.environ.get("TLIM_H", "1e9")) * 3600

def mobius_table(x):
    tab = {}
    for p, q, r, s in itertools.product(range(-R, R + 1), repeat=4):
        if p * s - q * r == 0 or math.gcd(math.gcd(p, q), math.gcd(r, s)) != 1: continue
        den = r + s * x
        if abs(den) < 1e-9: continue
        v = (p + q * x) / den
        if 1e-6 < abs(v) < 1e6: tab.setdefault(round(v, 8), []).append((p, q, r, s))
    return tab

def frac_sqrt(f):
    if f <= 0: return None
    a, b = math.isqrt(f.numerator), math.isqrt(f.denominator)
    return Fraction(a, b) if a * a == f.numerator and b * b == f.denominator else None

def units(T):
    for name, t in T.items():
        facs = M20.lin_factors(t["b"]); pairs = sorted({tuple(sorted(pq)) for pq in itertools.combinations(facs, 2)})
        for pi, pr in enumerate(pairs):
            for s1 in SH: yield name, t, pi, pr, s1

def run_unit(t, pr, s1, x, tab):
    (k1, t1), (k2, t2) = pr; A, B = t["a"][-1], t["b"][-1]; hits = []; xf = float(x)
    for s2 in SH:
        f1 = (k1, t1 + k1 * s1); f2 = (k2, t2 + k2 * s2)
        base = [f1[1] * f2[1], f1[0] * f2[1] + f2[0] * f1[1], f1[0] * f2[0]]
        for k in KS:
            for kap in (k, -k):
                if time.time() > DEADLINE: return None
                al = frac_sqrt(Fraction(kap * base[2] * A * A, B))
                if al is None or al.denominator not in (1, 2, 3): continue
                d = al.denominator; u = al.numerator; b2 = [kap * d * d * c for c in base]
                if any(sum(c * m ** j for j, c in enumerate(b2)) == 0 for m in range(1, 40)): continue
                bmax = 3000 if d == 3 else 1000; beta = np.arange(-bmax, bmax + 1)
                y1 = M20.cf_vec(u, beta, b2, DEPTH); y2 = M20.cf_vec(u, beta, b2, 2 * DEPTH)
                ok = np.isfinite(y1) & (np.abs(y1 - y2) < 1e-11 * np.maximum(1, np.abs(y2)))
                for i in np.nonzero(ok)[0]:
                    key = round(float(y2[i]), 8)
                    for kk in (key, round(key + 1e-8, 8), round(key - 1e-8, 8)):
                        if kk in tab:
                            hits.append({"a2": [int(beta[i]), u], "b2": b2, "s": [s1, s2], "kappa": kap, "d": d, "mob": tab[kk][0]}); break
    conf = []
    for h in hits:
        if time.time() > DEADLINE: return None
        A_ = lambda m, h=h: h["a2"][0] + h["a2"][1] * m; B_ = lambda m, h=h: sum(c * m ** j for j, c in enumerate(h["b2"]))
        y, dig = M20.limit_mp(A_, B_, CHECK, int(os.environ.get("RC_DMAX", "64000")))
        if y is None: h["slow_partner"] = True; h["slow_digits"] = dig; continue
        p, q, r, s = h["mob"]; mp.mp.dps = CHECK + 10; pred = (p + q * x) / (r + s * x)
        dd = float(-mp.log10(abs(pred - y) / max(abs(y), 1))) if pred != y else CHECK
        h["digits"] = round(dd, 1)
        if dd >= CHECK - 15: conf.append(h)
    return {"hits": hits, "confirmed": conf}

if __name__ == "__main__":
    T = json.load(open(sys.argv[1])); outf = sys.argv[2]; si, sk = map(int, os.environ.get("SHARD", "0/1").split("/"))
    done = set()
    if os.path.exists(outf):
        for l in open(outf):
            try: r = json.loads(l); done.add((r["name"], r["pair_i"], r["s1"]))
            except (ValueError, KeyError): pass
    xs, tabs = {}, {}; t0 = time.time()
    for j, (name, t, pi, pr, s1) in enumerate(units(T)):
        if j % sk != si or (name, pi, s1) in done: continue
        if time.time() > DEADLINE: print("deadline - stopping, next round continues", flush=True); break
        if name not in xs:
            mp.mp.dps = CHECK + 30; xs[name] = mp.mpf(t["x"]); tabs[name] = mobius_table(float(xs[name]))
        tu = time.time(); r = run_unit(t, pr, s1, xs[name], tabs[name])
        if r is None: print("deadline inside unit", name, pi, s1, "- not recorded", flush=True); break
        rec = {"name": name, "pair_i": pi, "pair": [list(pr[0]), list(pr[1])], "s1": s1, "n_hits": len(r["hits"]),
               "n_slow": sum(1 for h in r["hits"] if h.get("slow_partner")), "confirmed": r["confirmed"], "hits": r["hits"], "sec": round(time.time() - tu, 1)}
        open(outf, "a").write(json.dumps(rec, default=str) + "\n")
        print(name, pi, s1, "hits", rec["n_hits"], "slow", rec["n_slow"], "confirmed", [(c["a2"], c["b2"], c["mob"], c["digits"]) for c in r["confirmed"]], rec["sec"], "s", f"total {time.time()-t0:.0f}s", flush=True)
