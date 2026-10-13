"""
Brute-force PCF search (no AI), used as the baseline against the LLM explorer.
Same idea as the Ramanujan Machine (Raayoni et al., Nature 2021), simplified:
  polynomial continued fraction  x = a(0) + b(1)/(a(1) + b(2)/(a(2) + ...))
  a(n) = sum ai n^i (deg <= DA), b(n) = sum bi n^i (deg <= DB), coefficients in [-C..C]
Steps:
  1) evaluate all candidates in vectorised float64 (numpy) at depths D and 2D -> keep convergent ones
  2) match against a Mobius table (p + q*c)/(r + s*c) of constants (coefficients in [-R..R]) with a 1e-9 hash
  3) matches -> re-check with high-precision mpmath (converged and matching to >= 30 digits = HIT)
Kaggle-safe: numpy/mpmath only, no internet, no secrets.
Checkpoint: one work unit = one coefficient vector of a -> written to results/unit_<id>.json immediately; finished units are skipped.
Timer: no new unit is started after TIME_LIMIT_H hours (Kaggle 10.5 h standard).
Usage: python bf_search.py --C 3 --DA 2 --DB 2 --R 5 --out results_local
"""
import argparse, glob, itertools, json, math, os, random, time
from fractions import Fraction
from multiprocessing import Pool
import numpy as np
import mpmath

CONSTS = {"zeta2": "zeta(2)", "pi": "pi", "e": "e", "zeta3": "zeta(3)", "log2": "log(2)", "catalan": "catalan", "euler": "euler",
          "sqrt2": "sqrt(2)", "sqrt3": "sqrt(3)", "phi": "phi", "zeta5": "zeta(5)", "pi2": "pi**2", "log3": "log(3)"}
T0 = time.time()


# Extended set (round 3, 2026-09-27): constants less explored than pi/e/zeta(3) - checked for free on every convergent PCF
CONSTS_EXT = {
    "zeta5": "zeta(5)", "zeta7": "zeta(7)", "pi_sqrt3": "pi*sqrt(3)", "pi_sqrt2": "pi*sqrt(2)",
    "log1p_sqrt2": "log(1+sqrt(2))", "log_phi": "log(phi)", "log5": "log(5)", "pi_log2": "pi*log(2)",
    "log2_sq": "log(2)**2", "catalan_over_pi": "catalan/pi", "zeta3_over_pi2": "zeta(3)/pi**2", "pi3": "pi**3",
    "L2_chi3": "(zeta(2, mpf(1)/3) - zeta(2, mpf(2)/3))/9",          # L(2,chi_-3) = "Catalan of mod 3"
    "lemniscate": "gamma(mpf(1)/4)**2/(2*sqrt(2*pi))",               # lemniscate constant
    "gauss": "1/agm(1, sqrt(2))", "gamma13": "gamma(mpf(1)/3)", "gamma14": "gamma(mpf(1)/4)",
    "gamma13_cubed_pi": "gamma(mpf(1)/3)**3/pi", "li2_13": "polylog(2, mpf(1)/3)", "li3_12": "polylog(3, mpf(1)/2)",
    "e_pi": "exp(pi)", "sqrt_pi": "sqrt(pi)", "euler_e": "exp(euler)", "khinchin": "khinchin",
}


def const_values(dps=80):
    mpmath.mp.dps = dps
    return {k: mpmath.mpmathify(eval(v, {"__builtins__": {}}, {n: getattr(mpmath, n) for n in dir(mpmath) if not n.startswith("_")}))
            for k, v in CONSTS.items()}


def use_const_set(name):
    """--const_set ext = base set + extended set (must be called before building the table, in the main and child processes)"""
    if name == "ext":
        CONSTS.update(CONSTS_EXT)


def mobius_table(R):
    cv = const_values(30)
    table = {}
    rng = range(-R, R + 1)
    for name, c in cv.items():
        cf = float(c)
        for p, q, r, s in itertools.product(rng, rng, rng, rng):
            if q == 0 and s == 0 or p * s - q * r == 0:
                continue  # rational value / degenerate
            if math.gcd(math.gcd(p, q), math.gcd(r, s)) != 1 or (r, s) < (0, 0):
                continue  # drop duplicates from scaling / sign changes
            den = r + s * cf
            if abs(den) < 1e-6:
                continue
            v = (p + q * cf) / den
            if abs(v) > 1e6 or abs(v) < 1e-6:
                continue
            table.setdefault(round(v, 8), []).append((name, p, q, r, s))
    return table


def cf_eval_vec(a_coef, B, depth):
    """a_coef: coefficients of a (tuple), B: array (m, DB+1) of b coefficients -> values at depth and 2*depth"""
    m = B.shape[0]
    a0 = float(a_coef[0])
    p1, p0 = np.ones(m), np.full(m, a0)     # p_{-1}, p_0
    q1, q0 = np.zeros(m), np.ones(m)
    ok = np.ones(m, bool)
    out = {}
    for n in range(1, 2 * depth + 1):
        an = float(sum(c * n ** i for i, c in enumerate(a_coef)))
        bn = sum(B[:, i] * float(n) ** i for i in range(B.shape[1]))
        ok &= bn != 0                          # b(n)=0 -> the CF terminates (rational)
        p2 = an * p0 + bn * p1
        q2 = an * q0 + bn * q1
        sc = np.maximum(np.abs(p2), np.abs(q2))
        sc[sc == 0] = 1.0
        p1, p0, q1, q0 = p0 / sc, p2 / sc, q0 / sc, q2 / sc
        if n in (depth, 2 * depth):
            with np.errstate(divide="ignore", invalid="ignore"):
                out[n] = p0 / q0
    v1, v2 = out[depth], out[2 * depth]
    with np.errstate(invalid="ignore"):
        conv = ok & np.isfinite(v1) & np.isfinite(v2) & (np.abs(v1 - v2) <= 1e-11 * np.maximum(1, np.abs(v2)))
    return v2, conv


def cf_mp(a_coef, b_coef, depth, dps):
    mpmath.mp.dps = dps
    A = lambda n: sum(c * n ** i for i, c in enumerate(a_coef))
    Bf = lambda n: sum(c * n ** i for i, c in enumerate(b_coef))
    p1, p0, q1, q0 = mpmath.mpf(1), mpmath.mpf(A(0)), mpmath.mpf(0), mpmath.mpf(1)
    for n in range(1, depth + 1):
        an, bn = A(n), Bf(n)
        p1, p0, q1, q0 = p0, an * p0 + bn * p1, q0, an * q0 + bn * q1
        if n % 50 == 0:
            s = max(abs(p0), abs(q0))
            p1, p0, q1, q0 = p1 / s, p0 / s, q1 / s, q0 / s
    return p0 / q0


def digits(x, y):
    e = abs(x - y) / max(1, abs(x), abs(y))
    return 99 if e == 0 else int(-mpmath.log10(e))


def verify_hit(a_coef, b_coef, match, cv):
    name, p, q, r, s = match
    v1 = cf_mp(a_coef, b_coef, 1500, 60)
    v2 = cf_mp(a_coef, b_coef, 3000, 60)
    mpmath.mp.dps = 60
    target = (p + q * cv[name]) / (r + s * cv[name])
    conv, agree = digits(v1, v2), digits(v2, target)
    return {"a": list(a_coef), "b": list(b_coef), "const": name, "mobius": [p, q, r, s],
            "conv_digits": conv, "agree_digits": agree,
            "status": "HIT" if conv >= 30 and agree >= 30 else ("SLOW" if agree >= 12 else "FLOAT_COINCIDENCE")}


G = {}


def init(args):
    use_const_set(args.const_set)
    G["args"] = args
    G["table"] = mobius_table(args.R)
    G["cv"] = const_values(80)
    G["B"] = b_family(args)


def b_family(args):
    """All b(n) to try: full = all coefficient vectors with deg <= DB; mono = s*n^k*(n+t)^j (k+j <= DB), Apery-like (b = -n^6)"""
    if args.b_mode == "factored":  # v2: b(n) = s*prod(k*n + t), research-type formulas (e.g. 4n^2(2n+1)^2(5n-4)(5n+6))
        lin = [(k, t) for k in args.bk for t in range(-args.bt, args.bt + 1) if not (k > 1 and t % k == 0 and t != 0)]
        out = set()
        for d in args.bdeg:
            for combo in itertools.combinations_with_replacement(lin, d):
                poly = np.array([1.0])
                for k, t in combo:
                    poly = np.polynomial.polynomial.polymul(poly, [t, k])
                for sc in args.bscale:
                    for sgn in (1, -1):
                        c = np.zeros(args.DB + 1)
                        c[:len(poly)] = sgn * sc * poly
                        if c[0] == 0 and not any(c):
                            continue
                        out.add(tuple(int(round(v)) for v in c))
        return np.array(sorted(out), dtype=float)
    if args.b_mode == "full":
        rng = range(-args.C, args.C + 1)
        return np.array([b for b in itertools.product(rng, repeat=args.DB + 1) if any(b)], dtype=float)
    out = set()
    for sgn in [x for x in range(-args.Cb, args.Cb + 1) if x]:
        for k in range(args.DB + 1):
            for j in range(args.DB + 1 - k):
                for t in range(-3, 4):
                    if j and t == 0:
                        continue
                    poly = np.polynomial.polynomial.polymul(np.eye(k + 1)[k], np.polynomial.polynomial.polypow([t, 1], j))
                    c = np.zeros(args.DB + 1)
                    c[:len(poly)] = sgn * poly
                    out.add(tuple(int(round(v)) for v in c))
    return np.array(sorted(out), dtype=float)


def done_units(out):
    """Finished units from jsonl files (Kaggle mode: one line per unit instead of ~10^5 small files)"""
    done = set()
    for f in glob.glob(os.path.join(out, "units_*.jsonl")):
        for line in open(f):
            try:
                done.add(tuple(json.loads(line)["a"]))
            except (ValueError, KeyError):
                pass  # the last line may be truncated if the run was cut -> that unit is rerun
    return done


def run_unit(a_coef):
    args = G["args"]
    path = os.path.join(args.out, "unit_" + "_".join(map(str, a_coef)) + ".json")
    if args.store == "files" and os.path.exists(path):
        return path, None
    if (time.time() - T0) / 3600 > args.time_limit_h:
        return None, "time_limit"
    B = G["B"]
    v, conv = cf_eval_vec(a_coef, B, args.depth)
    hits, unmatched = [], []
    for i in np.nonzero(conv)[0]:
        cands = []
        x = v[i]
        if not (1e-6 < abs(x) < 1e6):
            continue
        k = round(float(x), 8)
        for kk in (k, round(k + 1e-8, 8), round(k - 1e-8, 8)):
            for match in G["table"].get(kk, []):
                name, p, q, r, s = match
                c = float(G["cv"][name])
                if abs((p + q * c) / (r + s * c) - x) <= args.tol * max(1, abs(x)):
                    cands.append(match)
        if cands:  # one CF -> keep only the "lowest" form (smallest coefficients) (phi, sqrt2 have many equivalent forms)
            best = min(cands, key=lambda m: (max(map(abs, m[1:])), sum(map(abs, m[1:]))))
            h = verify_hit(a_coef, [int(t) for t in B[i]], best, G["cv"])
            h["periodic_trivial"] = len(a_coef) == 1 and not any(B[i][1:]) and best[0] in ("phi", "sqrt2", "sqrt3")
            hits.append(h)
        elif args.fr_scan:
            unmatched.append(i)
    mystery = []
    if args.fr_scan and unmatched:  # mystery constants: convergent + no reference match + high factorial reduction (fr_proxy)
        from fr_proxy import fr_count
        idx = np.array(unmatched)
        fr = fr_count(tuple(a_coef), B[idx].astype(np.int64))
        for j in np.nonzero(fr >= args.fr_thr)[0]:
            mystery.append({"b": [int(t) for t in B[idx[j]]], "x": float(v[idx[j]]), "fr": int(fr[j])})
    res = {"a": list(a_coef), "n_cf": int(len(B)), "n_converged": int(conv.sum()),
           "hits": [h for h in hits if h["status"] != "FLOAT_COINCIDENCE"],
           "n_float_coincidence": sum(h["status"] == "FLOAT_COINCIDENCE" for h in hits),
           "mystery": mystery, "n_unmatched": len(unmatched)}
    if args.store == "jsonl":
        path = os.path.join(args.out, f"units_{os.getpid()}.jsonl")
        with open(path, "a") as fh:
            fh.write(json.dumps(res, separators=(",", ":")) + "\n")
            fh.flush()
        return path, None
    tmp = path + ".tmp"
    json.dump(res, open(tmp, "w"), indent=0)
    os.replace(tmp, path)          # atomic write: no half-written file if the run is cut
    return path, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--C", type=int, default=3)
    ap.add_argument("--DA", type=int, default=2)
    ap.add_argument("--DB", type=int, default=2)
    ap.add_argument("--R", type=int, default=5)
    ap.add_argument("--b_mode", choices=["full", "mono", "factored"], default="full")
    ap.add_argument("--bk", type=lambda x: [int(v) for v in x.split(",")], default=[1, 2, 3], help="factored: values of k in (k*n+t)")
    ap.add_argument("--bt", type=int, default=3, help="factored: |t| ≤ bt")
    ap.add_argument("--bdeg", type=lambda x: [int(v) for v in x.split(",")], default=[4], help="factored: number of factors")
    ap.add_argument("--bscale", type=lambda x: [int(v) for v in x.split(",")], default=[1, 2, 4])
    ap.add_argument("--a_pos", type=int, default=0, help="1 = only a with positive leading coefficient (a -> -a gives the negated value = duplicate)")
    ap.add_argument("--Cb", type=int, default=4, help="mono: |s| ≤ Cb")
    ap.add_argument("--store", choices=["files", "jsonl"], default="files")
    ap.add_argument("--const_set", choices=["basic", "ext"], default="basic")
    ap.add_argument("--fr_scan", type=int, default=0, help="1 = keep PCFs with no constant match but high factorial reduction")
    ap.add_argument("--fr_thr", type=int, default=8, help="minimum number of primes (out of 13) dividing both p_N, q_N")
    ap.add_argument("--shard", default="0/1", help="split over several kernels: i/n = only units i, i+n, ...")
    ap.add_argument("--tol", type=float, default=1e-9, help="float match tolerance before the precise check (smaller = fewer false leads)")
    ap.add_argument("--sample", type=int, default=0, help="timing: random sample of N units")
    ap.add_argument("--units", default="", help="testing: restrict units, e.g. '1,3,3,2;5,27,51,34'")
    ap.add_argument("--depth", type=int, default=300)
    ap.add_argument("--out", default="results_local")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--time_limit_h", type=float, default=10.5)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    use_const_set(args.const_set)
    json.dump(vars(args) | {"consts": CONSTS}, open(os.path.join(args.out, "config.json"), "w"), indent=1)
    rng = range(-args.C, args.C + 1)
    units = [a for a in itertools.product(rng, repeat=args.DA + 1) if any(a[1:])]  # constant a(n) is handled separately (DA=0)
    units += [a for a in itertools.product(rng, repeat=1) if a[0] != 0] if args.DA > 0 else []
    if args.a_pos:
        units = [u for u in units if [c for c in u if c][-1] > 0]
    if args.units:
        units = [tuple(int(x) for x in u.split(",")) for u in args.units.split(";")]
    if args.sample:
        units = random.Random(0).sample(units, args.sample)
    si, sn = (int(x) for x in args.shard.split("/"))
    units = sorted(units)[si::sn]
    if args.store == "jsonl":
        done = done_units(args.out)
        units = [u for u in units if tuple(u) not in done]
    print(f"units={len(units)} cf_per_unit~{len(b_family(args))} workers={args.workers}", flush=True)
    done = stopped = 0
    with Pool(args.workers, initializer=init, initargs=(args,)) as pool:
        for path, why in pool.imap_unordered(run_unit, units, chunksize=4):
            if why == "time_limit":
                stopped += 1
                continue
            done += 1
            if done % 200 == 0:
                print(f"{done}/{len(units)} {(time.time()-T0)/60:.1f} min", flush=True)
    print(f"finished units={done} skipped_by_timer={stopped} time={(time.time()-T0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
