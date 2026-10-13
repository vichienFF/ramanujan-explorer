"""Track A: search for new members of the "fixed a" families (a from the 23 candidates) - b = s*prod(k_i n + t_i), four factors
Stage 0: the leading coefficient B must make alpha^2+4B a square (rational characteristic roots), b(n) != 0 for all n >= 1
Stage 1 (fast proxy, numpy): count primes p in PR (range (N/2, 0.6N]) with p^2 dividing both P_N, Q_N  (full FR -> many, partial/generic -> ~0)
Stage 2: exact-integer S_N (N=200, 800), |Delta S| < 0.15
Checkpoint: one jsonl line per work unit (a, set of k) - timer - no internet / secrets"""
import argparse, glob, itertools, json, math, os, time
import numpy as np

T0 = time.time()
A_LIST = [(-3, 10, 4), (1, 9, 4), (-6, 1, 8), (8, 8, 3), (5, 13, 6), (2, -2, 3)]  # a0,a1,a2
N_PROXY = 240
PR = [127, 131, 137, 139]  # primes in (120, 144]


def lead_ok(alpha, bmax):
    out = []
    for B in range(-bmax, bmax + 1):
        d = alpha * alpha + 4 * B
        if B and d >= 0 and math.isqrt(d) ** 2 == d:
            out.append(B)
    return out


def proxy(a, facs, s, prs=PR, N=N_PROXY):
    """facs: array (M,4,2) of (k,t); s: array (M,) -> number of p in prs with p^2 | P_N and Q_N"""
    cnt = np.zeros(len(s), dtype=np.int64)
    for p in prs:
        m = p * p
        P0 = np.ones(len(s), dtype=np.int64); P1 = np.full(len(s), a[0] % m, dtype=np.int64)
        Q0 = np.zeros(len(s), dtype=np.int64); Q1 = np.ones(len(s), dtype=np.int64)
        K = facs[:, :, 0] % m; Tt = facs[:, :, 1] % m; S = s % m
        for n in range(1, N + 1):
            bn = S.copy()
            for i in range(4):
                bn = bn * ((K[:, i] * n + Tt[:, i]) % m) % m
            an = (a[0] + a[1] * n + a[2] * n * n) % m
            P0, P1 = P1, (an * P1 + bn * P0) % m
            Q0, Q1 = Q1, (an * Q1 + bn * Q0) % m
        cnt += ((P1 == 0) & (Q1 == 0))
    return cnt


def bpoly(k, t, s):
    c = [s]
    for ki, ti in zip(k, t):
        c2 = [0] * (len(c) + 1)
        for j, v in enumerate(c):
            c2[j] += v * ti; c2[j + 1] += v * ki
        c = c2
    return c  # coefficients from low to high degree


def S_exact(a, b, Ns=(200, 800)):
    A = lambda n: a[0] + a[1] * n + a[2] * n * n
    Bf = lambda n: sum(c * n ** i for i, c in enumerate(b))
    P0, P1, Q0, Q1 = 1, A(0), 0, 1; out = {}
    for n in range(1, max(Ns) + 1):
        P0, P1 = P1, A(n) * P1 + Bf(n) * P0
        Q0, Q1 = Q1, A(n) * Q1 + Bf(n) * Q0
        if n in Ns:
            g = math.gcd(P1, Q1)
            if Q1 == 0:
                return None
            out[n] = (math.log(abs(Q1)) - math.log(g)) / n
    return out


def units(args):
    ks = range(1, args.kmax + 1)
    for ai, a in enumerate(A_LIST):
        for kk in itertools.combinations_with_replacement(ks, 4):
            yield ai, kk


def run_unit(a, kk, args):
    prodk = math.prod(kk)
    Bs = [B for B in lead_ok(a[2], args.bmax) if B % prodk == 0]
    if not Bs:
        return []
    T = range(-args.tmax, args.tmax + 1)
    ts = []
    for t in itertools.product(T, repeat=4):
        # factors (k,t) in non-decreasing order (no duplicates), gcd(k,t)=1, no root at n >= 1
        pairs = list(zip(kk, t))
        if pairs != sorted(pairs):
            continue
        if any(math.gcd(k, ti) != 1 for k, ti in pairs):
            continue
        if any(ti < 0 and (-ti) % k == 0 for k, ti in pairs):
            continue
        ts.append(t)
    if not ts:
        return []
    ts = np.array(ts, dtype=np.int64)
    hits = []
    for B in Bs:
        s = B // prodk
        M = len(ts)
        facs = np.stack([np.broadcast_to(np.array(kk), (M, 4)), ts], axis=2).astype(np.int64)
        sv = np.full(M, s, dtype=np.int64)
        # stage 1 in steps: first prime first, the rest only for survivors
        c1 = proxy(a, facs, sv, prs=PR[:1])
        keep = np.nonzero(c1 > 0)[0]
        # registered condition: pass at least one of the first two (127,131) and >= thr of the four in total
        c2 = proxy(a, facs, sv, prs=PR[1:2])
        keep = np.nonzero((c1 + c2) > 0)[0]
        if len(keep) == 0:
            continue
        c = c1[keep] + c2[keep] + proxy(a, facs[keep], sv[keep], prs=PR[2:])
        for j, cj in zip(keep, c):
            if cj >= args.thr:
                t = [int(v) for v in ts[j]]
                hits.append({"a": list(a), "k": list(kk), "t": t, "s": int(s), "b": bpoly(kk, t, s), "proxy": int(cj)})
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmax", type=int, default=6)
    ap.add_argument("--tmax", type=int, default=10)
    ap.add_argument("--bmax", type=int, default=200)
    ap.add_argument("--thr", type=int, default=2)
    ap.add_argument("--out", default="track_a_out")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--time_limit_h", type=float, default=10.3)
    ap.add_argument("--stage2", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    done = set()
    for f in glob.glob(os.path.join(args.out, "*.jsonl")):
        for line in open(f):
            try:
                r = json.loads(line); done.add((r["ai"], tuple(r["kk"])))
            except ValueError:
                pass
    si, sn = (int(v) for v in args.shard.split("/"))
    U = list(units(args))[si::sn]
    if args.limit:
        U = U[:args.limit]
    print("units", len(U), "done", len(done), flush=True)
    for ai, kk in U:
        if (ai, kk) in done:
            continue
        if (time.time() - T0) / 3600 > args.time_limit_h:
            print("time limit", flush=True); break
        t1 = time.time()
        hits = run_unit(A_LIST[ai], kk, args)
        if args.stage2:
            for h in hits:
                S = S_exact(h["a"], h["b"])
                h["S200"], h["S800"] = (S[200], S[800]) if S else (None, None)
                h["fullFR"] = bool(S and abs(S[800] - S[200]) < 0.15)
        with open(os.path.join(args.out, f"ta_{os.getpid()}.jsonl"), "a") as fh:
            fh.write(json.dumps({"ai": ai, "kk": list(kk), "hits": hits}) + "\n")
        print(ai, kk, "hits", len(hits), "full", sum(h.get("fullFR", False) for h in hits),
              f"{time.time() - t1:.1f}s", f"{(time.time() - T0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
