"""Batch 4 K3 (registered dd7a724): deep identification of the 15 irreducible candidates (+ controls G1, G2).
x to >= 1000 digits; library: Li_k(r), L(k,chi_d), Clausen, pi^a sqrt(d) log(r), Gamma(j/d)^k pi^a sqrt(e) (d<=24),
elliptic K at singular moduli. Test PSLQ [1, x, c, x c] (coeff <= 1e8) at 1000 digits; hit = relation using x and c.
Checkpoint: 1 jsonl line per target."""
import itertools, json, math, os, sys, time
import mpmath as mp

DPS = 1050

def cf(a, b, digits):
    """exact-integer convergents until two successive values agree to `digits`"""
    A = lambda n: sum(c * n ** i for i, c in enumerate(a)); B = lambda n: sum(c * n ** i for i, c in enumerate(b))
    mp.mp.dps = digits + 30; P0, P1, Q0, Q1 = 1, A(0), 0, 1; prev = None; n = 0
    while True:
        n += 1; P0, P1, Q0, Q1 = P1, A(n) * P1 + B(n) * P0, Q1, A(n) * Q1 + B(n) * Q0
        if n % 200 == 0:
            g = math.gcd(P1, Q1); x = mp.mpf(P1 // g) / (Q1 // g)
            if prev is not None and abs(x - prev) < mp.mpf(10) ** (-digits - 5): return x, n
            prev = x
        if n > 400000: return None, n

def kronecker(d, n):
    from sympy.ntheory import legendre_symbol  # noqa
    from sympy import factorint
    r = 1
    for p, e in factorint(n).items():
        if p == 2: v = 0 if d % 2 == 0 else (1 if d % 8 in (1, 7) else -1)
        else: v = 0 if d % p == 0 else (1 if pow(d % p, (p - 1) // 2, p) == 1 else -1)
        r *= v ** e
    return r

def library():
    mp.mp.dps = DPS; L = {}
    for k in range(1, 5):
        for r in ("1/2", "-1/2", "1/3", "-1/3", "1/4", "-1/4", "1/9", "-1/8"):
            L[f"Li{k}({r})"] = mp.polylog(k, mp.mpf(int(r.split("/")[0])) / int(r.split("/")[1]))
    disc = [d for d in range(-100, 101) if d not in (0, 1) and (d % 4 == 1 or (d % 16 in (8, 12)))
            and all(d % (p * p) != 0 for p in (3, 5, 7)) and not (d % 4 == 0 and (d // 4) % 4 in (0,))]
    for d in disc:
        chi = [kronecker(d, n) if n else 0 for n in range(abs(d))]
        q = abs(d)
        L[f"L(1,chi_{d})"] = -sum(chi[a] * mp.digamma(mp.mpf(a) / q) for a in range(1, q) if chi[a]) / q   # L(1,chi), chi non-principal
        for k in (2, 3):
            L[f"L({k},chi_{d})"] = sum(chi[a] * mp.zeta(k, mp.mpf(a) / q) for a in range(1, q) if chi[a]) / mp.mpf(q) ** k
    for m in range(2, 13):
        L[f"Cl2(pi/{m})"] = mp.clsin(2, mp.pi / m); L[f"Cl3(pi/{m})"] = mp.clsin(3, mp.pi / m); L[f"Clc3(pi/{m})"] = mp.clcos(3, mp.pi / m)
    rs = {"2": mp.mpf(2), "3": mp.mpf(3), "5": mp.mpf(5), "6": mp.mpf(6), "7": mp.mpf(7), "phi": (1 + mp.sqrt(5)) / 2,
          "1+s2": 1 + mp.sqrt(2), "2+s3": 2 + mp.sqrt(3)}
    for a in (-1, 0, 1, 2):
        for d in (1, 2, 3, 5, 6, 7):
            L[f"pi^{a}*s{d}"] = mp.pi ** a * mp.sqrt(d)
            for rn, rv in rs.items(): L[f"pi^{a}*s{d}*log({rn})"] = mp.pi ** a * mp.sqrt(d) * mp.log(rv)
    for d in range(2, 25):
        for j in range(1, d):
            if math.gcd(j, d) != 1: continue
            g = mp.gamma(mp.mpf(j) / d)
            for k in (-4, -3, -2, -1, 1, 2, 3, 4):
                for a in (-2, -1, 0, 1, 2):
                    for e in (1, 2, 3):
                        L[f"G({j}/{d})^{k}*pi^{a}*s{e}"] = g ** k * mp.pi ** a * mp.sqrt(e)
    for r in range(1, 21):
        q = mp.exp(-mp.pi * mp.sqrt(r)); K = mp.pi / 2 * mp.jtheta(3, 0, q) ** 2
        L[f"K(lam*{r})"] = K; L[f"K(lam*{r})/pi"] = K / mp.pi
    return L

if __name__ == "__main__":
    TARGETS = json.load(open(sys.argv[1])); OUT = sys.argv[2] if len(sys.argv) > 2 else "deep_id.jsonl"
    t0 = time.time(); LIB = library(); print("library", len(LIB), f"{time.time()-t0:.0f}s", flush=True)
    done = {json.loads(l)["name"] for l in open(OUT)} if os.path.exists(OUT) else set()
    for t in TARGETS:
        if t["name"] in done: continue
        t1 = time.time(); x, n = cf(t["a"], t["b"], 1000)
        if x is None:
            open(OUT, "a").write(json.dumps({"name": t["name"], "err": "no convergence", "n": n}) + "\n"); continue
        mp.mp.dps = 1000; hits = []
        for name, c in LIB.items():
            r = mp.pslq([1, x, c, x * c], maxcoeff=10 ** 8, maxsteps=10 ** 5)
            if r and (r[1] or r[3]) and (r[2] or r[3]): hits.append({"const": name, "rel": [int(v) for v in r]})
        open(OUT, "a").write(json.dumps({"name": t["name"], "terms": n, "x60": mp.nstr(x, 60), "hits": hits[:20], "nhits": len(hits)}) + "\n")
        print(t["name"], "terms", n, "hits", len(hits), hits[:2], f"{time.time()-t1:.0f}s", flush=True)
