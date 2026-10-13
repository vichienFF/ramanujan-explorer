"""Batch 11A (PLAN_BATCH11_2026-10-07): identify the 15 candidates against L-values of rational newforms.
Library: newforms of weight 2, 3, 4, level <= NMAX, rational Fourier coefficients (trivial character for even weight,
Kronecker character (D/.) for weight 3), values L(f, s), s = 1..k, divided by pi^j (j = 0..4).
Tests at 300 digits: PSLQ [1,x,c,xc] (|coef| <= 1e8); for weight 3, 4 also [1,x,c,xc,pi^2,x pi^2] (|coef| <= 1e5).
Hits re-checked at 600 digits. Controls: 5 planted Mobius transforms (all recovered), 15 random reals (0 hits)."""
import json, os, random, sys, time
import cypari2, mpmath as mp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cmf")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deep_id import cf                                 # same exact-recurrence evaluator as the 21,984-constant run
pari = cypari2.Pari(); pari.allocatemem(4 * 10 ** 9)
H = os.path.dirname(os.path.abspath(__file__)); NMAX = int(os.environ.get("NMAX", "100")); DIG = 640

def library():
    pari.set_real_precision(DIG); lib = []
    for k in (2, 3, 4):
        for N in range(1, NMAX + 1):
            chars = [1] if k % 2 == 0 else [D for D in (-3, -4, -7, -8, -11, -15, -19, -20, -23, -24) if N % abs(D) == 0]
            for ch in chars:
                try:
                    mf = pari.mfinit([N, k, ch], 0); B = pari.mfeigenbasis(mf); F = pari.mffields(mf)
                except cypari2.PariError:
                    continue
                for i in range(len(B)):
                    if int(pari.poldegree(F[i])) != 1: continue
                    try:
                        L = pari.lfunmf(mf, B[i])
                        for s in range(1, k + 1):
                            v = pari.lfun(L, s)
                            if abs(float(pari.imag(v))) > 1e-100: continue
                            lib.append((f"L(f[N{N},k{k},chi{ch},#{i}],{s})", k, str(pari.real(v))))
                    except cypari2.PariError:
                        continue
        print("weight", k, "library size", len(lib), flush=True)
    return lib

def test(x, c, big):
    r = mp.pslq([1, x, c, x * c], maxcoeff=10 ** 8, maxsteps=10 ** 6)
    if r and (r[1] or r[3]) and (r[2] or r[3]): return [int(v) for v in r]
    if big:
        p2 = mp.pi ** 2; r = mp.pslq([1, x, c, x * c, p2, x * p2], maxcoeff=10 ** 5, maxsteps=10 ** 6)
        if r and (r[1] or r[3] or r[5]) and (r[2] or r[3]): return [int(v) for v in r]
    return None

def consts_at(lib, dps):
    """vanishing L-values (e.g. central values of odd-sign forms) are dropped: PSLQ needs nonzero entries."""
    mp.mp.dps = dps; return [(f"{nm}/pi^{j}", mp.mpf(v) / mp.pi ** j, k >= 3) for nm, k, v in lib for j in range(5) if abs(mp.mpf(v)) > mp.mpf(10) ** -100]

if __name__ == "__main__":
    t0 = time.time(); lib = library(); C300 = consts_at(lib, 300)
    print("constants", len(C300), f"{time.time()-t0:.0f}s", flush=True)
    rng = random.Random(20261013); out = {"plan": "PLAN_BATCH11_2026-10-07", "n_library": len(lib), "n_constants": len(C300)}
    ctrl = []
    for i in rng.sample(range(len(C300)), 5):
        nm, c, big = C300[i]; x = (3 - 2 * c) / (5 + 7 * c); ctrl.append({"const": nm, "found": test(x, c, big) is not None})
    out["positive_control"] = ctrl; print("positive control", ctrl, flush=True)
    if sys.argv[1:] == ["control"]: sys.exit()
    si, sk = map(int, (sys.argv[1] if len(sys.argv) > 1 else "0/1").split("/")); neg = 0
    for _ in range(15 if si == 0 else 0):
        x = mp.mpf("0." + "".join(str(rng.randint(0, 9)) for _ in range(300))) * 10
        neg += sum(test(x, c, b) is not None for _, c, b in C300)
    out["negative_hits"] = neg; print("negative hits", neg, flush=True)
    T = json.load(open(os.environ.get("TARGETS", os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))); out["hits"] = []
    C600 = None
    for ci, t in enumerate(T):
        if ci % sk != si: continue
        x, n = cf(t["a"], t["b"], 640); mp.mp.dps = 300; x3 = +x
        for idx, (nm, c, big) in enumerate(C300):
            r = test(x3, c, big)
            if r is None: continue
            if C600 is None: C600 = consts_at(lib, 600)
            mp.mp.dps = 600; ok = test(x, C600[idx][1], big) is not None
            out["hits"].append({"C": ci, "const": nm, "rel": r, "confirmed_600": ok}); print("HIT", ci, nm, r, ok, flush=True)
        print("C", ci, "done", f"{time.time()-t0:.0f}s", flush=True)
    out["summary"] = {"controls_ok": all(c["found"] for c in ctrl) and neg == 0, "confirmed_hits": sum(h["confirmed_600"] for h in out["hits"])}
    print(json.dumps(out["summary"])); json.dump(out, open(os.path.join(os.environ.get("OUTDIR", H), f"b11a_result_{si}.json"), "w"), indent=1)
