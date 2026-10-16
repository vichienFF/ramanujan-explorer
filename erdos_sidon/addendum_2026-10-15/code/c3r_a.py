"""Batch 27 C3R-a (local, descriptive; PLAN_BATCH27_DRAFT): decompose the 3rd factorial moment deviation R3 of Singer sets
into contributions of triple ratios rho = (c-a)/(b-a) mod m (m = q^2+q+1 PRIME only, so every difference is a unit).
Exact identity (all units, all shifts): R3 = sum_rho (N(rho)/E - 1) * A(rho) / sum_A, with N(rho) = #ordered distinct triples of S
with ratio rho, E = n(n-1)(n-2)/(m-2), A(rho) = mean_u cnt(0, u, u rho), cnt = max(0, l - cyclic span), sum_A = l(l-1)(l-2)/(m-1).
Reports: exact R3 (direct, all unit classes), the height-truncated sums R3_H (rho = a/b, max(|a|,|b|) <= H), and N(rho)/E for small rho.
Usage: python c3r_a.py out.jsonl [qlo qhi]"""
import json, math, random, sys, time
import numpy as np
import b22c_gaps as B
from b25m_moments import moments

def span_cnt(P, m, l):          # P: (k, npts) residues; count of windows [s, s+l) containing all points of each row
    P = np.sort(P % m, axis=1); g = np.diff(P, axis=1); wrap = P[:, 0] + m - P[:, -1]
    span = m - np.maximum(g.max(axis=1), wrap)
    return np.maximum(0, l - span)

def A_rho(rho, m, l):
    u = np.arange(1, m, dtype=np.int64)
    return span_cnt(np.stack([np.zeros_like(u), u, (u * rho) % m], 1), m, l).mean()

def ratio_counts(S, m):
    n = len(S); inv = np.array([0] + [pow(x, m - 2, m) for x in range(1, m)], dtype=np.int64)
    N = np.zeros(m, dtype=np.int64)
    for i in range(n):
        d = (S - S[i]) % m; d = np.delete(d, i)                   # b - a and c - a for all b, c != a
        r = (d[None, :] * inv[d][:, None]) % m                     # (c-a)/(b-a)
        np.fill_diagonal(r, 0)
        N += np.bincount(r.ravel(), minlength=m); N[0] -= len(d)  # remove b == c
    return N

def small_ratios(m, H):
    out = {}
    for b in range(1, H + 1):
        for a in range(-H, H + 1):
            if a == 0 or math.gcd(abs(a), b) != 1: continue
            r = (a * pow(b, m - 2, m)) % m
            if r in (0, 1) or r in out: continue
            out[r] = (a, b, max(abs(a), b))
    return out

if __name__ == "__main__":
    outf = sys.argv[1]; qlo, qhi = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (31, 211)
    qs = [q for q in B.primes(qlo, qhi) if B.factor(q * q + q + 1) == {q * q + q + 1}]
    print("prime-m q:", qs, flush=True)
    for q in qs:
        for kind, rep in (("singer", 0), ("null", 1)):
            t0 = time.time(); m = q * q + q + 1
            S = B.singer_set(q, random.Random(1000003 * q))[0] if kind == "singer" else \
                np.array(sorted(random.Random(91 * q + rep).sample(range(m), q + 1)), dtype=np.int64)
            n = len(S); N = ratio_counts(S, m); E = n * (n - 1) * (n - 2) / (m - 2)
            SR = small_ratios(m, 6); ts = np.array([t for t in range(1, m // 2 + 1)], dtype=np.int64)
            for C in (2, 3, 4, 5, 8):
                l = C * q; sumA = l * (l - 1) * (l - 2) / (m - 1)
                contrib = {r: (N[r] / E - 1) * A_rho(r, m, l) / sumA for r in SR}
                RH = {H: sum(v for r, v in contrib.items() if SR[r][2] <= H) for H in range(1, 7)}
                ex = moments(S, m, q, C, ts)["R3"]
                full = float(sum((N[r] / E - 1) * A_rho(r, m, l) for r in range(2, m)) / sumA) if m < 2500 else None
                rec = {"kind": kind, "q": q, "m": m, "C": C, "R3_exact": ex, **{f"R3_H{H}": RH[H] for H in RH},
                       "qR3_exact": q * ex, "R3_full_identity": full, "top": sorted(([f"{SR[r][0]}/{SR[r][1]}", round(float(N[r] / E), 4), round(q * v, 4)]
                                                          for r, v in contrib.items()), key=lambda z: -abs(z[2]))[:12],
                       "sec": round(time.time() - t0, 1)}
                open(outf, "a").write(json.dumps(rec) + "\n")
                print(kind, q, C, f"qR3 exact {q*ex:+.3f}", "full", None if full is None else f"{q*full:+.3f}", " ".join(f"H{H} {q*RH[H]:+.3f}" for H in (1, 2, 3, 6)), flush=True)
