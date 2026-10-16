r"""Batch 27 C3R-b / Lane B1: EXACT 3rd factorial-moment deviation R3 of a (q+1)-subset S of Z_m (m = q^2+q+1 PRIME), averaged over
ALL units and all shifts, in O(n^3 + l^2) via the ratio identity (verified against c3r_a.py, which uses the direct all-unit average):
F3 = (1/(m(m-1))) sum_{x in (-l,l)\0} sum_{y in (-l,l)\{0,x}} cnt(0,x,y) N(y/x),  cnt = l - (max(0,x,y) - min(0,x,y)) (2l < m),
N(rho) = #ordered distinct triples (a,b,c) of S with (c-a) = rho (b-a);  R3 = F3 / H3 - 1, H3 = (n)_3 (l)_3 / (m)_3.
Also: D_mid = RMS over ratios of height 3..6 (max(|a|,|b|), forbidden ones excluded) of N/E - 1, E = (n)_3/(m-2); D_all = RMS over all rho.
Usage: python c3r_fast.py out.jsonl  env QLO, QHI, QSTEP (every k-th prime-m q), NULLS (random sets per q), CS (e.g. 2,3,4,5,8),
SHARD=i/k, TLIM_H, QEXCLUDE (q already seen), QEXTRA (control q). Sets: Singer via singer_fast(q, Random(1000003 q)) (= b22c_gaps.singer_set); null: Random(91 q + rep).sample(range(m), q + 1)."""
import json, math, os, random, sys, time
import numpy as np
H_ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H_)
import b22c_gaps as B
T0 = time.time(); TLIM = float(os.environ.get("TLIM_H", "8.0")) * 3600

def inv_table(m):
    x = np.arange(m, dtype=np.int64); r = np.ones(m, dtype=np.int64); e = m - 2; b = x.copy()
    while e:
        if e & 1: r = (r * b) % m
        b = (b * b) % m; e >>= 1
    r[0] = 0; return r

def ratio_counts(S, m, inv):
    n = len(S); N = np.zeros(m, dtype=np.int64)
    for i in range(n):
        d = np.delete((S - S[i]) % m, i)
        r = (d[None, :] * inv[d][:, None]) % m
        N += np.bincount(r.ravel(), minlength=m); N[1] -= len(d)      # diagonal b == c gives rho = 1
    return N

def r3_exact(N, n, m, l, block=512):
    x = np.concatenate([np.arange(-l + 1, 0), np.arange(1, l)]).astype(np.int64)
    inv = np.array([pow(int(v) % m, m - 2, m) for v in x], dtype=np.int64); ym = x % m; tot = 0
    for i in range(0, len(x), block):
        X = x[i:i + block, None]; Y = x[None, :]
        cnt = l - (np.maximum(0, np.maximum(X, Y)) - np.minimum(0, np.minimum(X, Y)))
        cnt = np.where((X != Y) & (cnt > 0), cnt, 0)
        rho = (ym[None, :] * inv[i:i + block, None]) % m
        tot += int(np.sum(cnt * N[rho]))
    F3 = tot / (m * (m - 1))
    H3 = n * (n - 1) * (n - 2) * l * (l - 1) * (l - 2) / (m * (m - 1) * (m - 2))
    return F3 / H3 - 1

def singer_fast(q, rng):
    """Same set as b22c_gaps.singer_set(q, rng) (same primitive polynomial draw) but only m = q^2+q+1 steps: x^m lies in F_q*,
    so the zero pattern of the x^2 coefficient is m-periodic."""
    c = B.primitive_mod(q, 3, rng); m = q * q + q + 1
    e0, e1, e2, res = 1, 0, 0, []
    for a in range(m):
        if e2 == 0: res.append(a)
        e0, e1, e2 = (c[0] * e2) % q, (e0 + c[1] * e2) % q, (e1 + c[2] * e2) % q
    return np.array(res, dtype=np.int64), m

def small_ratios(m, Hmax=6):
    out = {}
    for b in range(1, Hmax + 1):
        for a in range(-Hmax, Hmax + 1):
            if a == 0 or math.gcd(abs(a), b) != 1: continue
            r = (a * pow(b, m - 2, m)) % m
            if r not in (0, 1) and r not in out: out[r] = max(abs(a), b)
    return out

def record(kind, q, rep, S, m, inv, Cs):
    n = len(S); N = ratio_counts(S, m, inv); E = n * (n - 1) * (n - 2) / (m - 2)
    SR = small_ratios(m); mid = np.array([N[r] / E - 1 for r, h in SR.items() if h >= 3])
    forb = [int(N[(a * pow(b, m - 2, m)) % m]) for a, b in ((-1, 1), (2, 1), (1, 2))]
    dev = N[2:] / E - 1
    return {"kind": kind, "q": q, "rep": rep, "m": m, "n": n, "forbidden_counts": forb, "D_mid": float(np.sqrt(np.mean(mid ** 2))),
            "D_all": float(np.sqrt(np.mean(dev ** 2))), **{f"R3_C{C}": r3_exact(N, n, m, C * q) for C in Cs}}

if __name__ == "__main__":
    outf = sys.argv[1]; si, sk = map(int, os.environ.get("SHARD", "0/1").split("/"))
    qlo, qhi, qst = int(os.environ.get("QLO", "179")), int(os.environ.get("QHI", "1499")), int(os.environ.get("QSTEP", "1"))
    nulls = int(os.environ.get("NULLS", "3")); Cs = [int(c) for c in os.environ.get("CS", "2,3,4,5,8").split(",")]
    qs = [q for q in B.primes(qlo, qhi) if B.factor(q * q + q + 1) == {q * q + q + 1}][::qst]
    excl = {int(v) for v in os.environ.get("QEXCLUDE", "").split(",") if v}; qs = [q for q in qs if q not in excl]
    qs += [int(v) for v in os.environ.get("QEXTRA", "").split(",") if v]          # positive-control q (values known from c3r_a)
    done = set()
    if os.path.exists(outf):
        for l_ in open(outf):
            try: r = json.loads(l_); done.add((r["kind"], r["q"], r["rep"]))
            except (ValueError, KeyError): pass
    jobs = [(kd, q, rep) for q in qs for kd, rep in [("singer", 0)] + [("null", k) for k in range(1, nulls + 1)]]
    jobs.sort(key=lambda j: -j[1])                                     # slowest (largest q) first so timing problems show at once
    for idx, (kd, q, rep) in enumerate(jobs):
        if idx % sk != si or (kd, q, rep) in done: continue
        if time.time() - T0 > TLIM: print("time limit", flush=True); break
        t0 = time.time(); m = q * q + q + 1; inv = inv_table(m)
        S = singer_fast(q, random.Random(1000003 * q))[0] if kd == "singer" else \
            np.array(sorted(random.Random(91 * q + rep).sample(range(m), q + 1)), dtype=np.int64)
        if kd == "singer" and (len(S) != q + 1 or not B.is_sidon_mod(S, m)): r = {"kind": kd, "q": q, "rep": rep, "err": "construction"}
        else: r = record(kd, q, rep, S, m, inv, Cs)
        r["sec"] = round(time.time() - t0, 1)
        open(outf, "a").write(json.dumps(r) + "\n"); print(json.dumps(r)[:200], flush=True)
